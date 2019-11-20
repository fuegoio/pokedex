import requests

from pokedex.models.pokemon import Ability, Generation, AbilityEffects, VerboseEffect, Language, PokemonAbilities


def load_ability_from_api(name):
    request = requests.get(f'https://pokeapi.co/api/v2/ability/{name}')
    data = request.json()

    generation = Generation.get_or_none(name=data['generation']['name'])
    if generation is None:
        generation = Generation.create(name=data['generation']['name'])

    ability = Ability.get_or_none(name=name)
    if ability is None:
        db_data = {'name': data['name'], 'is_main_series': data['is_main_series'], 'generation': generation}
        ability = Ability.create(**db_data)

    AbilityEffects.delete().where(AbilityEffects.ability == ability).execute()
    for effect in data['effect_entries']:
        verbose_effect = VerboseEffect.get_or_none(short_effect=effect['short_effect'])
        if verbose_effect is None:
            language = Language.get_or_none(name=effect['language']['name'])
            if language is None:
                language = Language.create(name=effect['language']['name'])
            verbose_effect = VerboseEffect.create(effect=effect['effect'], short_effect=effect['short_effect'],
                                                  language=language)
        ability_effect = AbilityEffects.create(ability=ability, effect=verbose_effect)

    return ability


def load_abilities_from_api():
    i = 0

    next_page = 'https://pokeapi.co/api/v2/ability/'
    while next_page is not None:
        request = requests.get(next_page)
        data = request.json()

        next_page = data['next']

        for ability in data['results']:
            load_ability_from_api(ability['name'])
            i += 1

        print(f'{i} abilities loaded.')

    return i


def get_abilities(generation=None, limit=None, offset=None):
    abilities = Ability.select().offset(offset).limit(limit)
    if generation is not None:
        generation_id = Generation.get_or_none(name=generation)
        if generation_id is not None:
            abilities = Generation.select().where(Generation.name == generation)

    return abilities


def get_abilities_of_pokemons(pokemon):
    abilities = PokemonAbilities.select().where(PokemonAbilities.pokemon == pokemon)
    return abilities


def search_abilities(query, limit=None):
    query = query.lower()
    abilities = Ability.select().where(Ability.name.contains(query))
    return abilities


##################################################################################
def get_generation_name(generation_id):
    generation = Generation.get_by_id(generation_id)
    return generation.name


####################################################################################"
def get_effects_of_abilities(abilities):
    effects = AbilityEffects.select(AbilityEffects, VerboseEffect).join(VerboseEffect).where(
        AbilityEffects.ability << abilities)
    effects_by_ability = {}
    for effect in effects:
        if effect.ability.id not in effects_by_ability.keys():
            effects_by_ability[effect.ability.id] = []
            effects_by_ability[effect.ability.id].append(effect.effect)
    return effects_by_ability
