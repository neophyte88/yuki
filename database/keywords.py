from datetime import datetime
import peewee as pw

from. basemodel import BaseModel, database as DB

class Keyword(BaseModel):

    class Meta:
        table_name = "keywords"
    
    label       = pw.CharField(max_length=255)
    category         = pw.CharField(max_length=255)
    added_on    = pw.DateTimeField(default= datetime.now)