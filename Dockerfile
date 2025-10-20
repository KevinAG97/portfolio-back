FROM python:3.10.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1
ENV LANG C.UTF-8

RUN pip install --upgrade pip uwsgi setuptools wheel

# copy source and install dependencies
RUN mkdir /src
COPY . /src/

WORKDIR /src
RUN pip install -r requirements.txt
