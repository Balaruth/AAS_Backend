import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.uni import Uni, UniList
from resources.bundesland import Bundesland, BundeslandList
from resources.fachbereich import Fachbereich, FachbereichList
from resources.studium import Studium, StudiumList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # only affects extension behaviour
app.secret_key = 'devkey'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # default: /auth endpoint

api.add_resource(Bundesland, '/<string:bundesland>')
api.add_resource(Uni, '/<string:bundesland>/<string:uni>')
api.add_resource(Fachbereich, '/<string:bundesland>/<string:uni>/<string:fachbereich>')
api.add_resource(Studium, '/<string:bundesland>/<string:uni>/<string:fachbereich>/<string:studium>')
api.add_resource(BundeslandList, '/bundeslaender')
api.add_resource(UniList, '/<string:bundesland>/unis')
api.add_resource(FachbereichList, '/<string:bundesland>/<string:uni>/fachbereiche')
api.add_resource(StudiumList, '/<string:bundesland>/<string:uni>/<string:fachbereich>/studien')
api.add_resource(UserRegister, '/register')

# get_json() params: force=True prevents an error if the json does not have the json header (even if json is incorrect)
# get_json() params: silent=True returns Null instead of an error if json is incorrectly formatted