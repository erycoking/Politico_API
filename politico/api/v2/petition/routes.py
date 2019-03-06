from flask import Blueprint, make_response, jsonify, request
from politico.api.v2.petition.model import PetitionTable
from politico.api.v2.office.model import OfficeTable
from politico.api.v2.users.model import UserTable

from politico.api.v2.auth.authentication import token_required

petition = Blueprint('petitions', __name__)

petition_tb = PetitionTable()
user_tb = UserTable()
office_tb = OfficeTable()

@petition.route('/petitions', methods=['POST'])
@token_required
def add_petition(current_user):
    petition_data = request.get_json()
    print(petition_data)
    msg = validate_petition_info(petition_data)
    if msg != 'ok':
        return make_response(jsonify({
            'status':400, 
            'error': msg
        }), 400)
    else:
        office = office_tb.get_one_office_by_name(petition_data['office'])
        petition = petition_tb.get_one_petition_by_created_by_and_office(current_user['id'], office['id'])
        if not petition:
            petition_data['created_by'] = current_user['id']
            added_petition = petition_tb.create_petition(petition_data)
            if 'error' in added_petition:
                return make_response(jsonify({
                    'status':400, 
                    'error': added_petition['error']
                }), 400)
            return make_response(jsonify({
                'status': 201, 
                'data': [added_petition]
            }), 201)
        else:
            return make_response(jsonify({
                'status': 409, 
                'error': 'cannot petition twice on the same office'
            }), 409)


@petition.route('/petitions', methods = ['GET'])
@token_required
def get_petitions(current_user):
    return make_response(jsonify({
        'status': 200, 
        'data': petition_tb.get_petitions()
    }), 200)

@petition.route('/petitions/<int:id>', methods=['GET'])
@token_required
def get_one_petition(current_user, id):
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
@token_required
def update_petition(current_user, id):
    admin = bool(current_user['is_admin'])
    if not (admin):
        print("I am in")
        return make_response(jsonify({
                'status': 401,
                'error': 'Only admin can perform this function'
            }), 401)
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

    petition_data['created_by'] = current_user['id']
    updated_petition = petition_tb.update_petition(id, petition_data)
    if 'error' in updated_petition:
        return make_response(jsonify({
            'status':400, 
            'error': updated_petition['error']
        }), 400)
    return make_response(jsonify({
        'status': 200, 
        'data': [updated_petition]
    }), 200)
    
@petition.route('/petitions/<int:id>', methods=['DELETE'])
@token_required
def delete_petition(current_user, id):
    admin = bool(current_user['is_admin'])
    if not (admin):
        print("I am in")
        return make_response(jsonify({
                'status': 401,
                'error': 'Only admin can perform this function'
            }), 401)
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
                    'message' : 'petition with id:{} successfully deleted'.format(id)
                }
            }), 200)
        else:
            return make_response(jsonify({
                'status': 400, 
                'error' : 'update or delete on table "petition" violates foreign key constraint.\nKey (id)=({}) is referenced on another table'.format(id)
            }), 400)



def validate_petition_info(petition):
    msg = None
    if not petition:
        msg = 'petition information is required'
    elif 'office' not in petition:
        msg = 'office missing'
    elif not (str(petition['office'])).isalpha():
        msg = 'Invalid Office name. Office name should be a string'
    elif not office_tb.get_one_office_by_name(petition['office']):
        msg =  'Office does not exist'
    else:
        msg = 'ok'
    return msg