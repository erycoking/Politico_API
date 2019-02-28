from flask import Blueprint, request, make_response, jsonify
from politico.api.v2.party.model import PartyTable
from politico.api.v1.party.routes import validateKeysInParty
from politico.api.v1.party.routes import validateValueInParty

from politico.api.v2.auth.authentication import token_required

party = Blueprint('party_2', __name__)

party_tb = PartyTable()

@party.route('/parties', methods = ['GET'])
@token_required
def get_parties(current_user):
    return make_response(jsonify({
        'status': 200, 
        'data': party_tb.get_parties()
    }), 200)

@party.route('/parties/<int:id>', methods=['GET'])
@token_required
def get_one_party(current_user, id):
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
@token_required
def add_party(current_user):
    admin = bool(current_user['is_admin'])
    if not (admin):
        print("I am in")
        return make_response(jsonify({
                'status': 401,
                'error': 'Only admin can perform this function'
            }), 401)
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
        if 'error' in added_party:
            return make_response(jsonify({
                'status':400, 
                'error': added_party['error']
            }), 400)
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
@token_required
def update_party(current_user, id):
    admin = bool(current_user['is_admin'])
    if not (admin):
        print("I am in")
        return make_response(jsonify({
                'status': 401,
                'error': 'Only admin can perform this function'
            }), 401)
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
    if 'error' in updated_party:
        return make_response(jsonify({
            'status':400, 
            'error': updated_party['error']
        }), 400)
    return make_response(jsonify({
        'status': 200, 
        'data': [updated_party]
    }), 200)
    
@party.route('/parties/<int:id>', methods=['DELETE'])
@token_required
def delete_party(current_user, id):
    admin = bool(current_user['is_admin'])
    if not (admin):
        print("I am in")
        return make_response(jsonify({
                'status': 401,
                'error': 'Only admin can perform this function'
            }), 401)
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
                'status': 400, 
                'error' : 'update or delete on table "party" violates foreign key constraint.\nKey (id)=({}) is referenced on another table'.format(id)
            }), 400)



