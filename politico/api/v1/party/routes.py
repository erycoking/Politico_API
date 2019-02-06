from flask import Blueprint, request, make_response, jsonify
from politico.api.v1.party.modal import partyTable

party = Blueprint('party', __name__)

party_table = partyTable()

@party.route('/parties', methods = ['GET'])
def get_parties():
    # route for displaying all parties
    return make_response(jsonify({
        'status': 200, 
        'data': party_table.get_all_parties()
    }), 200)

@party.route('/parties/<int:id>', methods=['GET'])
def get_one_party(id):
    # route for getting a single party
    party = party_table.get_single_party(id)
    if not party:
        return make_response(jsonify({
            'status': 404,
            'error': 'No party with id:{} found'.format(id)
        }), 404)
    else:
        return make_response(jsonify({
            'status': 200, 
            'data': [party.party_data]
        }), 200)

@party.route('/parties', methods=['POST'])
def add_party():
    # route for adding a party
    party_data = request.get_json()
    msg = validateKeysInParty(party_data)
    if msg != 'ok':
        return make_response(jsonify({
            'status': 406,
            'error': msg
        }), 406)
    
    msg1 = validateValueInParty(party_data)
    if msg1 != 'ok':
        return make_response(jsonify({
            'status': 406,
            'error': msg1
        }), 406)

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
            'status': 406,
            'error': msg
        }), 406)
    
    msg1 = validateValueInParty(party_data)
    if msg1 != 'ok':
        return make_response(jsonify({
            'status': 406,
            'error': msg1
        }), 406)

    existing_party = party_table.get_single_party(id)
    if not existing_party:
        return make_response(jsonify({
            'status': 404, 
            'error' : 'Party with id:{} does not exist'.format(id)
        }), 404)
    else:
        updated_party = party_table.update_party(id, party_data)
        return make_response(jsonify({
            'status': 202, 
            'data': [updated_party]
        }), 202)
    
@party.route('/parties/<int:id>', methods=['DELETE'])
def delete_party(id):
    existing_party = party_table.get_single_party(id)
    if not existing_party:
        return make_response(jsonify({
            'status': 404, 
            'error' : 'Party with id:{} does not exist'.format(id)
        }), 404)
    else:
        if party_table.delete_party(id):
            return make_response(jsonify({
                'status': 202, 
                'data' : {
                    'message' : 'Party successfully deleted'
                }
            }), 202)
        else:
            return make_response(jsonify({
                'status': 500, 
                'error' : 'Could not delete party with id:{}'.format(id)
            }), 500)



def validateKeysInParty(Party):
    # function for validating party keys
    if not Party:
        return 'No Party found'
    elif 'name' not in Party:
        return 'name missing'
    elif 'hqAddress' not in Party:
        return 'hqAddress missing'
    elif 'logoUrl' not in Party:
        return 'logoUrl missing'
    else:
        return 'ok'

def validateValueInParty(Party):
    # function for validating party input values 
    if not Party['name'] or len(Party['name']) < 3:
        return 'Invalid name.\nName must be longer than 2 characters'
    elif not Party['hqAddress'] or len(Party['hqAddress']) < 3:
        return 'Invalid hqAddress.\nHqAddress must be longer than 2 characters'
    elif not Party['logoUrl'] or len(Party['logoUrl']) < 3:
        return 'Invalid logoUrl.\nLogoUrl must be longer than 2 characters'
    else:
        return 'ok'
