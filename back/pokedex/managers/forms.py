import requests

from pokedex.models.pokemon import PokemonForm, Pokemon


def load_pokemon_form_from_api(name):
    request = requests.get(f'https://pokeapi.co/api/v2/pokemon-form/{name}')
    data = request.json()

    pokemon = Pokemon.get(name=data['pokemon']['name'])
    form = PokemonForm.get_or_none(name=name)
    if form is None:
        db_data = {'name': data['name'],
                   'order': data['order'],
                   'form_order': data['form_order'],
                   'is_default': data['is_default'],
                   'is_battle_only': data['is_battle_only'],
                   'is_mega': data['is_mega'],
                   'form_name': data['form_name'],
                   'pokemon': pokemon}
        form = PokemonForm.create(**db_data)

    return form


def load_pokemon_forms_from_api():
    i = 0

    next_page = 'https://pokeapi.co/api/v2/pokemon-form/'
    while next_page is not None:
        request = requests.get(next_page)
        data = request.json()

        next_page = data['next']

        for form in data['results']:
            load_pokemon_form_from_api(form['name'])
            i += 1

        print(f'{i} forms loaded.')

    return i
