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
    name=CharField()

class Collection(CommonModel):
    id = PrimaryKeyField()
    name = CharField(unique=True)
    user=ForeignKeyField(User)

class PokemonCollection(CommonModel):
    id=PrimaryKeyField()
    collection=ForeignKeyField(Collection)

    pokemon_id = FloatField()
    name = CharField()
    hp = FloatField()
    special_attack = FloatField()
    defense = FloatField()
    attack = FloatField()
    special_defense = FloatField()
    speed = FloatField()





    # pokemon_sprite_back = CharField()
    # pokemon_sprite_front = CharField()

class Match(CommonModel):
    id=PrimaryKeyField()
    player1=ForeignKeyField(User)
    player2=ForeignKeyField(User)


class PokemonMatch(CommonModel):
    id=PrimaryKeyField()
    pokemon_id = FloatField()
    name = CharField()
    hp = FloatField()
    special_attack = FloatField()
    defense = FloatField()
    attack = FloatField()
    special_defense = FloatField()
    speed = FloatField()


class PokemonPlayer(CommonModel):
    id=PrimaryKeyField()
    match=ForeignKeyField(Match)
    pokemon=ForeignKeyField(PokemonMatch)










with db:
    User.create_table(fail_silently=True)
    Collection.create_table(fail_silently=True)
    PokemonCollection.create_table(fail_silently=True)