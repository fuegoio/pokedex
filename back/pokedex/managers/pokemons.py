import requests
from playhouse.shortcuts import update_model_from_dict
from peewee import fn

from pokedex.models.pokemon import Pokemon, Ability, PokemonAbilities, Type, PokemonTypes


def get_pokemon_by_name(name):
    pokemon = Pokemon.get_or_none(name=name)
    return pokemon


def create_pokemon(name, hp, special_attack, defense, attack, special_defense, speed):
    stats = {'hp': hp, 'special_attack': special_attack, 'defense': defense,
             'attack': attack, 'special_defense': special_defense,
             'speed': speed}
    pokemon = Pokemon.get_or_none(name=name)
    if pokemon is None:
        pokemon = Pokemon.create(name=name, **stats)

    return pokemon


def load_pokemon_from_api(name):
    request = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
    pokemon_data = request.json()

    stats = {}
    for stat in pokemon_data['stats']:
        stat_name = stat['stat']['name'].replace('-', '_')
        stat_value = int(stat['base_stat'])

        stats[stat_name] = stat_value

    sprite_front = pokemon_data['sprites']['front_default']
    sprite_back = pokemon_data['sprites']['back_default']

    pokemon = Pokemon.get_or_none(name=name)
    data = {'sprite_front': sprite_front, 'sprite_back': sprite_back, **stats}
    if pokemon is None:
        pokemon = Pokemon.create(name=name, **data)
    else:
        update_model_from_dict(pokemon, data)
        pokemon.save()

    return pokemon


def load_pokemon_types_from_api(name):
    request = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
    pokemon_data = request.json()

    pokemon = get_pokemon_by_name(name)
    PokemonTypes.delete().where(PokemonTypes.pokemon == pokemon).execute()

    types = []
    for api_type in pokemon_data['types']:
        type_name = api_type['type']['name']

        type = Type.get_or_none(name=type_name)
        pokemon_type = PokemonTypes.create(pokemon=pokemon, type=type, slot=api_type['slot'])

        types.append(pokemon_type)

    return types


def load_pokemon_abilities_from_api(name):
    request = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
    pokemon_data = request.json()

    pokemon = get_pokemon_by_name(name)
    PokemonAbilities.delete().where(PokemonAbilities.pokemon == pokemon).execute()

    abilities = []
    for api_ability in pokemon_data['abilities']:
        ability_name = api_ability['ability']['name']

        ability = Ability.get_or_none(name=ability_name)
        pokemon_ability = PokemonAbilities.create(pokemon=pokemon, ability=ability,
                                                  is_hidden=api_ability['is_hidden'],
                                                  slot=api_ability['slot'])

        abilities.append(pokemon_ability)

    return abilities


def load_all_pokemons_from_api():
    i = 0

    next_page = 'https://pokeapi.co/api/v2/pokemon/'
    while next_page is not None:
        request = requests.get(next_page)
        pokemons_data = request.json()

        next_page = pokemons_data['next']

        for pokemon in pokemons_data['results']:
            load_pokemon_from_api(pokemon['name'])
            load_pokemon_abilities_from_api(pokemon['name'])
            load_pokemon_types_from_api(pokemon['name'])
            i += 1

        print(f'{i} pokemons loaded.')

    return i


def search_pokemons(query, ability_query=None, type_query=None):
    query = query.lower()
    if query is 'all':
        pokemons = Pokemon.select()
    else:
        pokemons = Pokemon.select().where(Pokemon.name.contains(query))

    if type_query is not None:
        filtered_pokemons = []
        for pokemon in pokemons:
            # types = [t.type.name for t in pokemon.types]
            types = []
            pokemontypes_de_ce_pokemon = PokemonTypes.select().where(PokemonTypes.pokemon == pokemon)
            for pokemontype in pokemontypes_de_ce_pokemon:
                type_name = pokemontype.type.name
                types.append(type_name)

            if type_query in types:
                filtered_pokemons.append(pokemon)
        pokemons = filtered_pokemons

    if ability_query is not None:
        filtered_pokemons = []
        for pokemon in pokemons:
            # types = [t.type.name for t in pokemon.types]
            abilities = []
            pokemonabilities_de_ce_pokemon = PokemonAbilities.select().where(PokemonAbilities.pokemon == pokemon)
            for pokemonability in pokemonabilities_de_ce_pokemon:
                ability_name = pokemonability.ability.name
                abilities.append(ability_name)

            if ability_query in abilities:
                filtered_pokemons.append(pokemon)
        pokemons = filtered_pokemons

    return pokemons[:10]


def edit_pokemon_stats(name, stat, new_value):
    pokemon = get_pokemon_by_name(name)

    update = {stat: new_value}
    pokemon.update(**update).execute()

    return pokemon

def edit_pokemon(pokemon, data):


    pokemon.update(**data).execute()

    return pokemon


def delete_pokemon(name):
    pokemon = get_pokemon_by_name(name)
    pokemon.delete_instance(recursive=True)
    return True


def get_stat_average():
    query = Pokemon.select(fn.AVG(Pokemon.hp).alias('hp_avg'),
                           fn.AVG(Pokemon.special_attack).alias('special_attack_avg'),
                           fn.AVG(Pokemon.defense).alias('defense_avg'),
                           fn.AVG(Pokemon.attack).alias('attack_avg'),
                           fn.AVG(Pokemon.special_defense).alias('special_defense_avg'),
                           fn.AVG(Pokemon.speed).alias('speed_avg'),
                           )

    # fn.AVG(Sample.value).over(partition_by=[Sample.counter]).alias('cavg'))
    sample = query[0]
    sample_dict = {'hp_avg': sample.hp_avg, 'special_attack_avg': sample.special_attack_avg,
                   'defense_avg': sample.defense_avg, 'attack_avg': sample.attack_avg,
                   'special_defense_avg': sample.special_defense_avg,
                   'speed_avg': sample.special_defense_avg}

    return sample_dict
