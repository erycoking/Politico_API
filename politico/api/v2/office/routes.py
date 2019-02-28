from flask import Blueprint, request, make_response, jsonify
from politico.api.v2.office.model import OfficeTable
from politico.api.v1.office.route import validate_office_data

from politico.api.v2.auth.authentication import token_required

# blueprint
office = Blueprint('offices', __name__)

office_tb = OfficeTable()

@office.route('/offices', methods=['POST'])
@token_required
def create_office(current_user):
    admin = bool(current_user['is_admin'])
    if not (admin):
        print("I am in")
        return make_response(jsonify({
                'status': 401,
                'error': 'Only admin can perform this function'
            }), 401)
    office_data = request.get_json()
    msg = validate_office_data(office_data)
    if msg != 'ok':
        return make_response(jsonify({
            'status': 400, 
            'error': msg
        }), 400)
    else:
        existing_office = office_tb.get_one_office_by_name(office_data['name'])
        if not existing_office:
            created_office = office_tb.create_office(office_data)
            if 'error' in created_office:
                return make_response(jsonify({
                    'status':400, 
                    'error': created_office['error']
                }), 400)
            return make_response(jsonify({
                'status': 201, 
                'data': [created_office]
            }), 201)
        else:
            return make_response(jsonify({
                'status': 400,
                'error': 'office with name:{} already exists'.format(office_data['name'])
            }), 400)

@office.route('/offices', methods=['GET'])
@token_required
def get_all_offices(current_user):
    return make_response(jsonify({
        'status': 200, 
        'data': office_tb.get_offices()
    }), 200)

@office.route('/offices/<int:id>', methods=['GET'])
@token_required
def get_single_office(current_user, id):
    office = office_tb.get_one_office(id)
    if not office:
        return make_response(jsonify({
            'status': 404,
            'error': 'No office with id:{} found'.format(id)
        }), 404)
    else:
        return make_response(jsonify({
            'status': 200,
            'data': [office]
        }), 200)

@office.route('/offices/<int:id>', methods=['PATCH'])
@token_required
def update_office(current_user, id):
    admin = bool(current_user['is_admin'])
    if not (admin):
        print("I am in")
        return make_response(jsonify({
                'status': 401,
                'error': 'Only admin can perform this function'
            }), 401)
    office_data = request.get_json()
    msg = validate_office_data(office_data)
    if msg != 'ok':
        return make_response(jsonify({
            'status': 400,
            'error': msg
        }))

    office = office_tb.get_one_office(id)
    if not office:
        return make_response(jsonify({
            'status': 404,
            'error': 'No office with id:{} found'.format(id)
        }), 404)
    else:
        updated_office = office_tb.update_office(id, office_data)
        if 'error' in updated_office:
            return make_response(jsonify({
                'status':400, 
                'error': updated_office['error']
            }), 400)
        return make_response(jsonify({
            'status': 200,
            'data': [updated_office]
        }), 200)

@office.route('/offices/<int:id>', methods=['DELETE'])
@token_required
def delete_office(current_user, id):
    admin = bool(current_user['is_admin'])
    if not (admin):
        print("I am in")
        return make_response(jsonify({
                'status': 401,
                'error': 'Only admin can perform this function'
            }), 401)
    office = office_tb.get_one_office(id)
    if office:
        if office_tb.delete_office(id):
            return make_response(jsonify({
                'status': 200,
                'data':[{
                    'message': 'office with id:{} deleted'.format(id)
                }]
            }), 200)
        else:
            return make_response(jsonify({
                'status': 400, 
                'error' : 'update or delete on table "office" violates foreign key constraint.\nKey (id)=({}) is referenced on another table'.format(id)
            }), 400)
    else:
        return make_response(jsonify({
            'status': 404, 
            'error': 'No office with id:{} found'.format(id)
        }), 404)



@office.route('/offices/<int:id>/result', methods=['GET'])
@token_required
def get_office_election_result(current_user, id):
    results = office_tb.get_office_election_result(id)
    if not results:
        return make_response(jsonify({
            'status': 404,
            'error': 'No result found'
        }), 404)
    else:
        return make_response(jsonify({
            'status': 200,
            'data': results
        }), 200)
        