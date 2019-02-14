from flask import Blueprint, make_response, jsonify, request
from politico.api.v2.candidates.model import CandidateTable
from politico.api.v2.office.model import OfficeTable
from politico.api.v2.vote.model import VotesTable
from politico.api.v2.users.model import UserTable

vote = Blueprint('votes', __name__)

votes_tb = VotesTable()
cand_tb = CandidateTable()
user_tb = UserTable()
office_tb = OfficeTable()

@vote.route('/votes', methods=['POST'])
def add_vote():
    vote_data = request.get_json()
    msg = validate_vote_info(vote_data)
    if msg != 'ok':
        return make_response(jsonify({
            'status':400, 
            'error': msg
        }), 400)
    else:
        vote = votes_tb.get_one_vote_created_by(vote_data.get('created_by'))
        if not vote:
            added_vote = votes_tb.create_vote(vote_data)
            return make_response(jsonify({
                'status': 200, 
                'data': [added_vote]
            }), 200)
        else:
            return make_response(jsonify({
                'status': 409, 
                'error': 'cannot vote twice'
            }), 409)


@vote.route('/votes', methods = ['GET'])
def get_votes():
    return make_response(jsonify({
        'status': 200, 
        'data': votes_tb.get_votes()
    }), 200)

@vote.route('/votes/<int:id>', methods=['GET'])
def get_one_vote(id):
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
def update_vote(id):
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

    updated_vote = votes_tb.update_vote(id, vote_data)
    return make_response(jsonify({
        'status': 200, 
        'data': [updated_vote]
    }), 200)
    
@vote.route('/votes/<int:id>', methods=['DELETE'])
def delete_vote(id):
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
                'status': 500, 
                'error' : 'Could not delete vote with id:{}'.format(id)
            }), 500)



def validate_vote_info(vote):
    user = user_tb.get_single_user(vote['created_by'])
    office = office_tb.get_one_office(vote['office'])
    candidate = cand_tb.get_one_candidate(vote['office'], vote['candidate'])
    msg = None
    if not vote:
        msg = 'vote information is required'
    elif 'candidate' not in vote:
        msg = 'candidate missing'
    elif 'office' not in vote:
        msg = 'office missing'
    elif 'created_by' not in vote:
        msg = 'user id missing'
    elif not isinstance(vote['created_by'], int) or not isinstance(vote['candidate'], int) or not isinstance(vote['office'], int):
        msg = 'all field should be of integer type'
    elif not user:
        msg = 'User does not exist'
    elif not office:
        msg =  'Office does not exist'
    elif not candidate:
        msg = 'candidate does not exist'
    else:
        msg = 'ok'
    return msg