FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

MAINTAINER Jytoui <jtyoui@qq.com>

COPY ./service /app
COPY ./model /app/model

ENV WORKERS_PER_CORE 0.5
ENV MAX_WORKERS 4

RUN pip3 install --no-cache-dir -r /app/requirements.txt -i https://pypi.douban.com/simple