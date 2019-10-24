from pokedex.models.user import UserRequestsHistory



def add_request_history (request_data): #method,url, ip, parameters):
    UserRequestsHistory.create(method= request_data['method'], IPadress = request_data['ip'], url = request_data['url'], parameters=request_data['parameters'])