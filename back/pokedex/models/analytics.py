from peewee import *

from .database import db
from playhouse.shortcuts import model_to_dict

class CommonModel(Model):
    def get_small_data(self):
        return model_to_dict(self, recurse=False, backrefs=False)

    class Meta:
        database = db
        schema = 'analytics'


class SearchHistory(CommonModel):
    id = PrimaryKeyField()
    type = CharField()
    ip = CharField()
    search = CharField()

class UserAgentHistory(CommonModel):
    id = PrimaryKeyField()
    IPadress = CharField()
    url = CharField()
    method = CharField()
    parameters = CharField(null=True)
    user_agent=CharField()




with db:
    SearchHistory.create_table(fail_silently=True)
    UserAgentHistory.create_table(fail_silently=True)
