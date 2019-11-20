from flask import Flask, render_template


# app = Flask()
# @app.errorhandler(Exception)

class NotFoundError(Exception):
    def __init__(self, resource, resource_id):
        Exception.__init__(self)
        self.resource = resource
        self.resource_id = resource_id


class PokemonNotFoundError(NotFoundError):
    def __init__(self, resource_id):
        NotFoundError.__init__(self, "Pokemon", resource_id)


class AbilityNotFoundError(NotFoundError):
    def __init__(self, resource_id):
        NotFoundError.__init__(self, "Ability", resource_id)


class TypesNotFoundError(NotFoundError):
    def __init__(self, resource_id):
        NotFoundError.__init__(self, "Types", resource_id)
