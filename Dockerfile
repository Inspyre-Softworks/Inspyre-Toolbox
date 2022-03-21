FROM python:latest

RUN apk update

RUN apk upgrade

RUN apk add curl

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/requirements.txt

# Update pip
RUN pip install --upgrade pip

RUN pip install poetry

RUN source $HOME/.pypoetry/env

RUN poetry install

RUN poetry shell

ENV PYTHONBUFFERED 1

COPY . .
CMD ['ptipython']
