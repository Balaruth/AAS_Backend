import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.uni import Uni, UniList
from resources.region import Region, RegionList
from resources.faculty import Faculty, FacultyList
from resources.course import Course, CourseList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # only affects extension behaviour
app.secret_key = 'devkey'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # default: /auth endpoint

api.add_resource(Region, '/<string:region>')
api.add_resource(Uni, '/<string:region>/<string:uni>')
api.add_resource(Facultz, '/<string:region>/<string:uni>/<string:faculty>')
api.add_resource(Course, '/<string:region>/<string:uni>/<string:faculty>/<string:course>')
api.add_resource(RegionList, '/regions')
api.add_resource(UniList, '/<string:region>/unis')
api.add_resource(FacultyList, '/<string:region>/<string:uni>/faculties')
api.add_resource(CourseList, '/<string:region>/<string:uni>/<string:faculty>/courses')
api.add_resource(UserRegister, '/register')


# get_json() params: force=True prevents an error if the json does not have the json header (even if json is incorrect)
# get_json() params: silent=True returns Null instead of an error if json is incorrectly formatted