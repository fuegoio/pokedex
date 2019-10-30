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


def get_species(egg_group=None, search=None, unused=False):
    if search is None:
        search = ""

    species = []
    for specie in PokemonSpecies.select():
        if search in specie.name:
            species.append(specie)

    if unused:
        species = [specie for specie in species if len(specie.pokemons) == 0]

    if egg_group is not None:
        filtered_species = []
        for specie in species:
            # types = [t.type.name for t in pokemon.types]
            eggroups = []

            poke_egg_group_species=PokemonSpeciesEggGroups.select().where(PokemonSpeciesEggGroups.pokemon_species==specie)
            for egg_specie in poke_egg_group_species:

                egggroup_name = egg_specie.egg_group.name
                eggroups.append(egggroup_name)

            if egg_group in eggroups:
                filtered_species.append(specie)
        return filtered_species




    return species


def get_pokemons_from_specie(specie_id):
    pokemons = []
    pokemon_species_varieties = PokemonSpeciesVariety.select(PokemonSpeciesVariety, Pokemon).join(Pokemon).where(PokemonSpeciesVariety.pokemon_species == specie_id)
    for pokemon_specie_variety in pokemon_species_varieties:
        pokemons.append(pokemon_specie_variety.pokemon)
    return pokemons


def get_specie_by_name(name):
    specie = PokemonSpecies.get_or_none(name=name)
    return specie

# def add_specie(name, generation_name):
#     # generation = Generation.get_or_none(Generation.name == generation_name)
#     # if generation is None:
#     #     generation = Generation.create(name=generation_name)
#
#     new_specie = PokemonSpecies.create(name=name, generation=generation)
#     return new_specie

def add_pokemon_to_specie(specie,pokemon):
    PokemonSpeciesVariety.create(pokemon_species=specie.id, is_default='false', pokemon=pokemon.id)



def get_specie(specie_id):
    specie = PokemonSpecies.get_or_none(id=specie_id)
    return specie


def get_pokemons_of_species(species):
    pokemons = PokemonSpeciesVariety.select(PokemonSpeciesVariety, Pokemon).join(Pokemon).where(
        PokemonSpeciesVariety.pokemon_species << species)

    pokemons_by_specie = {}
    for pokemon in pokemons:
        if pokemon.pokemon_species.id not in pokemons_by_specie.keys():
            pokemons_by_specie[pokemon.pokemon_species.id] = []
        pokemons_by_specie[pokemon.pokemon_species.id].append(pokemon.pokemon)

    return pokemons_by_specie


def add_variety(specie_id, pokemon_id, is_default=False):
    variety = PokemonSpeciesVariety.get_or_none(pokemon_species=specie_id, pokemon=pokemon_id)
    if variety is None:
        variety = PokemonSpeciesVariety.create(pokemon_species=specie_id, is_default=is_default, pokemon=pokemon_id)
    else:
        variety.is_default = is_default
        variety.save()

    return variety

def get_egg_groups():
    egggroup=EggGroup.select()
    return egggroup

def get_egg_group_by_name(name):
    egggroup = EggGroup.select(EggGroup.name==name)
    return egggroup