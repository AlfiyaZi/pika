SIBLING_CODEGEN_DIR=../rabbitmq-codegen/
AMQP_CODEGEN_DIR=$(shell [ -d $(SIBLING_CODEGEN_DIR) ] && echo $(SIBLING_CODEGEN_DIR) || echo codegen)
AMQP_SPEC_JSON_PATH=$(AMQP_CODEGEN_DIR)/amqp-0.9.1.json

PYTHON=python

all: rabbitmq/spec.py

rabbitmq/spec.py: codegen.py $(AMQP_CODEGEN_DIR)/amqp_codegen.py $(AMQP_SPEC_JSON_PATH)
	$(PYTHON) codegen.py body $(AMQP_SPEC_JSON_PATH) $@

clean:
	rm -f rabbitmq/spec.py
	rm -f rabbitmq/*.pyc

codegen:
	mkdir -p $@
	cp -r "$(AMQP_CODEGEN_DIR)"/* $@
	$(MAKE) -C $@ clean
