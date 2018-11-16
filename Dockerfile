FROM python:3.6.5-alpine3.7

RUN mkdir /code
WORKDIR /code
ADD . /code/

RUN pip install -r requirements.txt
ADD ./ .

