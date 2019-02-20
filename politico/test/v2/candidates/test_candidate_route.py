# import pytest
# from ...base import test_client, token, standard, error_standard

# @pytest.fixture(scope='module')
# def candidates():
#     candidates = {
#         "party":1,
#         "candidate":1
#     }
#     return candidates

# @pytest.fixture(scope='module')
# def candidates_2():
#     candidates = {
#         "party":1,
#         "candidate":1
#     }
#     return candidates

# @pytest.fixture(scope='module')
# def bad_candidates():
#     candidates = {
#         "candidate":1
#     }
#     return candidates

# @pytest.fixture(scope='module')
# def bad_candidates_2():
#     candidates = candidates = {
#         "party":1,
#         "candidate":"qwertyui"
#     }
#     return candidates

# def test_add_candidates(test_client, token, candidates):
#     url = '/api/v2/offices/1/register'
#     response  = test_client.open(url, method='POST', headers={
#         'Authorization': 'Bearer {}'.format(token)
#     }, json=candidates)
#     assert response.status_code == 201
#     response_data = standard(response)
#     data = response_data['data']
#     assert len(data) == 1
#     candidates_1 = data[0]
#     assert 'office' in candidates_1 and candidates_1['office'] == '1'
#     assert 'id' in candidates_1 and candidates_1['id'] == '1'

# def test_add_bad_candidates(test_client, token, bad_candidates):
#     url = '/api/v2/offices/1/candidates'
#     response  = test_client.open(url, method='POST', headers={
#         'Authorization': 'Bearer {}'.format(token)
#     }, json=bad_candidates)
#     assert response.status_code == 400
#     data = error_standard(response)
#     message = data['error']
#     assert message == 'party missing'


# def test_add_bad_candidates_2(test_client, token, bad_candidates_2):
#     url = '/api/v2/offices/1/candidates'
#     response  = test_client.open(url, method='POST', headers={
#         'Authorization': 'Bearer {}'.format(token)
#     }, json=bad_candidates_2)
#     assert response.status_code == 400
#     data = error_standard(response)
#     message = data['error']
#     assert message == 'all field should be of integer type'

# def test_upate_candidates(test_client, token, candidates_2):
#     url = '/api/v2/offices/1/candidates'
#     response  = test_client.open(url, method='PATCH', headers={
#         'Authorization': 'Bearer {}'.format(token)
#     }, json=candidates_2)
#     assert response.status_code == 200
#     response_data = standard(response)
#     data = response_data['data']
#     assert len(data) == 1
#     candidates_1 = data[0]
#     assert 'office' in candidates_1 and candidates_1['office'] == '1'
#     assert 'id' in candidates_1 and candidates_1['id'] == '1'

# def test_get_all_candidatess(test_client, token):
#     url = '/api/v2/offices/1/candidates'
#     response = test_client.open(url, method='GET', headers={
#             'Authorization': 'Bearer {}'.format(token)
#         }
#     )
#     assert response.status_code == 200
#     response_data = standard(response)
#     data = response_data['data']
#     assert len(data) == 1
#     candidates_1 = data[0]
#     assert candidates_1 is not None
#     assert 'office' in candidates_1 and candidates_1['office'] == '1'
#     assert 'id' in candidates_1 and candidates_1['id'] == '1'

# def test_get_single_candidates(test_client, token):
#     url = '/api/v2/offices/1/candidates/1'
#     response = test_client.open(url, method='GET', headers={
#             'Authorization': 'Bearer {}'.format(token)
#         }
#     )
#     assert response.status_code == 200
#     response_data = standard(response)
#     data = response_data['data']
#     assert len(data) == 1
#     candidates_1 = data[0]
#     assert candidates_1 is not None
#     assert 'name' in candidates_1 and candidates_1['name'] == 'mca'
#     assert 'type' in candidates_1 and candidates_1['type'] == 'local government'

# def test_delete_candidates(test_client, token):
#     url = '/api/v2/offices/1/candidates/1'
#     response = test_client.open(url, method='DELETE', headers={
#             'Authorization': 'Bearer {}'.format(token)
#         }
#     )
#     assert response.status_code == 200
#     response_data = standard(response)
#     data = response_data['data']
#     assert 'message' in data[0]
#     assert data[0]['message'] == 'candidates with id:1 deleted'