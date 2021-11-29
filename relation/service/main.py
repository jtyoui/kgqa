# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2021/1/13 下午7:49
# @Author: 张伟
# @EMAIL: Jtyoui@qq.com
# @Notes : restFul接口
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from model import prediction_model

app = FastAPI(title='回答系统接口', description='专业植物病理回答系统', version='1.0')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/relation', summary='关系抽取')
def qa(question: str = Query(..., description='一句问话', min_length=2)):
    try:
        text = prediction_model(question)
        return {"code": 200, "text": text, "msg": "success"}
    except Exception as e:
        return dict(code=400, msg=str(e))
