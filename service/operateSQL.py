# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2021/1/14 下午8:13
# @Author: 张伟
# @EMAIL: Jtyoui@qq.com
# @Notes : 建立数据库和表
import pymysql
import redis_lock

from config import QUE_TXT, NEO_TXT
from operateRedis import sr


class MySQL:
    def __init__(self, host, user, passwd, charset, db, *, create_db=False):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.charset = charset
        self.db = db
        self.create_db = create_db

    def create_database(self):
        db = F'CREATE DATABASE IF NOT EXISTS {self.db} CHARACTER SET {self.charset} COLLATE utf8mb4_0900_ai_ci;'
        self.cursor.execute(db)
        print('创建库完毕')

    def create_tables(self):
        """创建表"""
        answer = F"""
        CREATE TABLE IF NOT EXISTS `answer`
        (
            `id`       int          NOT NULL AUTO_INCREMENT,
            `question` text         NOT NULL COMMENT '问句',
            `data`     text         NOT NULL COMMENT '回答数据的答案',
            `sentence` text         NOT NULL COMMENT '相似问或者推荐问',
            PRIMARY KEY (`id`)      USING BTREE
        ) ENGINE = InnoDB DEFAULT CHARSET = {self.charset} COLLATE = utf8mb4_0900_ai_ci;
        """.replace('\n', '')
        hot = f"""CREATE TABLE IF NOT EXISTS `hot`
        (
            `id`       int          NOT NULL AUTO_INCREMENT,
            `question` text         NOT NULL COMMENT '问句',
            `num`      int DEFAULT  NULL COMMENT '问句出现的次数',
            PRIMARY KEY (`id`) USING BTREE
        ) ENGINE = InnoDB DEFAULT CHARSET = {self.charset} COLLATE = utf8mb4_0900_ai_ci;""".replace('\n', '')
        neo4j = f"""CREATE TABLE IF NOT EXISTS `neo4j`
        (
            `id`       int          NOT NULL AUTO_INCREMENT,
            `entity`   varchar(255) NOT NULL COMMENT '节点',
            `relation` varchar(255) NOT NULL COMMENT '关系',
            `node`     TEXT         NOT NULL COMMENT '节点',
            PRIMARY KEY (`id`) USING BTREE
        ) ENGINE = InnoDB DEFAULT CHARSET = {self.charset} COLLATE = utf8mb4_0900_ai_ci;""".replace('\n', '')
        es = f"""CREATE TABLE IF NOT EXISTS `es`
               (
                   `id`       int          NOT NULL AUTO_INCREMENT,
                   `question` text         NOT NULL COMMENT '问句',
                   PRIMARY KEY (`id`) USING BTREE
               ) ENGINE = InnoDB DEFAULT CHARSET = {self.charset} COLLATE = utf8mb4_0900_ai_ci;""".replace('\n', '')
        self.cursor.execute(answer)
        self.cursor.execute(hot)
        self.cursor.execute(neo4j)
        self.cursor.execute(es)
        print('创建表完毕')

    def __enter__(self):
        if self.create_db:
            self.conn = pymysql.connect(host=self.host, user=self.user, password=self.passwd, charset=self.charset)
        else:
            self.conn = pymysql.connect(host=self.host, user=self.user, password=self.passwd, charset=self.charset,
                                        db=self.db)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_tb is not None:
                self.conn.rollback()
                print('执行sql语句失败，发生了异常', exc_val)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print('执行sql语句提交失败，发生了异常', e)
        finally:
            self.cursor.close()
            self.conn.close()

    def add_answer(self, question: str, data: str, sentence: str):
        """插入answer数据"""
        sql = F"INSERT INTO answer(question,data,sentence) value ('{question}','{data}','{sentence}')"
        self.cursor.execute(sql)
        return True

    def add_hot(self, question: str):
        """插入数据库用户咨询的问题"""
        with redis_lock.Lock(sr, "hot"):
            find = sr.get(question)
            if find:
                sql = f'UPDATE hot SET num=num+1 WHERE question="{question}"'
            else:
                sql = f"INSERT INTO hot(question,num) value ('{question}',1)"
                sr.set(question, 1)
            self.cursor.execute(sql)

    def get_hot_num(self, num: int):
        """获取num条热点问题"""
        sql = F"SELECT question FROM hot ORDER BY num DESC LIMIT {num}"
        result = self.cursor.execute(sql)
        ls = [i[0] for i in self.cursor.fetchall()] if result > 0 else []
        return ls

    def init_redis_hot(self):
        """初始化redis"""
        sql = 'SELECT question FROM hot'
        self.cursor.execute(sql)
        sr.flushall()
        for line in self.cursor.fetchall():
            sr.set(line[0], 1)

    def init_neo4j(self):
        """保存neo4j数据到数据库"""
        with open(NEO_TXT) as fp:
            for line in fp.readlines()[1:]:
                ls = line.strip().split(',')
                if len(ls) == 3 and all(ls):
                    sql = f"INSERT INTO neo4j(entity,relation,node) value ('{ls[0]}','{ls[1]}','{ls[2]}')"
                    self.cursor.execute(sql)

    def init_es(self):
        """保存es数据到数据库"""
        with open(QUE_TXT) as fp:
            for line in fp:
                if line.strip():
                    sql = f"INSERT INTO es(question) value ('{line.strip()}')"
                    self.cursor.execute(sql)

    def select_es(self):
        """获取es数据库的全部数据"""
        sql = 'SELECT question FROM es'
        return self.select_sql(sql)

    def select_neo4j(self):
        """获取es数据库的全部数据"""
        sql = 'SELECT entity,relation,node FROM neo4j'
        return self.select_sql(sql)

    def select_sql(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def select_entity(self):
        sql = 'SELECT DISTINCT entity FROM neo4j'
        return self.select_sql(sql)

    def select_node(self):
        sql = 'SELECT DISTINCT node FROM neo4j'
        return self.select_sql(sql)

    def select_relation(self):
        sql = 'SELECT DISTINCT relation FROM neo4j'
        return self.select_sql(sql)

    def check_entity_node(self, entity, node):
        sql = f'SELECT * FROM neo4j where entity="{entity}" and node="{node}"'
        result = self.cursor.execute(sql)
        if result > 0:
            return True
        return False
