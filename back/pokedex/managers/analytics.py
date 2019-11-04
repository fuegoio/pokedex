from pokedex.models.analytics import SearchHistory, UserAgentHistory
from peewee import fn


def add_pokemon_search_history(ip, search):
    history = SearchHistory.create(type='pokemon', ip=ip, search=search)
    return history



def add_request_history (request_data): #method,url, ip, parameters):
    UserAgentHistory.create(user_agent= request_data['user_agent'] ,method= request_data['method'], IPadress = request_data['ip'], url = request_data['url'], parameters=request_data['parameters'])



def get_user_history():
    # history=UserAgentHistory.select().where(UserAgentHistory.IPadress== user_ip)
    results=[]
    query=UserAgentHistory.select(UserAgentHistory.user_agent, fn.Count(UserAgentHistory.user_agent).alias('number_of_request')).group_by(UserAgentHistory.user_agent)
    for user in query:
        results.append(user.user_agent + " did "+str(user.number_of_request)+ " requests")
    # users = list(query)
    # return somma
    # print(somma)
    return results
