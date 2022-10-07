# coding: utf-8
from flask import json
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, create_engine, VARCHAR, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.elements import Null

Base = declarative_base()
metadata = Base.metadata


class QaInfo(Base):
    __tablename__ = 'qa_info'

    ID = Column(Integer, primary_key=True, autoincrement=True, comment='自增ID')
    start_time = Column(DateTime)
    query = Column(String(255))
    head = Column(String(255))
    label = Column(VARCHAR(255))
    relation = Column(VARCHAR(64))
    answer = Column(String(1024))
    adopt = Column(Integer)

    def __init__(self, start_time, query, head, label, relation, answer, adopt):
        self.start_time = start_time
        self.query = query
        self.head = head
        self.label = label
        self.relation = relation
        self.answer = answer
        self.adopt = adopt


class Triples(Base):
    __tablename__ = 'triples'

    ID = Column(Integer, primary_key=True)
    info_id = Column(Integer)
    head = Column(String(255))
    head_label = Column(String(255))
    relation = Column(String(255))
    relation_type = Column(String(255))
    tail = Column(String(255))
    tail_label = Column(String(255))

    def __init__(self, info_id, head, head_label, relation, relation_type, tail, tail_label):
        self.info_id = info_id
        self.head = head
        self.head_label = head_label
        self.relation = relation
        self.relation_type = relation_type
        self.tail = tail
        self.tail_label = tail_label


class OtherQuestion(Base):
    __tablename__ = 'other_question'

    ID = Column(Integer, primary_key=True, autoincrement=True, comment='自增ID')
    start_time = Column(DateTime)
    query = Column(String(1024))
    intent = Column(String(255))
    entity = Column(String(255))
    label = Column(String(32))

    def __init__(self, start_time, query, intent, label=None, entity=None):
        self.start_time = start_time
        self.query = query
        self.intent = intent
        self.label = label
        self.entity = entity


def get_engine():
    return create_engine(
        "mysql+pymysql://root:root@localhost:3306/tcm_qa",
        encoding="utf-8",
        echo=True
    )


def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)
    print('Create table successfully!')
