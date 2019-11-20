from flask import request
from flask_restful import Resource
from pokedex.managers.scrapping import search_data


class Datascrap(Resource):
    def get(self):
        query = request.args.get('query', '')
        limit = request.args.get('limit', '')
        datascrap_matching = search_data(query, limit=limit)
        datascrap = [data.get_small_data() for data in datascrap_matching]
        return datascrap
