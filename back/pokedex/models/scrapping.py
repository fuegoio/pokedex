from peewee import *
from playhouse.shortcuts import model_to_dict

from .database import db


class CommonModel(Model):
    def get_small_data(self):
        return model_to_dict(self, recurse=False, backrefs=False)

    class Meta:
        database = db
        schema = 'scrapping'


class Pokemon(CommonModel):
    id = PrimaryKeyField()
    name = CharField()


with db:
    Pokemon.create_table(fail_silently=True)
