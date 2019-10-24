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


def get_species(search=None, unused=False):
    if search is None:
        search = ""

    species = []
    for specie in PokemonSpecies.select():
        if search in specie.name:
            species.append(specie)

    if unused:
        species = [specie for specie in species if len(specie.pokemons) == 0]
    return species


def get_pokemons_from_specie(specie_id):
    pokemons = []
    pokemon_species_varieties = PokemonSpeciesVariety.select(PokemonSpeciesVariety, Pokemon).join(Pokemon).where(PokemonSpeciesVariety.pokemon_species == specie_id)
    for pokemon_specie_variety in pokemon_species_varieties:
        pokemons.append(pokemon_specie_variety.pokemon)
    return pokemons


# def add_specie(name, generation_name):
#     # generation = Generation.get_or_none(Generation.name == generation_name)
#     # if generation is None:
#     #     generation = Generation.create(name=generation_name)
#
#     new_specie = PokemonSpecies.create(name=name, generation=generation)
#     return new_specie