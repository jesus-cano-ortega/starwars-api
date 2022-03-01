"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)



# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_all_users():
    # get all the user
    user_query = User.query.all()
    # map the results and your list of user inside of the all_user variable
    all_user = list(map(lambda x: x.serialize(), user_query))
    return jsonify(all_user), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_just_one_user(user_id):
    user = User.query.get(user_id)
    return jsonify(user.serialize()), 200

@app.route('/planet', methods=['GET'])
def get_all_planet():
    planet_query = Planet.query.all()
    all_planet = list(map(lambda x: x.serialize(), planet_query))
    return jsonify(all_planet), 200

#create new planet
#{ 'name': 'new_planet'}
@app.route('/planet', methods=['POST'])
def create_planet():
    # First we get the payload json
    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'name' not in body:
        raise APIException('You need to specify the name of the planet', status_code=400)
        
    # at this point, all data has been validated, we can proceed to inster into the bd
    new_planet = Planet(name=body['name'])
    db.session.add(new_planet)
    db.session.commit()
    return "Planet created successfully ;) ", 200


@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favourites(user_id):
    my_user = User.get_user(user_id)
    favs = list(map(lambda x: x.serialize(), my_user.fav_planet))
    return jsonify(favs), 200


@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_just_one_planet(planet_id):
    planet = Planet.query.get(planet_id)
    return jsonify(planet.serialize()), 200


@app.route('/character', methods=['GET'])
def get_all_character():
    character_query = Character.query.all()
    all_character = list(map(lambda x: x.serialize(), character_query))
    return jsonify(all_character), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_just_one_character(character_id):
    character = Character.query.get(character_id)
    return jsonify(character.serialize()), 200

    
    

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
