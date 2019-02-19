# import pytest
# from politico.api.v2.db.db import DB
# from politico.api.v2.office.model import OfficeTable



# @pytest.fixture(scope='module')
# def office_tb():
#     print('Initilizing database')
#     db = DB(True)
#     db.initialize_db()
#     table = OfficeTable(db)
#     yield table
#     print('Tearing Down database connection')
#     db.tear_down_test_database()

# def office_1(office_tb):
#     office_data = {
#             "type": "local government", 
#             "name": "senetor"
#         }
#     return office_tb.create_office(office_data)

# def office_2(office_tb):
#     office_data = {
#             "type": "local government", 
#             "name": "mca"
#         }
#     return office_tb.update_office(1, office_data)

# def test_create_office(office_tb):
#     office = office_1(office_tb)
#     print(office)
#     assert office.get('type') == 'local government'
#     assert office.get('name') == 'senetor'

# def test_get_one_office(office_tb):
#     office = office_tb.get_one_office(1)
#     print(office)
#     assert office.get('type') == 'local government'
#     assert office.get('name') == 'senetor'

# def test_get_all_offices(office_tb):
#     offices = office_tb.get_offices()
#     print(offices)
#     assert len(offices) == 1
#     office = offices[0]
#     assert office.get('type') == 'local government'
#     assert office.get('name') == 'senetor'

# def test_get_office_with_name(office_tb):
#     office = office_tb.get_one_office_by_name('senetor')
#     print(office)
#     assert office.get('type') == 'local government'
#     assert office.get('name') == 'senetor'

# def test_update_office(office_tb):
#     office = office_2(office_tb)
#     print(office)
#     assert office.get('type') == 'local government'
#     assert office.get('name') == 'mca'

# def test_delete_office(office_tb):
#     office_deleted = office_tb.delete_office(1)
#     print(office_deleted)
#     assert office_deleted == True