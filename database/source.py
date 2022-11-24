from datetime import datetime
import peewee as pw

from. basemodel import BaseModel, database as DB

class Source(BaseModel):

    class Meta:
        table_name = "sources"
    
    label       = pw.CharField(max_length=50)
    url         = pw.CharField(max_length=255)
    added_on    = pw.DateTimeField(default= datetime.now)