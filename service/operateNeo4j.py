# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2021/1/18 上午11:54
# @Author: 张伟
# @EMAIL: Jtyoui@qq.com
# @Notes : 操作Neo4j基本操作
from py2neo import Graph, Node, Relationship

from config import *
from operateSQL import MySQL

graph = Graph(f'http://{NEO4J_IP}:7474', username='neo4j', password=NEO4J_PASSWD)


def init_neo4j():
    """初始化索引"""
    name_key = {}
    graph.delete_all()
    with MySQL(HOST, USER, PASSWORD, CHARSET, DB) as ms:
        ls = ms.select_neo4j()
        for entity, relation, node in ls:
            if name_key.get(entity):
                a = name_key[entity]
            else:
                a = Node('Entity', name=entity)
                name_key[entity] = a
            b = Node('Node', name=node)
            ab = Relationship(a, 'relation', b, name=relation)
            graph.create(ab)


def find_neo4j(*, entity=None, node=None, relation=None) -> list:
    """查询关系"""
    print(entity, relation, node)
    if (relation is None) and all([entity, node]):
        cypher = 'match(a:Entity{name:"%s"}) - [r] -> (b:Node{name:"%s"}) return r.name' % (entity, node)
    elif (entity is None) and all([relation, node]):
        cypher = 'match(a:Entity) - [r] -> (b:Node{name:"%s"}) where r.name="%s" return a.name' % (node, relation)
    elif all([entity, relation]):
        cypher = 'match(a:Entity{name:"%s"}) - [r] -> (b:Node) where r.name="%s" return b.name' % (entity, relation)
    else:
        return []
    print(cypher)
    data = graph.run(cypher).to_table()
    result = [i[0] for i in set(data) if i[0]]
    return result
