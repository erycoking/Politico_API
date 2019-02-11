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
            return make_response(jsonify({
                'status': 200, 
                'data': [cand]
            }), 200)
        else:
            return make_response(jsonify({
                'status': 409, 
                'error': 'candidate with this id already exists'
            }), 409)


def validate_candidate_info(cand):
    candidate = cand_table.get_single_candidate(cand.get('candidate'))
    office = office_table.get_single_office(cand.get('office'))
    party = party_table.get_single_party(cand.get('party'))
    msg = None
    if not cand:
        msg = 'candidate information is required'
    elif 'office' not in cand:
        msg = 'office missing'
    elif 'party' not in cand:
        msg = 'party missing'
    elif 'candidate' not in cand:
        msg = 'candidate id missing'
    elif not isinstance(cand['office'], int) or not isinstance(cand['party'], int) or not isinstance(cand['candidate'], int):
        msg = 'all field should be of integer type'
    elif not candidate:
        msg = 'No candidate exists with that ID'
    elif not office:
        msg =  'Office does not exists'
    elif not party:
        msg = 'Party does not exist'
    else:
        msg = 'ok'
    return msg