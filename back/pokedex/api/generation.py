from flask import request
from flask_restful import Resource

from pokedex.managers.generation import get_generations, get_number_of_abilities_by_generation, \
    get_number_of_types_by_generation, create_new_generation


class Generation(Resource):
    def get(self):
        limit = request.args.get('limit', '')
        query = request.args.get('query', None)
        abilities = request.args.get('abilities', '')
        # results = [generation.get_small_data() for generation in generations]
        number_abilities_query = request.args.get('number_abilities', 'false') == 'true'
        number_types_query = request.args.get('number_types', 'false') == 'true'
        all_generations = get_generations(query)
        generations = []
        for generation in all_generations:
            dictionary = generation.get_small_data()
            if number_abilities_query is True:
                number_abilities = get_number_of_abilities_by_generation(generation)
                dictionary['number_abilities'] = number_abilities
            if number_types_query is True:
                number_types = get_number_of_types_by_generation(generation)
                dictionary['number_abilities'] = number_types
            generations.append(dictionary)
        # if abilities:
        #     abilities_by_generation = get_abilities_by_generation(generations)
        #     for generation in results:
        #         generation['abilities'] = [a.id for a in abilities_by_generation[generation['id']]]
        return generations

    def put(self):
        generation_name = request.args['generation']
        create_new_generation(generation_name)
