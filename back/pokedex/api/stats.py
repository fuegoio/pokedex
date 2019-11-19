from flask_restful import Resource

from pokedex.managers.analytics import get_hp_moy

class Stats(Resource):
    def get(self):
        hp_moy=get_hp_moy()
        #print (hp_moy)
        stats={'hp_moy':hp_moy[0].avg_hp}
        return stats