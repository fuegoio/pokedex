from peewee import *

from .database import db


class CommonModel(Model):
    class Meta:
        database = db
        schema = 'analytics'


class SearchHistory(CommonModel):
    id = PrimaryKeyField()
    type = CharField()
    ip = CharField()
    search = CharField()


with db:
    SearchHistory.create_table(fail_silently=True)
