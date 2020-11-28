from flask import Flask, Blueprint
from flask_restplus import Api
from flask_cors import CORS
from app.config import Config

server = Flask(__name__, static_folder='static')
server.config.from_object(Config())
cors = CORS(server, resources={r"/api/*": {"origins": "*"}})
api = Api(app=server)

ns_api = api.namespace('api')

# import app.routes.test
import app.routes.git
import app.routes.other
import app.routes.ogranization
# import app.routes.social