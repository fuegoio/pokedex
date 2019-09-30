from flask import request
from flask_restful import Resource

from pokedex.managers.pokemons import search_pokemons, get_pokemon_by_name, create_pokemon, delete_pokemon


class Pokemons(Resource):
    def get(self):
        query = request.args['query']
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

    def delete(self, pokemon_name):
        result = delete_pokemon(pokemon_name)
        return result
