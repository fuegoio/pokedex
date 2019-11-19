from flask import request
from flask_restful import Resource

from pokedex.managers.abilities import search_abilities, get_abilities, get_effects_of_abilities


class Abilities(Resource):
    def get(self):
        generation = request.args.get('generation', '')
        limit = request.args.get('limit', '')
        offset = request.args.get('offset', '')
        effects = request.args.get('effects', 'false') == 'true'
        # abilities_matching = search_abilities(query,limit = limit)
        # abilities = [ability.get_small_data() for ability in abilities_matching]
        abilities = get_abilities(generation, limit, offset)
        results = [ability.get_small_data() for ability in abilities]
        if effects:
            effects_by_ability = get_effects_of_abilities(abilities)
            for ability in results:
                ability['effects'] = [e.get_small_data() for e in effects_by_ability[ability['id']]]
        return results

