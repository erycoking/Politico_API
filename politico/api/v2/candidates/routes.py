from flask import Blueprint, make_response, jsonify, request
from politico.api.v2.candidates.model import CandidateTable
from politico.api.v2.office.model import OfficeTable
from politico.api.v2.party.model import PartyTable
from politico.api.v2.users.model import UserTable

from politico.api.v2.auth.authentication import token_required

import re

cand = Blueprint('candidates', __name__)

cand_tb = CandidateTable()
user_tb = UserTable()
party_tb = PartyTable()
office_tb = OfficeTable()

@cand.route('/office/<int:office_id>/register', methods=['POST'])
@token_required
def add_candidate(current_user, office_id):
    cand_data = request.get_json()
    msg = validate_candidate_info(cand_data)
    if msg != 'ok':
        return make_response(jsonify({
            'status':400, 
            'error': msg
        }), 400)
    else:
        cand = cand_tb.get_one_candidate_by_user(office_id, current_user.get('id'))
        if not cand:
            cand_data['candidate'] = current_user.get('id')
            added_cand = cand_tb.create_candidate(office_id, cand_data)
            if 'error' in added_cand:
                return make_response(jsonify({
                    'status':400, 
                    'error': added_cand['error']
                }), 400)
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
@token_required
def get_candidates(current_user, office_id):
    return make_response(jsonify({
        'status': 200, 
        'data': cand_tb.get_candidates(office_id)
    }), 200)

@cand.route('/office/<int:office_id>/candidates/<int:id>', methods=['GET'])
@token_required
def get_one_candidate(current_user, office_id, id):
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
@token_required
def update_candidate(current_user, office_id, id):
    existing_candidate = cand_tb.get_one_candidate(office_id, id)
    if not existing_candidate:
        return make_response(jsonify({
            'status': 404, 
            'error' : 'candidate with id:{} does not exist'.format(id)
        }), 404)
        
    cand_data = request.get_json()
    msg = validate_candidate_info(cand_data)
    if msg != 'ok':
        return make_response(jsonify({
            'status':400, 
            'error': msg
        }), 400)

    cand_data['candidate'] = id
    updated_candidate = cand_tb.update_candidate(office_id, id, cand_data)
    if 'error' in updated_candidate:
        return make_response(jsonify({
            'status':400, 
            'error': updated_candidate['error']
        }), 400)
    return make_response(jsonify({
        'status': 200, 
        'data': [updated_candidate]
    }), 200)
    
@cand.route('/office/<int:office_id>/candidates/<int:id>', methods=['DELETE'])
@token_required
def delete_candidate(current_user, office_id, id):
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
                'status': 400, 
                'error' : 'update or delete on table "candidates" violates foreign key constraint.\nKey (id)=({}) is referenced on another table'.format(id)
            }), 400)



def validate_candidate_info(cand):
    msg = None
    if 'party' not in cand:
        msg = 'party missing'
    elif not (str(cand['party'])).isdigit():
        msg = 'all field should be of integer type'
    elif not party_tb.get_one_party(cand['party']):
        msg = 'Party does not exist'
    else:
        msg = 'ok'
    return msg