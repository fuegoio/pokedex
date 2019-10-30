from flask import Blueprint, request
from flask_restful import Api


from pokedex.models.database import db
from pokedex.managers.users import add_request_history

from .pokemons import Pokemon, Pokemons
from .types import Types
from .species import Species, Specie

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


def register_api(app):

    @app.route("/")
    def get_my_ip():
        ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        request_data={'method': request.method, 'url':request.url,'ip':ip, 'parameters':request.args}
        return request_data

    @api_bp.before_request
    def before_request():
        db.connect(reuse_if_open=True)
        add_request_history(get_my_ip())


    @api_bp.teardown_request
    def after_request(exception=None):
        db.close()



    api.add_resource(Pokemons, '/pokemons')
    api.add_resource(Pokemon, '/pokemon/<pokemon_name>')
    api.add_resource(Species, '/species')
    api.add_resource(Specie, '/specie/<specie_id>')
    api.add_resource(Types, '/types')
    app.register_blueprint(api_bp, url_prefix="/api/v1")
