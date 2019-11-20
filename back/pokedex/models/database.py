import os

from peewee import PostgresqlDatabase

db = PostgresqlDatabase(
    'pokedex',
    user='pokedex',
    password='pokedex',
    host=os.environ.get('DB_HOST', 'localhost'),
    autorollback=True
)
