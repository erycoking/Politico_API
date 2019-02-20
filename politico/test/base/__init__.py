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



