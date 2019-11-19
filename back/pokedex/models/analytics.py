from peewee import *

from .database import db


class CommonModel(Model):
    class Meta:
        database = db
        schema = 'analytics'


class UserAgent(CommonModel):
    id = PrimaryKeyField()
    user_agent = CharField()


class SearchHistory(CommonModel):
    id = PrimaryKeyField()
    type = CharField()
    ip = CharField()
    search = CharField()


with db:
    SearchHistory.create_table(fail_silently=True)
    UserAgent.create_table(fail_silently=True)
