import requests

from pokedex.models.pokemon import Type, Generation, PokemonTypes, Pokemon


def get_types(search=None, unused=False):
    if search is None:
        search = ""

    types = []
    for type in Type.select():
        if search in type.name:
            types.append(type)

    if unused:
        types = [type for type in types if len(type.pokemons) == 0]
    return types


def add_type(name, generation_name):
    generation = Generation.get_or_none(Generation.name == generation_name)
    if generation is None:
        generation = Generation.create(name=generation_name)

    new_type = Type.create(name=name, generation=generation)
    return new_type


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


def get_pokemons_from_type(type_id):
    pokemons = []
    pokemon_types = PokemonTypes.select(PokemonTypes, Pokemon).join(Pokemon).where(PokemonTypes.type == type_id)
    for pokemon_type in pokemon_types:
        pokemons.append(pokemon_type.pokemon)
    return pokemons
