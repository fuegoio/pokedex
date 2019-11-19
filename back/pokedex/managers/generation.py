import requests
from pokedex.models.pokemon import Generation, Ability, Type

def get_generations(query=None):

    if query is not None:
        generations=Generation.select().where(Generation.name == query)
    else:
        generations = Generation.select()

    return generations

# def get_generations(generations=None, limit=None):
#     generation = Generation.select().limit(limit)
#     return generation


def get_number_of_abilities_by_generation(generation=None):
    ability_of_generation = Ability.select().where(Ability.generation == generation)
    number_of_abilities_of_generation = ability_of_generation.count()
    return number_of_abilities_of_generation


def get_number_of_types_by_generation(generation=None):
    type_of_generation = Type.select().where(Type.generation == generation)
    number_of_types_of_generation = type_of_generation.count()
    return number_of_types_of_generation


def create_new_generation(generation_name):
    Generation.create(name=generation_name)
