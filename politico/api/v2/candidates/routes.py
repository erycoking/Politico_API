from flask import Blueprint, make_response, jsonify, request
from politico.api.v2.candidates.model import CandidateTable
from politico.api.v2.office.model import OfficeTable
from politico.api.v2.party.model import PartyTable
from politico.api.v2.users.model import UserTable

cand = Blueprint('candidates', __name__)

cand_tb = CandidateTable()
user_tb = UserTable()
party_tb = PartyTable()
office_tb = OfficeTable()

@cand.route('/office/<int:office_id>/register', methods=['POST'])
def add_candidate(office_id):
    cand_data = request.get_json()
    msg = validate_candidate_info(office_id, cand_data)
    if msg != 'ok':
        return make_response(jsonify({
            'status':400, 
            'error': msg
        }), 400)
    else:
        cand = cand_tb.get_one_candidate_by_user(office_id, cand_data.get('candidate'))
        if not cand:
            added_cand = cand_tb.create_candidate(office_id, cand_data)
            return make_response(jsonify({
                'status': 200, 
                'data': [added_cand]
            }), 200)
        else:
            return make_response(jsonify({
                'status': 409, 
                'error': 'candidate with this id already exists'
            }), 409)


@cand.route('/office/<int:office_id>/candidates', methods = ['GET'])
def get_candidates(office_id):
    return make_response(jsonify({
        'status': 200, 
        'data': cand_tb.get_candidates(office_id)
    }), 200)

@cand.route('/office/<int:office_id>/candidates/<int:id>', methods=['GET'])
def get_one_candidate(office_id, id):
    candidate = cand_tb.get_one_candidate(office_id, id)
    if not candidate:
        return make_response(jsonify({
            'status': 404,
            'error': 'No candidate with id:{} found'.format(id)
        }), 404)
    else:
        return make_response(jsonify({
            'status': 200, 
            'data': [candidate]
        }), 200)


@cand.route('/office/<int:office_id>/candidates/<int:id>', methods=['PATCH'])
def update_candidate(office_id, id):
    existing_candidate = cand_tb.get_one_candidate(office_id, id)
    if not existing_candidate:
        return make_response(jsonify({
            'status': 404, 
            'error' : 'candidate with id:{} does not exist'.format(id)
        }), 404)
        
    cand_data = request.get_json()
    msg = validate_candidate_info(office_id, cand_data)
    if msg != 'ok':
        return make_response(jsonify({
            'status':400, 
            'error': msg
        }), 400)

    updated_candidate = cand_tb.update_candidate(office_id, id, cand_data)
    return make_response(jsonify({
        'status': 200, 
        'data': [updated_candidate]
    }), 200)
    
@cand.route('/office/<int:office_id>/candidates/<int:id>', methods=['DELETE'])
def delete_candidate(office_id, id):
    existing_candidate = cand_tb.get_one_candidate(office_id, id)
    if not existing_candidate:
        return make_response(jsonify({
            'status': 404, 
            'error' : 'candidate with id:{} does not exist'.format(id)
        }), 404)
    else:
        if cand_tb.delete_candidate(office_id, id):
            return make_response(jsonify({
                'status': 200, 
                'data' : {
                    'message' : 'candidate successfully deleted'
                }
            }), 200)
        else:
            return make_response(jsonify({
                'status': 500, 
                'error' : 'Could not delete candidate with id:{}'.format(id)
            }), 500)



def validate_candidate_info(office_id, cand):
    user = user_tb.get_single_user(cand['candidate'])
    office = office_tb.get_one_office(office_id)
    party = party_tb.get_one_party(cand['party'])
    msg = None
    if not cand:
        msg = 'candidate information is required'
    elif 'party' not in cand:
        msg = 'party missing'
    elif 'candidate' not in cand:
        msg = 'candidate id missing'
    elif not isinstance(cand['party'], int) or not isinstance(cand['candidate'], int):
        msg = 'all field should be of integer type'
    elif not user:
        msg = 'You have to be registered as citizen before you become a candidate'
    elif not office:
        msg =  'Office does not exists'
    elif not party:
        msg = 'Party does not exist'
    else:
        msg = 'ok'
    return msg