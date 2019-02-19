# import pytest
# from politico.api.v2.db.db import DB
# from politico.api.v2.party.model import PartyTable



# @pytest.fixture(scope='module')
# def party_tb():
#     print('Initilizing database')
#     db = DB(True)
#     db.initialize_db()
#     table = PartyTable(db)
#     yield table
#     print('Tearing Down database connection')
#     db.tear_down_test_database()

# def party_1(party_tb):
#     party_data = {
#             "hq_address": "Westlands, Nairobi",
#             "logo_url": "http://logo.com/logo.jpg",
#             "name": "jubilee"
#         }
#     return party_tb.create_party(party_data)

# def party_2(party_tb):
#     party_data = {
#         "hq_address": "riftvalley",
#         "logo_url": "http://logo.com/logo.jpg",
#         "name": "urp"
#     }
#     return party_tb.update_party(1, party_data)

# def test_create_party(party_tb):
#     party = party_1(party_tb)
#     print(party)
#     assert party.get('name') == 'jubilee'
#     assert party.get('logo_url') == 'http://logo.com/logo.jpg'

# def test_get_one_party(party_tb):
#     party = party_tb.get_one_party(1)
#     print(party)
#     assert party.get('name') == 'jubilee'
#     assert party.get('logo_url') == 'http://logo.com/logo.jpg'

# def test_get_all_partys(party_tb):
#     partys = party_tb.get_parties()
#     print(partys)
#     assert len(partys) == 1
#     party = partys[0]
#     assert party.get('name') == 'jubilee'
#     assert party.get('logo_url') == 'http://logo.com/logo.jpg'

# def test_get_party_with_name(party_tb):
#     party = party_tb.get_one_party_by_name('jubilee')
#     print(party)
#     assert party.get('name') == 'jubilee'
#     assert party.get('logo_url') == 'http://logo.com/logo.jpg'

# def test_update_party(party_tb):
#     party = party_2(party_tb)
#     print(party)
#     assert party.get('name') == 'urp'
#     assert party.get('logo_url') == 'http://logo.com/logo.jpg'

# def test_delete_party(party_tb):
#     party_deleted = party_tb.delete_party(1)
#     print(party_deleted)
#     assert party_deleted == True