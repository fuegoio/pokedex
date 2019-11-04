from flask import request
from flask_restful import Resource

from pokedex.managers.analytics import add_pokemon_search_history
from pokedex.managers.pokemons import search_pokemons, get_pokemon_by_name, create_pokemon, delete_pokemon
# from pokedex.managers.types import get_list_types, get_types

class Pokemons(Resource):
    def get(self):

        query = request.args['query']
        # query = request.args.get('query', "")
        type_query= request.args.get('type', "")
        # type_query = request.args['type']

        ask_effect = request.args.get('effect', 'false') == 'true'
        ask_shape = request.args.get('shape', 'false') == 'true'
        pokemons_matching = search_pokemons(query, type=type_query)
        pokemons = [pokemon.get_small_data(ask_effect, ask_shape) for pokemon in pokemons_matching]


        add_pokemon_search_history(request.remote_addr, query)
        
        return pokemons

    def post(self):
        data = request.json
        pokemon = create_pokemon(data['name'], data['hp'], 10, 0, 0, 0, 0)
        return pokemon.get_small_data()


class Pokemon(Resource):
    def get(self, pokemon_name):
        ask_shape = request.args.get('shape', 'false') == 'true'
        pokemon = get_pokemon_by_name(pokemon_name)
        if pokemon is None:
            return {'msg': 'Not found'}, 404

        return pokemon.get_small_data(ask_shape)

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
