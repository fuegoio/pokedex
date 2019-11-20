from flask import request
from flask_restful import Resource

from pokedex.managers.analytics import add_pokemon_search_history
from pokedex.managers.pokemons import search_pokemons, get_pokemon_by_name, create_pokemon, delete_pokemon,  edit_pokemon_stats
from pokedex.managers.forms import get_forms_of_pokemons
from pokedex.managers.abilities import get_abilities_of_pokemons
from pokedex.managers.useragent import add_user_agent
from pokedex.errors.not_found import PokemonNotFoundError


class Pokemons(Resource):
    def get(self):
        query = request.args.get('query','')
        type = request.args.get('type')
        limit = request.args.get('limit')
        forms = request.args.get('forms', 'false') == 'true'
        ability = request.args.get('ability',None)
        abilities = request.args.get('abilities', 'false') == 'true'
        add_pokemon_search_history(request.remote_addr, query)
        #abilities_matching = search_abilities(query, ability=ability, limit=limit)
        pokemons_matching = search_pokemons(query, type=type, ability=ability, limit=limit)
        pokemons = [pokemon.get_small_data() for pokemon in pokemons_matching]

        if forms:
            for pokemon in pokemons:
                pokemon['forms'] = []

                forms_of_this_pokemon = get_forms_of_pokemons(pokemon['id'])
                for forms in forms_of_this_pokemon:
                    pokemon['forms'].append(forms.name)
        if abilities:
            for pokemon in pokemons:
                pokemon['abilities'] = []

                abilities_of_this_pokemon = get_abilities_of_pokemons(pokemon['id'])
                for pokemon_abilities in abilities_of_this_pokemon:
                    pokemon['abilities'].append(pokemon_abilities.ability.name)
        return pokemons

    def post(self):
        data = request.json
        pokemon = create_pokemon(data['name'], data['hp'], 10, 0, 0, 0, 0)
        return pokemon.get_small_data()


class Pokemon(Resource):
    def get(self, pokemon_name):
        pokemon = get_pokemon_by_name(pokemon_name)
        forms = request.args.get('forms', 'false') == 'true'
        abilities = request.args.get('abilities',None)
        if pokemon is None:
            # return {'msg': 'Not found'}, 404
            raise PokemonNotFoundError(pokemon_name)
        pokemon = pokemon.get_small_data()

        if forms:
            pokemon['forms'] = []
            forms_of_this_pokemon = get_forms_of_pokemons(pokemon['id'])
            for forms in forms_of_this_pokemon:
                pokemon['forms'].append(forms.name)
        return pokemon.get_small_data()

    def patch(self, pokemon_name):
        # return 'panic', 500
        stat = request.args.get('stat')
        new_value = request.args.get('new_value')
        result=edit_pokemon_stats(name=pokemon_name,stat=stat,new_value=new_value)
        if pokemon_name is None:
            return {'msg': 'Not found'}, 404
        return result.get_small_data()



    def delete(self, pokemon_name):
        result = delete_pokemon(pokemon_name)
        return result
