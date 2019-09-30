from peewee import *

from .database import db


class Pokemon(Model):
    id = PrimaryKeyField()
    name = CharField()
    hp = FloatField()
    special_attack = FloatField()
    defense = FloatField()
    attack = FloatField()
    special_defense = FloatField()
    speed = FloatField()

    sprite_front = CharField(null=True)
    sprite_back = CharField(null=True)

    class Meta:
        database = db
        schema = 'public'

    @property
    def stats(self):
        return {'hp': self.hp, 'special_attack': self.special_attack, 'defense': self.defense, 'attack': self.attack,
                'special_defense': self.special_defense}

    def get_types_name(self):
        names = []
        for pokemon_type in self.types:
            names.append(pokemon_type.type.name)
        return names

    def get_small_data(self):
        return {'name': self.name, 'stats': self.stats, 'types': self.get_types_name(), 'sprite_front': self.sprite_front}


with db:
    Pokemon.create_table(fail_silently=True)


class Ability(Model):
    id = PrimaryKeyField()
    name = CharField()
    url = CharField()

    class Meta:
        database = db
        schema = 'public'


class PokemonAbilities(Model):
    id = PrimaryKeyField()
    pokemon = ForeignKeyField(Pokemon, backref='abilities')
    ability = ForeignKeyField(Ability, backref='pokemons')
    is_hidden = BooleanField()
    slot = IntegerField()

    class Meta:
        database = db
        schema = 'public'


with db:
    Ability.create_table(fail_silently=True)
    PokemonAbilities.create_table(fail_silently=True)


class Type(Model):
    id = PrimaryKeyField()
    name = CharField()
    url = CharField()

    class Meta:
        database = db
        schema = 'public'


class PokemonTypes(Model):
    id = PrimaryKeyField()
    pokemon = ForeignKeyField(Pokemon, backref='types')
    type = ForeignKeyField(Type, backref='pokemons')
    slot = IntegerField()

    class Meta:
        database = db
        schema = 'public'


with db:
    Type.create_table(fail_silently=True)
    PokemonTypes.create_table(fail_silently=True)
