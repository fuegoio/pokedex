from flask import request
from flask_restful import Resource
from pokedex.managers.useragent import sum_requests_of_user_agent, add_user_agent


class UserAgent(Resource):
    def get(self):
        sum_requests = sum_requests_of_user_agent()

        return sum_requests
