FROM python:3.12.2-alpine3.19
LABEL maintainer="mrrahbarnia@gmail.com"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir app
WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
      --disabled-password \
      --no-create-home \
      mohammadreza && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R mohammadreza:mohammadreza /vol && \
    chmod -R 700 /vol

USER mohammadreza