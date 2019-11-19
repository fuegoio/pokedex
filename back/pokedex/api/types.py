from flask import request
from flask_restful import Resource

from pokedex.managers.types import get_types, get_pokemons_from_type, add_type


class Types(Resource):
    def get(self):
        pokemons = request.args.get('pokemons', 'false') == 'true'
        query = request.args.get('query', None)
        types = get_types(query)

        result = []
        for type in types:
            type_result = type.get_small_data()

            if pokemons:
                type_result['pokemons'] = []
                pokemons_of_this_type = get_pokemons_from_type(type.id)
                for pokemon in pokemons_of_this_type:
                    pokemon_result = {'id': pokemon.id, 'name': pokemon.name}
                    type_result['pokemons'].append(pokemon_result)

            result.append(type_result)
        return result

    def put(self):
        name = request.json['name']
        generation_name = request.json['generation']
        new_type = add_type(name, generation_name)
        return new_type.get_small_data()
