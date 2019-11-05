from flask import request
from pokedex.managers.collections import get_pokemonscollection_by_name, delete_pokemon_from_collection, create_new_user, \
    get_user_by_name, create_a_new_collection, get_collection_by_name, add_pokemon_to_collection
from pokedex.managers.pokemons import search_pokemons, get_pokemon_by_name, edit_pokemon
from flask_restful import Resource


class User(Resource):
    def put(self, user_name):
        # data = request.json
        create_new_user(user_name)

    def get(self, user_name):
        user = get_user_by_name(user_name)
        if user is None:
            return {'msg': 'Not found'}, 404
        return user.name


class Collections(Resource):
    def put(self):
        collection_name = request.args['name']
        collection = get_collection_by_name(collection_name)
        if collection is not None:
            return {'msg': 'Collection already exist'}, 404

        user_name = request.args['user']
        user = get_user_by_name(user_name)
        if user is None:
            return {'msg': 'Not found'}, 404

        new_collection = create_a_new_collection(collection_name, user)
        return "%s added to %s" % (new_collection.name, user.name)


class Collection(Resource):
    def put(self, collection_name):
        collection = get_collection_by_name(collection_name)
        if collection is None:
            return {'msg': 'Collection not found'}, 404
        pokemon_name = request.args['pokemon']
        pokemon = get_pokemon_by_name(pokemon_name)
        if pokemon is None:
            return {'msg': 'Not found'}, 404
        else:
            add_pokemon_to_collection(pokemon, collection)
            return "%s added to %s" % (pokemon.name, collection.name)

    def delete(self, collection_name):
        collection = get_collection_by_name(collection_name)
        if collection is None:
            return {'msg': 'Collection not found'}, 404
        pokemon_name = request.args['pokemon']
        pokemons_collection = get_pokemonscollection_by_name(pokemon_name, collection)
        if pokemons_collection is None:
            return {'msg': 'No pokemon found with this name '}, 404
        # else:
        #     print(pokemons_collection[0].name)

        delete_pokemon_from_collection(pokemons_collection[0])
        if len(pokemons_collection)>1:

            return "One %s delete from %s" % (pokemons_collection[0].name, collection.name)
        else:
            return "%s delete from %s" % (pokemons_collection[0].name, collection.name)

    def patch(self, pokemon_name):
        pokemon_collection = get_pokemonscollection_by_name(pokemon_name)
        if pokemon_collection is None:
            return {'msg': 'Not found'}, 404
        data = request.json
        edit_pokemon(pokemon_collection, data)
        pokemon_collection = get_pokemonscollection_by_name(pokemon_name)
        return pokemon_collection.name