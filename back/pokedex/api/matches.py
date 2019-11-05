from flask import request
from flask_restful import Resource

from pokedex.managers.collections import get_user_by_name
from pokedex.managers.matches import play_turn, fight

# from pokedex.managers.collections import get_pokemonscollection_by_name, delete_pokemon_from_collection, create_new_user, \
#     get_user_by_name, create_a_new_collection, get_collection_by_name, add_pokemon_to_collection, get_pokemons_from_collection

class Play(Resource):
    def get(self):

        player1_name = request.args['player1']
        player2_name = request.args['player2']
        player1 = get_user_by_name(player1_name)
        if player1 is None:
            return {'msg': 'Player1 not found'}, 404
        print(player1.name)

        player2 = get_user_by_name(player2_name)
        if player2 is None:
            return {'msg': 'Player2 not found'}, 404
        print(player2.name)

        fight(player1,player2)


