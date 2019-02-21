from flask import Blueprint, make_response, jsonify, request
from politico.api.v2.candidates.model import CandidateTable
from politico.api.v2.office.model import OfficeTable
from politico.api.v2.vote.model import VotesTable
from politico.api.v2.users.model import UserTable

from politico.api.v2.auth.authentication import token_required, is_admin

vote = Blueprint('votes', __name__)

votes_tb = VotesTable()
cand_tb = CandidateTable()
user_tb = UserTable()
office_tb = OfficeTable()

@vote.route('/votes', methods=['POST'])
@token_required
def add_vote(current_user):
    vote_data = request.get_json()
    msg = validate_vote_info(vote_data)
    if msg != 'ok':
        return make_response(jsonify({
            'status':400, 
            'error': msg
        }), 400)
    else:
        vote = votes_tb.get_one_vote_created_by_and_office(current_user['id'], vote_data['office'])
        if not vote:
            vote_data['created_by'] = current_user['id']
            added_vote = votes_tb.create_vote(vote_data)
            print(added_vote)
            if 'error' in added_vote:
                return make_response(jsonify({
                    'status':400, 
                    'error': added_vote['error']
                }), 400)
            return make_response(jsonify({
                'status': 200, 
                'data': [added_vote]
            }), 200)
        else:
            return make_response(jsonify({
                'status': 409, 
                'error': 'cannot vote twice for the same office'
            }), 409)


@vote.route('/votes', methods = ['GET'])
@token_required
def get_votes(current_user):
    return make_response(jsonify({
        'status': 200, 
        'data': votes_tb.get_votes()
    }), 200)

@vote.route('/votes/<int:id>', methods=['GET'])
@token_required
def get_one_vote(current_user, id):
    vote = votes_tb.get_one_vote(id)
    if not vote:
        return make_response(jsonify({
            'status': 404,
            'error': 'No vote with id:{} found'.format(id)
        }), 404)
    else:
        return make_response(jsonify({
            'status': 200, 
            'data': [vote]
        }), 200)


@vote.route('/votes/<int:id>', methods=['PATCH'])
@token_required
def update_vote(current_user, id):
    is_admin(current_user)
    existing_vote = votes_tb.get_one_vote(id)
    if not existing_vote:
        return make_response(jsonify({
            'status': 404, 
            'error' : 'vote with id:{} does not exist'.format(id)
        }), 404)
        
    vote_data = request.get_json()
    msg = validate_vote_info(vote_data)
    if msg != 'ok':
        return make_response(jsonify({
            'status':400, 
            'error': msg
        }), 400)

    vote_data['created_by'] = current_user['id']
    updated_vote = votes_tb.update_vote(id, vote_data)
    if 'error' in updated_vote:
        return make_response(jsonify({
            'status':400, 
            'error': updated_vote['error']
        }), 400)
    return make_response(jsonify({
        'status': 200, 
        'data': [updated_vote]
    }), 200)
    
@vote.route('/votes/<int:id>', methods=['DELETE'])
@token_required
def delete_vote(current_user, id):
    is_admin(current_user)
    existing_vote = votes_tb.get_one_vote(id)
    if not existing_vote:
        return make_response(jsonify({
            'status': 404, 
            'error' : 'vote with id:{} does not exist'.format(id)
        }), 404)
    else:
        if votes_tb.delete_vote(id):
            return make_response(jsonify({
                'status': 200, 
                'data' : {
                    'message' : 'vote successfully deleted'
                }
            }), 200)
        else:
            return make_response(jsonify({
                'status': 400, 
                'error' : 'update or delete on table "vote" violates foreign key constraint.\nKey (id)=({}) is referenced on another table'.format(id)
            }), 400)



def validate_vote_info(vote):
    office = office_tb.get_one_office(vote['office'])
    candidate = cand_tb.get_one_candidate(vote['office'], vote['candidate'])
    msg = None
    if not vote:
        msg = 'vote information is required'
    elif 'candidate' not in vote:
        msg = 'candidate missing'
    elif 'office' not in vote:
        msg = 'office missing'
    elif not (str(vote['candidate'])).isdigit() or not (str(vote['candidate'])).isdigit():
        msg = 'all field should be of integer type'
    elif not office:
        msg =  'Office does not exist'
    elif not candidate:
        msg = 'No candidate by id::{} is running for office with id::{}'.format(vote['candidate'], vote['office'])
    else:
        msg = 'ok'
    return msg