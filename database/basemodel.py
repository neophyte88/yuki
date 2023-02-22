import peewee as pw
# create a peewee database instance -- our models will use this database to
# persist information
# DATABASE = "database.db"
# database = pw.SqliteDatabase(DATABASE)

#CONFIGURATION
DATABASE_HOST = 'localhost'
DATABASE_NAME = 'yuki_db'
DATABASE_USER = 'root'
DATABASE_PASSWORD = 'toor'
DATABASE_PORT = 3306

database = pw.MySQLDatabase(DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST, port=DATABASE_PORT)


# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage.
class BaseModel(pw.Model):
    class Meta:
        database = database