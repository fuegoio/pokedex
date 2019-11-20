from peewee import *

from .database import db
from playhouse.shortcuts import model_to_dict


class CommonModel(Model):
    def get_small_data(self):
        return model_to_dict(self, recurse=False, backrefs=False)

    class Meta:
        database = db
        schema = 'collections'


class User(CommonModel):
    id = PrimaryKeyField()
    name = CharField


class Collection(CommonModel):
    id = PrimaryKeyField()
    name = CharField()
    user = ForeignKeyField(User)


class PokemonCollection(CommonModel):
    id = PrimaryKeyField()
    collection = ForeignKeyField(Collection)
    pokemon_id = FloatField()
    name = CharField()
    hp = FloatField()
    special_attack = FloatField()
    defense = FloatField()
    attack = FloatField()
    special_defense = FloatField()
    speed = FloatField()

with db:
    Collection.create_table(fail_silently=True)