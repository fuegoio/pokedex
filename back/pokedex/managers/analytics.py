from pokedex.models.analytics import SearchHistory


def add_pokemon_search_history(ip, search):
    history = SearchHistory.create(type='pokemon', ip=ip, search=search)
    return history
