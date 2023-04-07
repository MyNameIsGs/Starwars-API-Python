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
from models import db, User, Character, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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
def get_user():

    users= User.query.all()
    users_list=[]
    for user in users:
        users_list.append(user.serialize())

    return jsonify(users_list), 200

@app.route('/user', methods=['POST'])
def post_user():

    body= request.json
    email= body.get("email",None)
    password= body.get("password",None)

    if email is None or password is None:
       return jsonify({"Message":"Email or Password is not valid"}), 400

    else:
        try:
            user=User(email=email,password=password)
            db.session.add(user)
            db.session.commit()
            return jsonify({"Message":"User Registered"})

        except Exception as error:
                return jsonify(error.args[0]),error.args[1]

@app.route('/characters', methods=['POST'])
def post_characters():

    body= request.json
    name= body.get("name",None)
    birthday= body.get("birthday",None)
    color_eyes= body.get("color_eyes",None)
    color_hair= body.get("color_hair",None)
    tone_skin= body.get("tone_skin",None)

    if name is None or birthday is None or color_eyes is None or color_hair is None or tone_skin is None:
        return jsonify({"Message":"Data not found"}), 400

    else:
        try:
            character=Character(name=name, birthday=birthday, color_eyes=color_eyes, color_hair=color_hair, tone_skin=tone_skin)
            db.session.add(character)
            db.session.commit()
            return jsonify({"Message":"Character Added"})

        except Exception as error:
                return jsonify(error.args[0]),error.args[1]

@app.route('/planets', methods=['POST'])
def post_planets():


    body= request.json
    name= body.get("name",None)
    poblation= body.get("poblation",None)
    diameter= body.get("diameter",None)
    climate= body.get("climate",None)
    

    if name is None or poblation is None or diameter is None or climate is None:
        return jsonify({"Message":"Data not found"}), 400

    else:
        try:
            planets=Planets(name=name, poblation=poblation, diameter=diameter, climate=climate)
            db.session.add(planets)
            db.session.commit()
            return jsonify({"Message":"Planet Added"})

        except Exception as error:
                return jsonify(error.args[0]),error.args[1]


@app.route('/characters', methods=['GET'])
def get_character():

    characters= Character.query.all()
    characters_list=[]
    for character in characters:
        characters_list.append(character.serialize())
        
@app.route('/planets', methods=['GET'])
def get_planet():

    planets= Planets.query.all()
    planets_list=[]
    for planet in planets:
        planets_list.append(planet.serialize())

    return jsonify(planets_list), 200

@app.route('/user/favorites/<int:id>', methods=["GET"])
def get_favorites(id):

    favorites= Favorites.query.filter_by(user_id=id)
    print(favorites)
    favorites_list=[]
    for favorite in favorites:
        favorites_list.append(favorite.serialize())

    return jsonify([fav.serialize() for fav in favorites]), 200

@app.route('/user/favorites/<int:character_id>/<int:user_id>', methods=["POST"])
def post_favorite_character(user_id, character_id):

    body= request.json
    name= body.get("name",None)
    favorites= Favorites.query.filter_by(user_id=user_id, character_id=character_id).first()

    if favorites is not None:
        return jsonify ({"Message":"Already in Favorites"})
    
    else:
        try:
            newFavorite=Favorites(name=name, character_id=character_id, user_id=user_id)
            db.session.add(newFavorite)
            db.session.commit()
            return jsonify({"Message":"Character Added"})

        except Exception as error:
                return jsonify(error.args[0])

@app.route('/user/favorites/<int:planets_id>/<int:user_id>', methods=["POST"])
def post_favorite_planet(user_id, planets_id):

    body= request.json
    name= body.get("name",None)
    favorites= Favorites.query.filter_by(user_id=user_id, planets_id=planets_id).first()

    if favorites is not None:
        return jsonify ({"Message":"Already in Favorites"})
    
    else:
        try:
            newFavorite=Favorites(name=name, planets_id=planets_id, user_id=user_id)
            db.session.add(newFavorite)
            db.session.commit()
            return jsonify({"Message":"Planet Added"})

        except Exception as error:
                return jsonify(error.args[0])
  
  


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
