from peewee import *

from .database import db
from playhouse.shortcuts import model_to_dict

class CommonModel(Model):
    # def get_small_data(self):
    #     return model_to_dict(self, recurse=False, backrefs=False)

    class Meta:
        database = db
        schema = 'collections'


class User(CommonModel):
    id = PrimaryKeyField()
    name=CharField()

class Collection(CommonModel):
    id = PrimaryKeyField()
    name = CharField()
    user=ForeignKeyField(User)

class PokemonCollection(CommonModel):
    id=PrimaryKeyField()
    collection=ForeignKeyField(Collection)

    pokemon_id = FloatField()
    pokemon_name = CharField()
    pokemon_hp = FloatField()
    pokemon_special_attack = FloatField()
    pokemon_defense = FloatField()
    pokemon_attack = FloatField()
    pokemon_special_defense = FloatField()
    pokemon_speed = FloatField()
    # pokemon_sprite_back = CharField()
    # pokemon_sprite_front = CharField()

class Match(CommonModel):
    id=PrimaryKeyField()
    player1=ForeignKeyField(User)
    player2=ForeignKeyField(User)


with db:
    User.create_table(fail_silently=True)
    Collection.create_table(fail_silently=True)
    PokemonCollection.create_table(fail_silently=True)