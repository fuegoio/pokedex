from peewee import *


from .database import db



class UserRequestsHistory(Model):
    id = PrimaryKeyField()
    IPadress = CharField()
    url = CharField()
    method= CharField()
    parameters = CharField(null=True)


    class Meta:
        database = db
        schema = 'analytics'



with db:
    UserRequestsHistory.create_table(fail_silently=True)