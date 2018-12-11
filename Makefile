PACKAGE=app

all: default

default: deps clean

deps:
	pip install -U -r requirements.txt

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -path '*/__pycache__/*' -delete
	rm -rf ./log/ && rm -rf ./results/ && rm -rf ./processing_result/ && rm -rf .scrapy/
	rm -rf ./code/log/ && rm -rf ./code/results/ && rm -rf ./code/processing_result/ && rm -rf ./code/.scrapy/

serve:
	python code/script.py

