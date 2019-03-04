from flask import Blueprint, request, make_response, jsonify
from politico.api.v1.party.model import PartyTable

import re

party = Blueprint('party', __name__)

party_table = PartyTable()

@party.route('/parties', methods = ['GET'])
def get_parties():
    # route for displaying all parties
    return make_response(jsonify({
        'status': 200, 
        'data': party_table.parties
    }), 200)

@party.route('/parties/<int:id>', methods=['GET'])
def get_one_party(id):
    # route for getting a single party
    party = party_table.parties.get(id)
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
    # route for adding a party
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

    party_exists = party_table.get_single_party_by_name(party_data['name'])
    if not party_exists:
        added_party = party_table.add_party(party_data)
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
    # route for updating a party
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

    existing_party = party_table.parties.get(id)
    if not existing_party:
        return make_response(jsonify({
            'status': 404, 
            'error' : 'Party with id:{} does not exist'.format(id)
        }), 404)
    else:
        updated_party = party_table.update_party(id, party_data)
        return make_response(jsonify({
            'status': 200, 
            'data': [updated_party]
        }), 200)
    
@party.route('/parties/<int:id>', methods=['DELETE'])
def delete_party(id):
    existing_party = party_table.parties.get(id)
    if not existing_party:
        return make_response(jsonify({
            'status': 404, 
            'error' : 'Party with id:{} does not exist'.format(id)
        }), 404)
    else:
        if party_table.delete_party(id):
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



def validateKeysInParty(Party):
    # function for validating party keys
    msg = None
    if not Party:
        msg = 'No Party found'
    elif 'name' not in Party:
        msg = 'name missing'
    elif 'hq_address' not in Party:
        msg = 'hq_address missing'
    elif 'logo_url' not in Party:
        msg = 'logo_url missing'
    else:
        msg = 'ok'
    return msg

def validateValueInParty(Party):
    # function for validating party input values 
    image_url_pattern = re.compile(r'^https?://(www\.)?(\w+)(\.\w+)/(\w+/)*.*$')
    address_pattern = re.compile(r'[a-zA-Z0-9]{2,25}([.,]?( [a-zA-Z0-9]{2,25})*.?)*')
    name_url = re.compile(r'[A-Za-z]{2,25}( [A-Za-z]{2,25})*')
    msg = None
    if not re.fullmatch(name_url, Party['name']) or len(Party['name']) < 3:
        msg = 'Invalid name.Name should not be less than 3 characters and should contain only alphabets'
    elif not re.fullmatch(address_pattern, Party['hq_address']) or len(Party['hq_address']) < 3:
        msg = 'Invalid hq_address.hq_address cannot be less than 3 characters and should contain only alphanumerics.'
    elif not re.fullmatch(image_url_pattern, Party['logo_url']):
        msg = 'Invalid logo_url.Please give a valid url'
    else:
        msg = 'ok'

    return msg
