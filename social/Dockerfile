FROM python:3.8

WORKDIR /app
ARG requirements=requirements/production.txt

ADD . /app

RUN pip install --no-cache-dir -r $requirements
RUN pip install --no-cache-dir -e .