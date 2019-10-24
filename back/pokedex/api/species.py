from flask import request
from flask_restful import Resource

from pokedex.managers.species import get_species, get_pokemons_from_specie#, add_specie


class Species(Resource):
    def get(self):
        pokemons = request.args.get('pokemons', 'false') == 'true'
        species = get_species()

        result = []
        for specie in species:
            specie_result = specie.get_small_data()

            if pokemons:
                specie_result['pokemons'] = []
                pokemons_of_this_specie = get_pokemons_from_specie(specie.id)
                for pokemon in pokemons_of_this_specie:
                    specie_result['pokemons'].append(pokemon.name)

            result.append(specie_result)
        return result

class Specie(Resource):
    def get(self,specie_name):
        species = get_species(specie_name)
        result = []
        for specie in species:
            specie_result = {'specie': specie.name}#specie.get_small_data()
            specie_result['pokemons'] = []
            pokemons_of_this_specie = get_pokemons_from_specie(specie.id)
            for pokemon in pokemons_of_this_specie:
                specie_result['pokemons'].append(pokemon.get_small_data())
            result.append(specie_result)

        return result



    # def put(self):
    #     name = request.json['name']
    #     generation_name = request.json['generation']
    #     new_specie = add_specie(name, generation_name)
    #     return new_specie.get_small_data()
