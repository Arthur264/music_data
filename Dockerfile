FROM python:3.6-alpine3.8

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code
WORKDIR /code
ADD . /code/

RUN pip install -r requirements.txt

