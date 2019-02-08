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
        existing_office = office_table.get_office_by_name(office_data['name'])
        if not existing_office:
            created_office = office_table.add_office(office_data)
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
    # returns all offices in the DB
    offices = office_table.get_all_offices()
    return make_response(jsonify({
        'status': 200, 
        'data': offices
    }), 200)

@office.route('/offices/<int:id>', methods=['GET'])
def get_single_office(id):
    # returns a single office
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
    # updates an office in the database
    office_data = request.get_json()
    msg = validate_office_data(office_data)
    if msg != 'ok':
        return make_response(jsonify({
            'status': 400,
            'error': msg
        }))

    office = office_table.get_single_office(id)
    if not office:
        return make_response(jsonify({
            'status': 404,
            'error': 'No office with id:{} found'.format(id)
        }), 404)
    else:
        updated_office = office_table.update_office(id, office_data)
        return make_response(jsonify({
            'status': 200,
            'data': [updated_office]
        }), 200)

@office.route('/offices/<int:id>', methods=['DELETE'])
def delete_office(id):
    # delete an office in the database
    office_check = office_table.get_single_office(id)
    if office_check:
        if office_table.delete_office(id):
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



def validate_office_data(office):
    # validates office input
    if not office:
        return 'No office data found'
    elif 'type' not in office:
        return 'office type missing'
    elif 'name' not in office:
        return 'office name missing'
    elif office['type'] not in ['federal', 'legislative', 'state', 'local_government']:
        return 'Invalid office type.'
    elif not isinstance(office['name'], str):
        return 'Invalid office name. Office name should be made of strings'
    elif len(office['name']) < 3:
        return 'Invalid office name. Office name should be greater than 3 characters'
    else:
        return 'ok'
