from peewee import PostgresqlDatabase

db = PostgresqlDatabase(
    'pokedex',
    user='pokedex',
    password='pokedex',
    host='localhost',
    autorollback=True
)
