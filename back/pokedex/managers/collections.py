# import requests
# from playhouse.shortcuts import update_model_from_dict
# from peewee import fn
from pokedex.models.collection import User, Collection, PokemonCollection


def create_new_user(name):
    User.create(name=name)


def get_user_by_name(user_name):
    return User.get_or_none(name=user_name)


def create_a_new_collection(name, user):
    collection = Collection.create(name=name, user=user)
    return collection


def add_pokemon_to_collection(pokemon, collection):
    PokemonCollection.create(

        collection=collection,

        pokemon_id=pokemon.id,
        name=pokemon.name,
        hp=pokemon.hp,
        special_attack=pokemon.special_attack,
        defense=pokemon.defense,
        attack=pokemon.attack,
        special_defense=pokemon.special_defense,
        speed=pokemon.speed,
    )


def delete_pokemon_from_collection(pokemon_collection, collection=None):
    # #selected_pokemons = PokemonCollection.select().where(PokemonCollection.pokemon_name == pokemon.pokemon_name,
    #                                                      PokemonCollection.collection == collection)
    # selected_pokemons.delete()
    pokemon_collection.delete_instance(recursive=True)

# def update_pokemon(pokemon, stat_name, stat_value):
#     pokemon.stat_name=stat_value
#     pokemon.save()


def get_pokemon_list(collection):
    selected_pokemons = PokemonCollection.select().where(PokemonCollection.collection == collection)
    return selected_pokemons


def get_collection_by_name(collection_name):
    return Collection.get_or_none(name=collection_name)


def get_pokemonscollection_by_name(pokemon_name, collection):

    pokemons_collection=PokemonCollection.select().where(PokemonCollection.collection_id==collection, PokemonCollection.name==pokemon_name)
    return pokemons_collection


def get_pokemons_from_collection(collection):
    pokemons_collections=PokemonCollection.select().where(PokemonCollection.collection==collection)
    return pokemons_collections