from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    fav_planet = db.relationship('Planet')
    fav_char = db.relationship('Character')
    
    def __repr__(self):
         return f"{self.username}"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "active": self.is_active, 
            "fav_planet": list(map(lambda x: x.serialize(), self.fav_planet)),
            "fav_char": list(map(lambda x: x.serialize(), self.fav_char))
        }

    @classmethod
    def get_user(cls, id):
        user = cls.query.get(id)
        return user

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "affiliations": self.affiliations
        }