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
    # isin = Column(String, primary_key=True)
    id = Column(Integer, primary_key=True)
    Boersen_ID = Column(Integer)
    OBID = Column(String)
    erzeugt_am = Column(DateTime)
    Anbieter_ID = Column(String)
    Anbieter_ObjektID = Column(String)
    Immobilientyp = Column(String)
    Immobilientyp_detail = Column(String)
    Vermarktungstyp = Column(String)
    Land = Column(String)
    Bundesland = Column(String)
    Bezirk = Column(String)
    Stadt = Column(String)
    PLZ = Column(String)
    Strasse = Column(String)
    Hausnummer = Column(String)
    Ueberschrift = Column(String)
    Beschreibung = Column(String)
    Etage = Column(Integer)
    Kaufpreis = Column(Integer)
    Kaltmiete = Column(Integer)
    Warmmiete = Column(Integer)
    Nebenkosten = Column(Integer)
    Zimmeranzahl = Column(Integer)
    Wohnflaeche = Column(Integer)
    Monat = Column(Integer)
    url = Column(String)
    Telefon = Column(String)
    Erstellungsdatum = Column(String)
    Gewerblich = Column(String)


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
