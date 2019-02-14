from flask import Blueprint, request, make_response, jsonify
from politico.api.v2.office.model import OfficeTable
from politico.api.v1.office.route import validate_office_data

# blueprint
office = Blueprint('offices', __name__)

office_tb = OfficeTable()

@office.route('/offices', methods=['POST'])
def create_office():
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
def get_all_offices():
    return make_response(jsonify({
        'status': 200, 
        'data': office_tb.get_offices()
    }), 200)

@office.route('/offices/<int:id>', methods=['GET'])
def get_single_office(id):
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
def update_office(id):
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
        return make_response(jsonify({
            'status': 200,
            'data': [updated_office]
        }), 200)

@office.route('/offices/<int:id>', methods=['DELETE'])
def delete_office(id):
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
                'error': 'Could not delete office with id:{}'.format(id)
            }), 200)
    else:
        return make_response(jsonify({
            'status': 404, 
            'error': 'No office with id:{} found'.format(id)
        }), 404)



