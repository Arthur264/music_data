PACKAGE=app
TESTS_DIR=tests

all: default

default: deps clean

deps:
	pip install -U -r requirements.txt

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -path '*/__pycache__/*' -delete
	find . -type d -empty -delete
	@rm -rf tmp_test/

serve:
	python start_broker.py

