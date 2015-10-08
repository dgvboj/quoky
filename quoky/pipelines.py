# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String, Integer


Base = declarative_base()


class Detail(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True)
    Boersen_ID = Column(Integer)
    OBID = Column(String(20))
    erzeugt_am = Column(DateTime)
    Anbieter_ID = Column(String(20))
    Anbieter_ObjektID = Column(String(100))
    Immobilientyp = Column(String(50))
    Immobilientyp_detail = Column(String(200))
    Vermarktungstyp = Column(String(50))
    Land = Column(String(30))
    Bundesland = Column(String(50))
    Bezirk = Column(String(150))
    Stadt = Column(String(150))
    PLZ = Column(String(10))
    Strasse = Column(String(100))
    Hausnummer = Column(String(40))
    Ueberschrift = Column(String(500))
    Beschreibung = Column(String(15000))
    Etage = Column(String(30))
    Kaufpreis = Column(Integer)
    Kaltmiete = Column(Integer)
    Warmmiete = Column(Integer)
    Nebenkosten = Column(Integer)
    Zimmeranzahl = Column(Integer)
    Wohnflaeche = Column(Integer)
    Monat = Column(Integer)
    url = Column(String(1000))
    Telefon = Column(String(100))
    Erstellungsdatum = Column(String(50))
    Gewerblich = Column(Integer)


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
        self.session.commit()
        self.session.close_all()

    def process_item(self, item, spider):
        detail = Detail(**item)
        self.session.add(detail)
        return item
