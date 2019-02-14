from flask import Blueprint, make_response, jsonify, request
from politico.api.v2.petition.model import PetitionTable
from politico.api.v2.office.model import OfficeTable
from politico.api.v2.users.model import UserTable

petition = Blueprint('petitions', __name__)

petition_tb = PetitionTable()
user_tb = UserTable()
office_tb = OfficeTable()

@petition.route('/petitions', methods=['POST'])
def add_petition():
    petition_data = request.get_json()
    print(petition_data)
    msg = validate_petition_info(petition_data)
    if msg != 'ok':
        return make_response(jsonify({
            'status':400, 
            'error': msg
        }), 400)
    else:
        petition = petition_tb.get_one_petition(petition_data.get('petition'))
        if not petition:
            added_petition = petition_tb.create_petition(petition_data)
            return make_response(jsonify({
                'status': 200, 
                'data': [added_petition]
            }), 200)
        else:
            return make_response(jsonify({
                'status': 409, 
                'error': 'cannot petition twice'
            }), 409)


@petition.route('/petitions', methods = ['GET'])
def get_petitions():
    return make_response(jsonify({
        'status': 200, 
        'data': petition_tb.get_petitions()
    }), 200)

@petition.route('/petitions/<int:id>', methods=['GET'])
def get_one_petition(id):
    petition = petition_tb.get_one_petition(id)
    if not petition:
        return make_response(jsonify({
            'status': 404,
            'error': 'No petition with id:{} found'.format(id)
        }), 404)
    else:
        return make_response(jsonify({
            'status': 200, 
            'data': [petition]
        }), 200)


@petition.route('/petitions/<int:id>', methods=['PATCH'])
def update_petition(id):
    existing_petition = petition_tb.get_one_petition(id)
    if not existing_petition:
        return make_response(jsonify({
            'status': 404, 
            'error' : 'petition with id:{} does not exist'.format(id)
        }), 404)
        
    petition_data = request.get_json()
    msg = validate_petition_info(petition_data)
    if msg != 'ok':
        return make_response(jsonify({
            'status':400, 
            'error': msg
        }), 400)

    updated_petition = petition_tb.update_petition(id, petition_data)
    return make_response(jsonify({
        'status': 200, 
        'data': [updated_petition]
    }), 200)
    
@petition.route('/petitions/<int:id>', methods=['DELETE'])
def delete_petition(id):
    existing_petition = petition_tb.get_one_petition(id)
    if not existing_petition:
        return make_response(jsonify({
            'status': 404, 
            'error' : 'petition with id:{} does not exist'.format(id)
        }), 404)
    else:
        if petition_tb.delete_petition(id):
            return make_response(jsonify({
                'status': 200, 
                'data' : {
                    'message' : 'petition successfully deleted'
                }
            }), 200)
        else:
            return make_response(jsonify({
                'status': 500, 
                'error' : 'Could not delete petition with id:{}'.format(id)
            }), 500)



def validate_petition_info(petition):
    user = user_tb.get_single_user(petition['created_by'])
    office = office_tb.get_one_office(petition['office'])

    msg = None
    if not petition:
        msg = 'petition information is required'
    elif 'created_by' not in petition:
        msg = 'user missing'
    elif 'office' not in petition:
        msg = 'office id missing'
    elif not isinstance(petition['created_by'], int) or not isinstance(petition['office'], int):
        msg = 'all field should be of integer type'
    elif not user:
        msg = 'User does not exist'
    elif not office:
        msg =  'Office does not exist'
    else:
        msg = 'ok'
    return msg