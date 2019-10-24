from flask import request
from flask_restful import Resource

from pokedex.managers.pokemons import search_pokemons, get_pokemon_by_name, create_pokemon, delete_pokemon
# from pokedex.managers.types import get_list_types, get_types

class Pokemons(Resource):
    def get(self):

        query = request.args['query']
        # ask_effect = bool(request.args['effect'])

        pokemons_matching = search_pokemons(query, type=None)
        pokemons = [pokemon.get_small_data() for pokemon in pokemons_matching]
        return pokemons

    def post(self):
        data = request.json
        pokemon = create_pokemon(data['name'], data['hp'], 10, 0, 0, 0, 0)
        return pokemon.get_small_data()


class Pokemon(Resource):
    def get(self, pokemon_name):
        pokemon = get_pokemon_by_name(pokemon_name)
        if pokemon is None:
            return {'msg': 'Not found'}, 404

        return pokemon.get_small_data()

    def patch(self, pokemon_name):
        return 'panic', 500

    def delete(self, pokemon_name):
        result = delete_pokemon(pokemon_name)
        return result

#
# class Types(Resource):
#     def get(self):
#         data=[]
#         ask_pokemons = bool(request.args['pokemons'])
#         types=get_types()
#         if ask_pokemons is True:
#             for type in types:
#                 pokemon_matching=search_pokemons('all', type.name)
#                 pokemon_names = [p.name for p in pokemon_matching]
#                 data.append({'type': type.name, 'pokemons' : pokemon_names})
#         else:
#             data=[type.name for type in types]
#
#         return data
