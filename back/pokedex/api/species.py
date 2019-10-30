from flask import request
from flask_restful import Resource

from pokedex.managers.species import get_species, get_species, get_pokemons_of_species, get_specie, add_variety #get_pokemons_from_specie, add_pokemon_to_specie, get_specie_by_name#, add_specie
from pokedex.managers.pokemons import get_pokemon_by_name

class Species(Resource):
    def get(self):
        pokemons = request.args.get('pokemons', 'false') == 'true'

        species = get_species()
        results = [specie.get_small_data() for specie in species]
        if pokemons:
            pokemons_by_species = get_pokemons_of_species(species)
            for specie in results:
                specie['pokemons'] = [p.name for p in pokemons_by_species[specie['id']]]

        return results

    def put(self):
        data = request.json
        variety = add_variety(data['specie'], data['pokemon'], data.get('is_default', False))
        return variety.get_small_data()
    # def get(self):
    #     pokemons = request.args.get('pokemons', 'false') == 'true'
    #     species = get_species()
    #
    #     result = []
    #     for specie in species:
    #         specie_result = specie.get_small_data()
    #
    #         if pokemons:
    #             specie_result['pokemons'] = []
    #             pokemons_of_this_specie = get_pokemons_from_specie(specie.id)
    #             for pokemon in pokemons_of_this_specie:
    #                 specie_result['pokemons'].append(pokemon.name)
    #
    #         result.append(specie_result)
    #     return result

class Specie(Resource):
    def get(self, specie_id):
        specie = get_specie(specie_id)
        results = specie.get_small_data()

        pokemons_by_species = get_pokemons_of_species([specie])
        results['pokemons'] = [p.get_small_data() for p in pokemons_by_species[specie.id]]

        return results
    # def get(self,specie_name):
    #     species = get_species(specie_name)
    #     result = []
    #     for specie in species:
    #         specie_result = {'specie': specie.name}
    #         specie_result['pokemons'] = []
    #         pokemons_of_this_specie = get_pokemons_from_specie(specie.id)
    #         for pokemon in pokemons_of_this_specie:
    #             specie_result['pokemons'].append(pokemon.get_small_data())
    #         result.append(specie_result)
    #     return result


        # pokemon_name = request.json['pokemon']
        # pokemon = get_pokemon_by_name(pokemon_name)
        # if pokemon is None:
        #     return {'msg': 'Pokeon not found'}, 404
        # specie_name = request.json['specie']
        # specie = get_specie_by_name(specie_name)
        # if specie is None:
        #     return {'msg': 'Specie not found'}, 404
        # add_pokemon_to_specie(specie, pokemon)
        # result = []
        # specie_result = {'specie': specie.name}
        # specie_result['pokemons'] = []
        # pokemons_of_this_specie = get_pokemons_from_specie(specie.id)
        # for pokemon in pokemons_of_this_specie:
        #     specie_result['pokemons'].append(pokemon.get_small_data())
        # result.append(specie_result)
        #
        # return result



    # def put(self):
    #     name = request.json['name']
    #     generation_name = request.json['generation']
    #     new_specie = add_specie(name, generation_name)
    #     return new_specie.get_small_data()
