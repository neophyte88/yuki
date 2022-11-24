import peewee as pw
# create a peewee database instance -- our models will use this database to
# persist information
DATABASE = "database.db"
database = pw.SqliteDatabase(DATABASE)

# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage.
class BaseModel(pw.Model):
    class Meta:
        database = database