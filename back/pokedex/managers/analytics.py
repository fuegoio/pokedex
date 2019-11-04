from pokedex.models.analytics import SearchHistory, UserAgentHistory


def add_pokemon_search_history(ip, search):
    history = SearchHistory.create(type='pokemon', ip=ip, search=search)
    return history



def add_request_history (request_data): #method,url, ip, parameters):
    UserAgentHistory.create(method= request_data['method'], IPadress = request_data['ip'], url = request_data['url'], parameters=request_data['parameters'])



def get_user_history(user_ip):
    history=UserAgentHistory.select().where(UserAgentHistory.IPadress== user_ip)
    return history
