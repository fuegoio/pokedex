import requests

from pokedex.models.pokemon import Pokemon, Ability, PokemonAbilities, Type, PokemonTypes


def get_pokemon_by_name(name):
    pokemon = Pokemon.get_or_none(name=name)
    return pokemon


def get_pokemons_by_hp(min_hp):
    results = []

    pokemons = Pokemon.select()
    for pokemon in pokemons:
        if pokemon.hp >= min_hp:
            results.append(pokemon)

    return results


def create_pokemon(name, hp, special_attack, defense, attack, special_defense, speed):
    stats = {'hp': hp, 'special_attack': special_attack, 'defense': defense,
             'attack': attack, 'special_defense': special_defense,
             'speed': speed}
    pokemon = Pokemon.get_or_none(name=name)
    if pokemon is None:
        pokemon = Pokemon.create(name=name, **stats)
    else:
        pokemon.update(**stats).execute()

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
    if pokemon is None:
        pokemon = Pokemon.create(name=name, sprite_front=sprite_front, sprite_back=sprite_back, **stats)
    else:
        pokemon.update(**stats).execute()
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
        if type is None:
            type = Type.create(name=type_name, url=api_type['type']['url'])

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
        if ability is None:
            ability = Ability.create(name=ability_name, url=api_ability['ability']['url'])

        pokemon_ability = PokemonAbilities.create(pokemon=pokemon, ability=ability,
                                                  is_hidden=api_ability['is_hidden'],
                                                  slot=api_ability['slot'])

        abilities.append(pokemon_ability)

    return abilities


def load_all_pokemons_from_api(abilities, types):
    i = 0

    next_page = 'https://pokeapi.co/api/v2/pokemon/'
    while next_page is not None:
        request = requests.get(next_page)
        pokemons_data = request.json()

        next_page = pokemons_data['next']

        for pokemon in pokemons_data['results']:
            load_pokemon_from_api(pokemon['name'])
            if abilities:
                load_pokemon_abilities_from_api(pokemon['name'])
            if types:
                load_pokemon_types_from_api(pokemon['name'])
            i += 1

        print(f'{i} pokemons loaded.')

    return i


def search_pokemons(query, type):
    query = query.lower()
    pokemons = Pokemon.select().where(Pokemon.name.contains(query)).limit(20)

    if type is not None:
        filtered_pokemons = []
        for pokemon in pokemons:
            # types = [t.type.name for t in pokemon.types]
            types = []
            pokemontypes_de_ce_pokemon = PokemonTypes.select().where(PokemonTypes.pokemon == pokemon)
            for pokemontype in pokemontypes_de_ce_pokemon:
                type_name = pokemontype.type.name
                types.append(type_name)

            if type in types:
                filtered_pokemons.append(pokemon)
        return filtered_pokemons

    return pokemons


def edit_pokemon_stats(name, stat, new_value):
    """
    Edit stats of a pokemon
    
    :param name:
    :param stat:
    :param new_value:
    :return:
    """
    pokemon = get_pokemon_by_name(name)

    update = {stat: new_value}
    pokemon.update(**update).execute()

    return pokemon


def edit_pokemon_hp(name, new_hp):
    pokemon = get_pokemon_by_name(name)
    pokemon.hp = new_hp
    pokemon.save()

    return pokemon


def delete_pokemon(name):
    pokemon = get_pokemon_by_name(name)
    pokemon.delete_instance(recursive=True)
    return True
