from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime


#Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

#Import for Secretes Module (given by python)
import secrets

#Imports for Flask_login
from flask_login import UserMixin, LoginManager

#Import for Flask-Marshmallow
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = "")
    last_name = db.Column(db.String(150), nullable = True, default = "")
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = "")
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = "", unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    poke = db.relationship('Poke', backref = 'owner', lazy = True)


    def __init__(self, email, first_name = "", last_name = "", id = "", password =  "", token = "", g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email 
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f"User {self.email} has been added to the database."


class Poke(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(250), nullable = True)
    type_ = db.Column(db.String(50), nullable = False)
    pokedex_number = db.Column(db.String(10), nullable = False)
    weight = db.Column(db.String(100))
    height = db.Column(db.String(100))
    ability = db.Column(db.String(100))
    gen_of_release = db.Column(db.String(150))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, name, description, type_, pokedex_number, weight, height, ability, gen_of_release, user_token, id = ""):
        self.id = self.set_id()
        self.name = name
        self.description = description 
        self.type_ = type_
        self.pokedex_number = pokedex_number
        self.weight = weight
        self.height = height 
        self.ability = ability 
        self.gen_of_release = gen_of_release
        self.user_token = user_token

    def __repr__(self):
        return f"The following pokemon has been added: {self.name}"

    def set_id(self):
        return(secrets.token_urlsafe())

class PokeSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'type_', 'weight', 'height', 'pokedex_number', 'gen_of_release', 'ability']

poke_schema = PokeSchema()
pokes_schema = PokeSchema(many = True)