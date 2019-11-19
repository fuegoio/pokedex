from pokedex.models.analytics import SearchHistory
from pokedex.models.pokemon import Pokemon
from peewee import fn


def add_pokemon_search_history(ip, search):
    history = SearchHistory.create(type='pokemon', ip=ip, search=search)
    return history


def get_hp_moy():
    avg = Pokemon.select(fn.AVG(Pokemon.hp).alias('avg_hp'))
    return avg
