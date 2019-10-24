from pokedex.models.user import UserRequestsHistory



def add_request_history (ip,url,parameters):
    UserRequestsHistory.create(IPadress = ip, url = url, parameters=parameters)