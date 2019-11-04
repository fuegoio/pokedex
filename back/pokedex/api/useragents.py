from flask import request
from flask_restful import Resource

from pokedex.managers.analytics import get_user_history


class UserAgent(Resource):
    def get(self):
        # user=request.remote_addr
        # print(request.user_agent)
        # UserAgent

        results=get_user_history()
        # result=[]
        # for elem in history:
        #     result.append(elem.get_small_data())
        #
        return results