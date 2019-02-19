import pytest
from politico import create_app
from politico.api.v2.db import DB


@pytest.fixture(scope='module')
def test_client():
    app = create_app('testing')
    test_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield test_client
    ctx.pop()

