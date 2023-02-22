# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class Source(peewee.Model):
    label = CharField(max_length=50)
    url = CharField(max_length=255)
    added_on = DateTimeField(default=datetime.datetime.now)
    class Meta:
        table_name = "sources"


@snapshot.append
class RawUrl(peewee.Model):
    url = TextField()
    source = snapshot.ForeignKeyField(backref='url_source', index=True, model='source')
    added_on = DateTimeField(default=datetime.datetime.now)
    class Meta:
        table_name = "raw_urls"


@snapshot.append
class EnrichedUrl(peewee.Model):
    url = snapshot.ForeignKeyField(backref='url', index=True, model='rawurl')
    effective_url = TextField()
    url_hash = CharField(max_length=32, unique=True)
    contents = TextField()
    media_uri = TextField()
    keywords = TextField()
    ip = CharField(max_length=20)
    added_on = DateTimeField(default=datetime.datetime.now)
    class Meta:
        table_name = "enriched_urls"


@snapshot.append
class Keyword(peewee.Model):
    label = CharField(max_length=255)
    category = CharField(max_length=255)
    added_on = DateTimeField(default=datetime.datetime.now)
    class Meta:
        table_name = "keywords"


