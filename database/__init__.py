import peewee as pw

from .basemodel import database 
from .source import Source
from .urls import RawUrl, EnrichedUrl

def create_tables():
    with database:
        database.create_tables([Source,RawUrl,EnrichedUrl])