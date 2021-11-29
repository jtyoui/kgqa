# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2021/1/14 下午6:40
# @Author: 张伟
# @EMAIL: Jtyoui@qq.com
# @Notes : 一些基本的服务
import json

from pydantic import BaseModel

from config import *
from operateES import find_key
from operateNeo4j import find_neo4j
from operateSQL import MySQL
import requests


class ResponseModal(BaseModel):
    """返回格式类型"""
    msg: str = 'success'
    code: int = 200
    data: list = []
    sentence: list = []


def similarity(sentence: str, num=5) -> list:
    """返回相似语句
    :param sentence: 问句
    :param num: 返回相似句前几条
    """
    result = find_key(QUE_INDEX, QUE_DOC, sentence, num)
    return result


def recommend(sentence: str, num=5) -> list:
    """返回推荐问题
    :param sentence: 问句
    :param num: 返回推荐问前几条
    """
    return similarity(sentence, num)


def get_data(ls, sentence):
    """根据数据库数据去匹配字段"""
    data = []
    for line in ls:
        if line[0] in sentence:
            data.append(line[0])
    if data:
        return max(data, key=lambda x: len(x))
    return None


def answer(sentence: str) -> tuple:
    """搜索问句的答案"""
    with MySQL(HOST, USER, PASSWORD, CHARSET, db=DB) as ms:
        entity = get_data(ms.select_entity(), sentence)
        node = get_data(ms.select_node(), sentence)
    result = requests.get(f'http://{RELATION_IP}/relation?question={sentence}').json()
    if result['code'] == 200:
        relation = result['text']
        if entity and node:
            node = None
        data = find_neo4j(entity=entity, node=node, relation=relation)
        return data, entity
    assert Exception("找不到关系错误！")


def get_hot(num: int) -> list:
    """获取热点问题
    :param num: 返回热点问题前几条
    """
    with MySQL(HOST, USER, PASSWORD, CHARSET, db=DB) as ms:
        result = ms.get_hot_num(num)
    return result


def insert_answer(question: str, data: str, sentence: list):
    """插入问答返回数据"""
    st = json.dumps(sentence, ensure_ascii=False)
    with MySQL(HOST, USER, PASSWORD, CHARSET, db=DB) as ms:
        ms.add_hot(question)
        ms.add_answer(question, data, st)
