from flask import Blueprint, request, jsonify
from Poke_inventory.helpers import token_required 
from Poke_inventory.models import db, User, Poke, poke_schema, pokes_schema 


api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return {'some':'value'}

#CREATE POKEMON ENDPOINT
@api.route('/pokes', methods = ['POST'])
@token_required
def create_poke(current_user_token):
    name = request.json['name']
    description = request.json['description']
    type_ = request.json['type_']
    weight = request.json['weight']
    height = request.json['height']
    pokedex_number = request.json['pokedex_number']
    gen_of_release = request.json['gen_of_release']
    ability = request.json['ability']
    user_token = current_user_token.token

    print(f"BIG TESTER: {current_user_token.token}")

    poke = Poke(name, description, type_, weight, height, pokedex_number, gen_of_release, ability, user_token = user_token )

    db.session.add(poke)
    db.session.commit()

    response = poke_schema.dump(poke)

    return jsonify(response)

    #Retrieve all Poke Endpoints

@api.route('/pokes', methods = ['GET'])
@token_required
def get_pokes(current_user_token):
    owner = current_user_token.token
    pokes = Poke.query.filter_by(user_token = owner).all()
    response = pokes_schema.dump(pokes)
    return jsonify(response)

#Retrieve ONE Pokemon Endpoint
@api.route('/pokes/<id>', methods = ['GET'])
@token_required
def get_poke(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        poke = Poke.query.get(id)
        response = poke_schema.dump(poke)
        return jsonify(response)
    else: 
        return jsonify({'message': 'Valid Token Required'}), 401

#Update Pokemon
@api.route('/pokes/<id>', methods = ['POST', 'PUT'])
@token_required
def update_poke(current_user_token, id):
    poke = Poke.query.get(id)

    poke.name = request.json['name']
    poke.description = request.json['description']
    poke.type_ = request.json['type_']
    poke.weight = request.json['weight']
    poke.height = request.json['height']
    poke.pokedex_number = request.json['pokedex_number']
    poke.gen_of_release = request.json['gen_of_release']
    poke.ability = request.json['ability']
    poke.user_token = current_user_token.token

    db.session.commit()
    response = poke_schema.dump(poke)
    return jsonify(response)

#Delete Pokemon
@api.route('/pokes/<id>', methods=['DELETE'])
@token_required
def delete_poke(current_user_token, id):
    poke = Poke.query.get(id)
    db.session.delete(poke)
    db.session.commit()
    response = poke_schema.dump(poke)
    return jsonify(response)