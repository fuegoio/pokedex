import requests

from pokedex.models.pokemon import Type, Generation


def get_types(search=None, unused=False):
    types = []

    if search is None:
        search = ""
        

    for type in Type.select():
        if search in type.name:
            types.append(type)
            
    if unused:
        types = [type for type in types if len(type.pokemons) == 0]
    return types


def load_type_from_api(name):
    request = requests.get(f'https://pokeapi.co/api/v2/type/{name}')
    data = request.json()

    generation = Generation.get_or_none(name=data['generation']['name'])
    if generation is None:
        generation = Generation.create(name=data['generation']['name'])

    type = Type.get_or_none(name=data['name'])
    if type is None:
        type = Type.create(name=data['name'], generation=generation)

    return type


def load_types_from_api():
    i = 0

    next_page = 'https://pokeapi.co/api/v2/type/'
    while next_page is not None:
        request = requests.get(next_page)
        data = request.json()

        next_page = data['next']

        for type in data['results']:
            load_type_from_api(type['name'])
            i += 1

        print(f'{i} type loaded.')

    return i

def get_list_types(ask_pokemons, search=None, unused=False):

    if unused:
        types = [typex.name for typex in Type.select() if len(typex.pokemons) == 0]

    elif search != None:
        types = [typex.name for typex in Type.select() if typex.pokemons == search]

    else:
        types = [typex.name for typex in Type.select()]

    return types