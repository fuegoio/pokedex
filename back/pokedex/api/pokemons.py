from flask import request
from flask_restful import Resource

from pokedex.managers.analytics import add_pokemon_search_history
from pokedex.managers.pokemons import search_pokemons, get_pokemon_by_name, create_pokemon, delete_pokemon


class Pokemons(Resource):
    def get(self):
        query = request.args['query']
        pokemons_matching = search_pokemons(query, type=None)
        pokemons = [pokemon.get_small_data() for pokemon in pokemons_matching]

        add_pokemon_search_history(request.remote_addr, query)

        return pokemons

    def post(self):
        data = request.json
        pokemon = create_pokemon(data['name'], data['hp'], 10, 0, 0, 0, 0)
        return pokemon.get_small_data()


class Pokemon(Resource):
    def get(self, pokemon_name):
        pokemon = get_pokemon_by_name(pokemon_name)
        return pokemon.get_small_data()

    def patch(self, pokemon_name):
        return 'panic', 500

    def delete(self, pokemon_name):
        result = delete_pokemon(pokemon_name)
        return result
