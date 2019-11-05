from flask import request
from pokedex.managers.collections import create_new_user, get_user_by_name
from flask_restful import Resource



class User(Resource):
    def put (self, user_name):
        # data = request.json
        create_new_user(user_name)
    def get (self, user_name):
        user=get_user_by_name(user_name)
        if user is None:
            return {'msg': 'Not found'}, 404
        return user.name


