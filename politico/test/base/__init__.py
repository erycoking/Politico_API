import pytest
import unittest
from politico import create_app
from politico.api.v2.db import DB


@pytest.fixture(scope='module')
def test_client():
    app = create_app('testing')
    app.config['TESTING'] = True
    test_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    db = DB()
    db.initialize_db()
    yield test_client
    db.tear_down_test_database()
    ctx.pop()


# db = DB()

# class BaseTest(unittest.TestCase):

    
    
#     def setUp(self):
#         self.app = create_app('testing')
#         self.
#         self.test_client = self.app.test_client
#         self.ctx = self.app.app_context()
#         self.app.app_context().push()
#         db.initialize_db()
#         self.added_user =self.

#     # def tearDown(self):
#     #     with self.app.app_context():
#     #         db.tear_down_test_database
#     #     self.app.app_context().pop()


