from flask import Blueprint, request, make_response, jsonify
from politico.api.v2.party.model import PartyTable
from politico.api.v1.party.routes import validateKeysInParty
from politico.api.v1.party.routes import validateValueInParty

party = Blueprint('party_2', __name__)

party_tb = PartyTable()

@party.route('/parties', methods = ['GET'])
def get_parties():
    return make_response(jsonify({
        'status': 200, 
        'data': party_tb.get_parties()
    }), 200)

@party.route('/parties/<int:id>', methods=['GET'])
def get_one_party(id):
    party = party_tb.get_one_party(id)
    if not party:
        return make_response(jsonify({
            'status': 404,
            'error': 'No party with id:{} found'.format(id)
        }), 404)
    else:
        return make_response(jsonify({
            'status': 200, 
            'data': [party]
        }), 200)

@party.route('/parties', methods=['POST'])
def add_party():
    party_data = request.get_json()
    msg = validateKeysInParty(party_data)
    if msg != 'ok':
        return make_response(jsonify({
            'status': 400,
            'error': msg
        }), 400)
    
    msg1 = validateValueInParty(party_data)
    if msg1 != 'ok':
        return make_response(jsonify({
            'status': 400,
            'error': msg1
        }), 400)

    party_exists = party_tb.get_one_party_by_name(party_data['name'])
    if not party_exists:
        added_party = party_tb.create_party(party_data)
        return make_response(jsonify({
            'status': 201,
            'data': [added_party]
        }), 201)
    else:
        return make_response(jsonify({
            'status': 409, 
            'error': 'Party with name::{} already exists'.format(party_data['name'])
        }), 409)

@party.route('/parties/<int:id>', methods=['PATCH'])
def update_party(id):
    existing_party = party_tb.get_one_party(id)
    if not existing_party:
        return make_response(jsonify({
            'status': 404, 
            'error' : 'Party with id:{} does not exist'.format(id)
        }), 404)
        
    party_data = request.get_json()
    msg = validateKeysInParty(party_data)
    if msg != 'ok':
        return make_response(jsonify({
            'status': 400,
            'error': msg
        }), 400)
    
    msg1 = validateValueInParty(party_data)
    if msg1 != 'ok':
        return make_response(jsonify({
            'status': 400,
            'error': msg1
        }), 400)

    updated_party = party_tb.update_party(id, party_data)
    return make_response(jsonify({
        'status': 200, 
        'data': [updated_party]
    }), 200)
    
@party.route('/parties/<int:id>', methods=['DELETE'])
def delete_party(id):
    existing_party = party_tb.get_one_party(id)
    if not existing_party:
        return make_response(jsonify({
            'status': 404, 
            'error' : 'Party with id:{} does not exist'.format(id)
        }), 404)
    else:
        if party_tb.delete_party(id):
            return make_response(jsonify({
                'status': 200, 
                'data' : {
                    'message' : 'Party successfully deleted'
                }
            }), 200)
        else:
            return make_response(jsonify({
                'status': 500, 
                'error' : 'Could not delete party with id:{}'.format(id)
            }), 500)


