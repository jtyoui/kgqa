# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2021/1/15 下午2:11
# @Author: 张伟
# @EMAIL: Jtyoui@qq.com
# @Notes : redis服务器的一些操作
from redis import StrictRedis

from config import *

sr = StrictRedis(host=REDIS_HOST, port='6379')
