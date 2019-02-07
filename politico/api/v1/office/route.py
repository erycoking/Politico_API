"""routes for interacting with office model"""

# import custom modules
from flask import Blueprint, request, make_response, jsonify

# import custom modules
from politico.api.v1.office.model import Office
from politico.api.v1.office.model import OfficeTable

# create a blueprint
office = Blueprint('office', __name__)

# initialize office table
office_table = OfficeTable()

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
        created_office = office_table.add_office(office_data)
        return make_response(jsonify({
            'status': 201, 
            'data': [created_office.office_data]
        }), 201)

@office.route('/offices', methods=['GET'])
def get_all_offices():
    offices = office_table.get_all_offices()
    return make_response(jsonify({
        'status': 200, 
        'data': offices
    }), 200)

@office.route('/offices/<int:id>', methods=['GET'])
def get_single_office(id):
    office = office_table.get_single_office(id)
    if not office:
        return make_response(jsonify({
            'status': 404,
            'error': 'No office with id:{} found'.format(id)
        }), 404)
    else:
        return make_response(jsonify({
            'status': 200,
            'data': [office.office_data]
        }), 200)

@office.route('/offices/<int:id>', methods=['PATCH'])
def update_office(id):
    office_data = request.get_json()
    office = office_table.get_single_office(id)
    if not office:
        return make_response(jsonify({
            'status': 404,
            'error': 'No office with id:{} found'.format(id)
        }), 404)
    
    msg = validate_office_data(office_data)
    if msg != 'ok':
        return make_response(jsonify({
            'status': 400,
            'error': msg
        }))
    else:
        updated_office = office_table.update_office(id, office_data)
        return make_response(jsonify({
            'status': 400,
            'data': [updated_office.office_data]
        }))


def validate_office_data(office):
    if not office:
        return 'No office data found'
    elif 'type' not in office:
        return 'office type missing'
    elif 'name' not in office:
        return 'office name missing'
    elif office['type'] not in ['federal', 'legislative', 'state', 'local_government']:
        return 'Invalid office type.'
    elif not isinstance(office['name'], basestring):
        return 'Invalid office name. Office name should be made of strings'
    elif len(office['name']) < 3:
        return 'Invalid office name. Office name should be greater than 3 characters'
    else:
        return 'ok'
