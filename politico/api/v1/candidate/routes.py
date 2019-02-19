from flask import Blueprint, make_response, jsonify, request
from politico.api.v1.candidate.model import Candidate
from politico.api.v1.candidate.model import CandidateTable
from politico.api.v1.office.model import OfficeTable
from politico.api.v1.party.model import PartyTable
from politico.api.v1.user.model import UserTable

cand = Blueprint('cand', __name__)

cand_table = CandidateTable()
user_table = UserTable()
party_table = PartyTable()
office_table = OfficeTable()

@cand.route('/candidates', methods=['POST'])
def add_candidate():
    cand_data = request.get_json()
    msg = validate_candidate_info(cand_data)
    if msg != 'ok':
        return make_response(jsonify({
            'status':400, 
            'error': msg
        }), 400)
    else:
        cand = cand_table.get_candidate_by_candidate(cand_data.get('candidate'))
        if not cand:
            added_cand = cand_table.add_candidate(cand_data)
            return make_response(jsonify({
                'status': 200, 
                'data': [added_cand]
            }), 200)
        else:
            return make_response(jsonify({
                'status': 409, 
                'error': 'candidate with this id already exists'
            }), 409)


def validate_candidate_info(cand):
    user = user_table.users.get(cand.get('candidate'))
    office = office_table.offices.get(cand.get('office'))
    party = party_table.parties.get(cand.get('party'))
    msg = None
    if not cand:
        msg = 'candidate information is required'
    elif 'office' not in cand:
        msg = 'office missing'
    elif 'party' not in cand:
        msg = 'party missing'
    elif 'candidate' not in cand:
        msg = 'candidate id missing'
    elif not (str(cand['office'])).isdigit() or not (str(cand['party'])).isdigit() or not (str(cand['candidate'])).isdigit():
        msg = 'all field should be of integer type'
    elif not user:
        msg = 'No user exists with that ID'
    elif not office:
        msg =  'Office does not exists'
    elif not party:
        msg = 'Party does not exist'
    else:
        msg = 'ok'
    return msg