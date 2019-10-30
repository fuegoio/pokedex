from peewee import *
from playhouse.shortcuts import model_to_dict

from .database import db


class CommonModel(Model):
    def get_small_data(self):
        return model_to_dict(self, recurse=False, backrefs=False)

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
    sprite_back = CharField()
    sprite_front = CharField()

    @property
    def stats(self):
        return {'hp': self.hp, 'special-attack': self.special_attack, 'defense': self.defense, 'attack': self.attack,
                'special-defense': self.special_defense, 'speed': self.speed}

    def get_small_data(self,ask_effect='false'):
        if ask_effect is True:
            return {"id": self.id, "name": self.name, **self.stats, 'sprite_back': self.sprite_back,
                    'sprite_front': self.sprite_front,'effects': self.get_abilities_effect()}
        else:
            return {"id": self.id, "name": self.name, **self.stats, 'sprite_back': self.sprite_back,
                    'sprite_front': self.sprite_front}


    def get_abilities_effect(self):
        abilities_effects_list= []
        for pokemon_ability in self.abilities:
            effects_list=[]
            for ability_effect in pokemon_ability.ability.effects:
                effects_list.append(ability_effect.effect.effect)
            abilities_effects_list.append(effects_list)
        return abilities_effects_list


class Ability(CommonModel):
    id = PrimaryKeyField()
    name = CharField()
    is_main_series = BooleanField()
    generation = ForeignKeyField(Generation)


class AbilityEffects(CommonModel):
    id = PrimaryKeyField()
    ability = ForeignKeyField(Ability, backref='effects')
    effect = ForeignKeyField(VerboseEffect, backref='abilities')


class PokemonAbilities(CommonModel):
    id = PrimaryKeyField()
    pokemon = ForeignKeyField(Pokemon, backref='abilities')
    ability = ForeignKeyField(Ability, backref='pokemons')
    is_hidden = BooleanField()
    slot = IntegerField()


class Type(CommonModel):
    id = PrimaryKeyField()
    name = CharField()
    generation = ForeignKeyField(Generation)

    def get_small_data(self):
        return {'id': self.id, 'name': self.name,
                'generation': self.generation.name}


class PokemonTypes(CommonModel):
    id = PrimaryKeyField()
    pokemon = ForeignKeyField(Pokemon, backref='types')
    type = ForeignKeyField(Type, backref='pokemons')
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

    def get_egg_groups(self):
        egg_group_list= []
        for egg_specie in self.egg_groups:
            #print(egg_specie.egg_group.name)
            egg_group_list.append(egg_specie.egg_group.name)

            # effects_list=[]
            # for ability_effect in pokemon_ability.ability.effects:
            #     effects_list.append(ability_effect.effect.effect)
            # abilities_effects_list.append(effects_list)
        return egg_group_list



    def get_small_data(self):

        return {'id': self.id, 'name': self.name,
                'order': self.order, 'gender_rate': self.gender_rate,
                'capture_rate': self.capture_rate, 'base_happiness': self.base_happiness,
                'is_baby': self.is_baby, 'egg_groups': self.get_egg_groups()}


class PokemonSpeciesVariety(CommonModel):
    id = PrimaryKeyField()
    pokemon_species = ForeignKeyField(PokemonSpecies)
    is_default = BooleanField()
    pokemon = ForeignKeyField(Pokemon)


class PokemonSpeciesEggGroups(CommonModel):
    id = PrimaryKeyField()
    pokemon_species = ForeignKeyField(PokemonSpecies, backref='egg_groups')
    egg_group = ForeignKeyField(EggGroup, backref='pokemon_species')


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
