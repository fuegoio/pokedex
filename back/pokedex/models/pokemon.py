from peewee import *

from .database import db


class CommonModel(Model):
    class Meta:
        database = db
        schema = 'pokemon'


class Generation(CommonModel):
    id = PrimaryKeyField()
    name = CharField()


class Language(CommonModel):
    id = PrimaryKeyField()
    name = TextField()


class VerboseEffect(CommonModel):
    id = PrimaryKeyField()
    effect = TextField()
    short_effect = CharField()
    language = ForeignKeyField(Language)


class Pokemon(CommonModel):
    id = PrimaryKeyField()
    name = CharField()
    hp = FloatField()
    special_attack = FloatField()
    defense = FloatField()
    attack = FloatField()
    special_defense = FloatField()
    speed = FloatField()


class Ability(CommonModel):
    id = PrimaryKeyField()
    name = CharField()
    is_main_series = BooleanField()
    generation = ForeignKeyField(Generation)


class AbilityEffects(CommonModel):
    id = PrimaryKeyField()
    ability = ForeignKeyField(Ability)
    effect = ForeignKeyField(VerboseEffect)


class PokemonAbilities(CommonModel):
    id = PrimaryKeyField()
    pokemon = ForeignKeyField(Pokemon)
    ability = ForeignKeyField(Ability)
    is_hidden = BooleanField()
    slot = IntegerField()


class Type(CommonModel):
    id = PrimaryKeyField()
    name = CharField()
    generation = ForeignKeyField(Generation)


class PokemonTypes(CommonModel):
    id = PrimaryKeyField()
    pokemon = ForeignKeyField(Pokemon)
    type = ForeignKeyField(Type)
    slot = IntegerField()


class PokemonForm(CommonModel):
    id = PrimaryKeyField()
    name = CharField()
    order = IntegerField()
    form_order = IntegerField()
    is_default = BooleanField()
    is_battle_only = BooleanField()
    is_mega = BooleanField()
    form_name = CharField()
    pokemon = ForeignKeyField(Pokemon)


class EggGroup(CommonModel):
    id = PrimaryKeyField()
    name = CharField()


class PokemonSpecies(CommonModel):
    id = PrimaryKeyField()
    name = CharField()
    order = IntegerField()
    gender_rate = IntegerField()
    capture_rate = IntegerField()
    base_happiness = IntegerField()
    is_baby = BooleanField()


class PokemonSpeciesVariety(CommonModel):
    id = PrimaryKeyField()
    pokemon_species = ForeignKeyField(PokemonSpecies)
    is_default = BooleanField()
    pokemon = ForeignKeyField(Pokemon)


class PokemonSpeciesEggGroups(CommonModel):
    id = PrimaryKeyField()
    pokemon_species = ForeignKeyField(PokemonSpecies)
    egg_group = ForeignKeyField(EggGroup)


with db:
    Generation.create_table(fail_silently=True)
    Language.create_table(fail_silently=True)
    VerboseEffect.create_table(fail_silently=True)
    Pokemon.create_table(fail_silently=True)
    Ability.create_table(fail_silently=True)
    AbilityEffects.create_table(fail_silently=True)
    PokemonAbilities.create_table(fail_silently=True)
    Type.create_table(fail_silently=True)
    PokemonTypes.create_table(fail_silently=True)
    PokemonForm.create_table(fail_silently=True)
    EggGroup.create_table(fail_silently=True)
    PokemonSpecies.create_table(fail_silently=True)
    PokemonSpeciesVariety.create_table(fail_silently=True)
    PokemonSpeciesEggGroups.create_table(fail_silently=True)
