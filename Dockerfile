FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

MAINTAINER Jytoui <jtyoui@qq.com>

COPY ./requirements.txt /requirements.txt
COPY ./service /app

# 加入pip源
ENV pypi https://pypi.douban.com/simple

RUN pip3 install --no-cache-dir -r /requirements.txt -i ${pypi}
