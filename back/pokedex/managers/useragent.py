import requests
from peewee import fn
from flask import request

from pokedex.models.analytics import UserAgent


def add_user_agent():
    get_user = request.headers.get('User-Agent')
    add_user = UserAgent.create(get_user=get_user)
    add_user.save()
    return add_user


def sum_requests_of_user_agent():
    query = UserAgent.select(UserAgent.user_agent,
                             fn.Count(UserAgent.user_agent).alias('count')).group_by(UserAgent.user_agent)
    result = []

    for i in query:
        result.append({'User_Agent': i.user_agent, 'count': i.count})
    return result


