import requests

from pokedex.models.pokemon import PokemonSpecies, EggGroup, PokemonSpeciesEggGroups, PokemonSpeciesVariety, Pokemon


def load_pokemon_species_from_api(name):
    request = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{name}')
    data = request.json()

    species = PokemonSpecies.get_or_none(name=name)
    if species is None:
        db_data = {'name': data['name'],
                   'order': data['order'],
                   'gender_rate': data['gender_rate'],
                   'capture_rate': data['capture_rate'],
                   'base_happiness': data['base_happiness'],
                   'is_baby': data['is_baby']}
        species = PokemonSpecies.create(**db_data)

    PokemonSpeciesEggGroups.delete().where(PokemonSpeciesEggGroups.pokemon_species == species).execute()
    for api_egg_group in data['egg_groups']:
        egg_group = EggGroup.get_or_none(name=api_egg_group['name'])
        link = PokemonSpeciesEggGroups.create(pokemon_species=species, egg_group=egg_group)

    PokemonSpeciesVariety.delete().where(PokemonSpeciesVariety.pokemon_species == species).execute()
    for variety in data['varieties']:
        pokemon = Pokemon.get_or_none(name=variety['pokemon']['name'])
        PokemonSpeciesVariety.create(pokemon_species=species, is_default=variety['is_default'], pokemon=pokemon)

    return species


def load_pokemons_species_from_api():
    i = 0

    next_page = 'https://pokeapi.co/api/v2/pokemon-species/'
    while next_page is not None:
        request = requests.get(next_page)
        data = request.json()

        next_page = data['next']

        for species in data['results']:
            load_pokemon_species_from_api(species['name'])
            i += 1

        print(f'{i} species loaded.')

    return i
