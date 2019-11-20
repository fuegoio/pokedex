import requests
from lxml import html
from tqdm import tqdm
from pokedex.models.scrapping import Pokemonscraping, Generationscraping


def search_data(query, limit=None):
    query = query.lower()
    datascrap = Pokemonscraping.select().where(Pokemonscraping.name.contains(query))
    return datascrap


def load_generations_from_wikipedia():
    wikipedia_request = requests.get('https://en.wikipedia.org/wiki/List_of_Pok%C3%A9mon')
    xpath = '/html/body/div[3]/div[3]/div[4]/div/table[1]'
    tree = html.fromstring(wikipedia_request.content)
    generation_tables = tree.xpath(xpath)

    generation_table = generation_tables[0]
    print(generation_table.text_content())

    generation_table_rows = generation_table.findall('.//tr')
    generations = []

    for row in generation_table_rows[3:]:
        i = 0
        header_generation = row.findall('.//th')[0].text_content()
        generations.append(header_generation)
        for cell in row.findall('td'):
            i += 1
            if i == 0:
                content = cell.text_content()
                generation_name = content
                generations.append(generation_name)
                i += 1

            if i == 1:
                content = cell.text_content()
                generation_year = content.split("–")
                generations.append(generation_year)
                i += 1

            if i == 2:
                content = cell.text_content()
                generation_version = content.split(",")
                generations.append(generation_version)
                i += 1

            if i == 3 or i == 4:
                generations.append(None)
                i += 1
            if i == 5:
                content = cell.text_content()
                number_of_new_pokemon_in_generation = content
                generations.append(number_of_new_pokemon_in_generation)
                i += 1
            if i == 6:
                content = cell.text_content()
                number_of_all_pokemons_in_generation = content
                generations.append(number_of_all_pokemons_in_generation)
                i += 1

    Generationscraping.delete().execute()

    for generation_name in tqdm(generations):
        generation_name = generations[0]
        # for generation_year in tqdm(generations)
        Generationscraping.create(name=generation_name)


def load_pokemons_from_wikipedia():
    wikipedia_request = requests.get('https://en.wikipedia.org/wiki/List_of_Pok%C3%A9mon')
    xpath = '/ html / body / div[3] / div[3] / div[4] / div / table[3]'
    tree = html.fromstring(wikipedia_request.content)
    pokemons_tables = tree.xpath(xpath)

    pokemons_table = pokemons_tables[0]
    # print (pokemons_table.text_content())

    pokemons_table_rows = pokemons_table.findall('.//tr')

    pokemons = {}

    for row in pokemons_table_rows[2:]:
        pokemon_id = None

        i = 0
        for cell in row.findall('td'):
            if i % 2 == 0:
                content = cell.text_content()
                if 'No additional' not in content:
                    pokemon_id = int(content)
                    pokemons[pokemon_id] = None
                else:
                    i += 1
            else:
                symbols_to_strip = ['\n', '※', '♭', '[c]', '~', '♭[e]', '♯']
                pokemon_name = cell.text_content()
                for symbol in symbols_to_strip:
                    pokemon_name = pokemon_name.strip(symbol)