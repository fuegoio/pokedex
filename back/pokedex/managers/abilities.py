import requests

from pokedex.models.pokemon import Ability, Generation, AbilityEffects, VerboseEffect, Language


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
            verbose_effect = VerboseEffect.create(effect=effect['effect'], short_effect=effect['short_effect'], language=language)
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
