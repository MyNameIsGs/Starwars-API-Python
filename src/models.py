from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
   

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    birthday = db.Column(db.String(80), nullable=False)
    color_eyes = db.Column(db.String(50), nullable=False)
    color_hair = db.Column(db.String(50), nullable=False)
    tone_skin = db.Column(db.String(50), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birthday": self.birthday,
            "color_eyes": self.color_eyes,
            "color_hair": self.color_hair,
            "tone_skin": self.tone_skin
        }

class Planets(db.Model):
    
  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    poblation = db.Column(db.String(250))
    diameter = db.Column(db.String(250))
    climate = db.Column(db.String(250))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "poblation": self.poblation,
            "diameter": self.diameter,
            "climate": self.climate
            
        }

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    character_id = db.Column(db.Integer, ForeignKey("character.id"))
    planets_id = db.Column(db.Integer, ForeignKey("planets.id"))
    user_id = db.Column(db.Integer, ForeignKey("user.id"))

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "character_id": self.character_id,
            "planets_id": self.planets_id,
            "user_id": self.user_id
        }