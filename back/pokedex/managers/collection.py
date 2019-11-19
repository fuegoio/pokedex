from pokedex.models.collection import User, PokemonCollection, Collection


def get_user_by_name(user_name):
    return User.get_or_none(name=user_name)


def create_new_user(user_name):
    User.create(name=user_name)


def get_collection_by_name(collection_name):
    return Collection.get_or_none(name=collection_name)


def get_collection_of_pokemons_by_name(pokemon_name, collection):
    collection_of_pokemons = PokemonCollection.select().where(PokemonCollection.collection_id == collection,
                                                              PokemonCollection.name == pokemon_name)
    return collection_of_pokemons


def get_pokemons_from_collection(collection):
    pokemon_from_collection = PokemonCollection.select().where(PokemonCollection.collection == collection)
    return pokemon_from_collection


def create_new_collection(name, user):
    collection = Collection.create(name=name, user=user)
    return collection


def add_new_pokemon_to_collection(pokemon, collection):
    PokemonCollection.create(collection=collection,
                             pokemon_id=pokemon.id,
                             name=pokemon.name,
                             hp=pokemon.hp,
                             special_attack=pokemon.special_attack,
                             defense=pokemon.defense,
                             attack=pokemon.attack,
                             special_defense=pokemon.special_defense,
                             speed=pokemon.speed)


def delete_pokemon_from_collection(pokemon_from_collection):
    pokemon_from_collection.delete_instance(recursive=True)
