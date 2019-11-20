from peewee import *
from playhouse.shortcuts import model_to_dict

from .database import db


class CommonModel(Model):
    def get_small_data(self):
        return model_to_dict(self, recurse=False, backrefs=False)

    class Meta:
        database = db
        schema = 'scraping'


class Pokemonscraping(CommonModel):
    id = PrimaryKeyField()
    name = CharField()


class Generationscraping(CommonModel):
    id = PrimaryKeyField()
    name = CharField()


with db:
    Pokemonscraping.create_table(fail_silently=True)
    Generationscraping.create_table(fail_silently=True)
