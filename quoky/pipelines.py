# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def get_session(db, create=False):
    '''Get sqlalchemy session, create database if requested'''
    engine = create_engine(db)
    if create:
        Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()


class DatabasePipeline(object):

    def __init__(self, db):
        self.db = db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(db=crawler.settings.get('DB'))

    def open_spider(self, spider):
        self.session = get_session(self.db, True)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        return item
