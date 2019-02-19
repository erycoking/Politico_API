# import pytest

# from politico.api.v2.party import routes
# from politico.config import create_app

# @pytest.fixture(scope='modules')
# def test_client():
#     test_client = create_app().test_client()
#     ctx = create_app().app_context()
#     ctx.push()
#     yield test_client
#     ctx.pop()



# def add_party(test_client):
#     party = {
#         "hq_address": "Westlands, Nairobi.",
#         "logo_url": "http://logo.com/logo/logo.jpg",
#         "name": "Nasa ria"
#     }
#     return test_client.post('/')

