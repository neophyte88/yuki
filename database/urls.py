from datetime import datetime

import peewee as pw

from .basemodel import BaseModel
from .source import Source

class RawUrl(BaseModel):

    class Meta:
        table_name = "raw_urls"
        collation = "utf8mb4_unicode_ci"
    
    url      = pw.CharField(max_length=255, null=False)
    source   = pw.ForeignKeyField(Source, backref="url_source")
    added_on = pw.DateTimeField(default=datetime.now)

class EnrichedUrl(BaseModel):
    
    class Meta:
        table_name = "enriched_urls"
        collation = "utf8mb4_unicode_ci"

    url           = pw.ForeignKeyField(RawUrl, backref="url")
    effective_url = pw.TextField()
    url_hash      = pw.CharField(max_length=32, unique=True)
    contents      = pw.TextField()
    media_uri     = pw.TextField()
    keywords      = pw.TextField()
    ip            = pw.CharField(max_length=20)
    added_on      = pw.DateTimeField(default=datetime.now)