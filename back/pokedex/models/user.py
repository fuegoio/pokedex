from peewee import *


from .database import db



class UserRequestsHistory:
    id = PrimaryKeyField()
    IPadress = CharField()
    url = CharField()
    parameters = CharField(null=True)


    class Meta:
        database = db
        schema = 'pokemon'