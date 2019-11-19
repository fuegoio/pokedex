from flask import request
from flask_restful import Resource
from pokedex.managers.collections import *
from pokedex.managers.pokemons import get_pokemon_by_name


class User(Resource):
    def get(self, user_name):
        user = get_user_by_name(user_name)
        return user.name

    def put(self, user_name):
        create_new_user(user_name)


class Collection(Resource):
    def get(self, collection_name):
        collection = get_collection_by_name(collection_name)
        collection_of_pokemons = get_pokemons_from_collection(collection)
        result = []
        for stats in collection_of_pokemons:
            result.append(stats.get_small_data())
            return result

    def put(self, collection_name):
        collection = get_collection_by_name(collection_name)
        pokemon_name = request.arg.get['pokemon']
        pokemon = get_pokemon_by_name(pokemon_name)
        add_new_pokemon_to_collection(pokemon, collection)

    def delete(self, collection_name):
        collection = get_collection_by_name(collection_name)
        pokemon_name = request.arg.get['pokemon']
        collection_of_pokemons = get_collection_of_pokemons_by_name(pokemon_name, collection)
        delete_pokemon_from_collection(collection_of_pokemons)

    def patch(self, collection_name):
        collection = get_collection_by_name(collection_name)
        pokemon = request.arg.get['pokemon']
        collection_of_pokemons = get_collection_of_pokemons_by_name(pokemon, collection)
        edit_pokemon(collection_of_pokemons)
        collection_of_pokemons = get_collection_of_pokemons_by_name(pokemon, collection)