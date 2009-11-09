#!/usr/bin/env python
'''
Example of simple consumer, waits one message, replies an ack and exits.
'''

import sys
import pika
import asyncore

conn = pika.AsyncoreConnection(pika.ConnectionParameters(
        sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1',
        credentials = pika.PlainCredentials('guest', 'guest')))

print 'Connected to %r' % (conn.server_properties,)

ch = conn.channel()
ch.queue_declare(queue="test", durable=True, exclusive=False, auto_delete=False)

should_quit = False

def handle_delivery(ch, method, header, body):
    print "method=%r" % (method,)
    print "header=%r" % (header,)
    print "  body=%r" % (body,)
    ch.basic_ack(delivery_tag = method.delivery_tag)

    global should_quit
    should_quit = True

tag = ch.basic_consume(handle_delivery, queue = 'test')
while conn.is_alive() and not should_quit:
    asyncore.loop(count = 1)
if conn.is_alive():
    ch.basic_cancel(tag)
    conn.close()

print conn.connection_close
