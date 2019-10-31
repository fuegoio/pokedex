from flask import request
from flask_restful import Resource

from pokedex.managers.egg_groups import get_egg_groups, get_pokemons_from_egg_group


class EggGroups(Resource):
    def get(self):
        pokemons = request.args.get('pokemons', 'false') == 'true'
        egg_groups = get_egg_groups()

        result = []
        for egg_group in egg_groups:
            egg_group_result = egg_group.get_small_data()

            if pokemons:
                egg_group_result['pokemons'] = []
                pokemons_of_this_egg_group = get_pokemons_from_egg_group(egg_group.id)
                for pokemon in pokemons_of_this_egg_group:
                    pokemon_result = {'id': pokemon.id, 'name': pokemon.name}
                    egg_group_result['pokemons'].append(pokemon_result)

            result.append(egg_group_result)
        return result
