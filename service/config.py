# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2021/1/14 上午9:55
# @Author: 张伟
# @EMAIL: Jtyoui@qq.com
# @Notes : 配置文件
import os

CUR_DIR = os.path.dirname(__file__)  # 当前文件夹路径
DATA_DIR = os.path.join(os.path.dirname(CUR_DIR), 'data')  # 数据文件夹路径
QUE_TXT = os.path.join(DATA_DIR, 'questions.txt')
NEO_TXT = os.path.join(DATA_DIR, 'relation.csv')

HOST_LIST = [
    {"host": 'es01', "port": 9200},
    {"host": 'es02', "port": 9201},
    {"host": 'es03', "port": 9202}
]  # es的ip

QUE_INDEX = 'que_index'  # es的索引
QUE_DOC = 'que_doc'  # es的文档
HOST = 'mysql'  # mysql的ip地址
USER = 'root'  # mysql的账号
PASSWORD = 'password'  # mysql的密码
DB = 'wss'  # mysql的数据库
REDIS_HOST = 'redis'  # redis的ip
CHARSET = 'utf8mb4'  # mysql的编码
NEO4J_IP = 'neo4j'
NEO4J_PASSWD = 'password'
RELATION_IP = 'relation'
