# import os
import pytest
from project import create_app
from project.extensions import db as _db


# TESTDB = 'forleti_test_db'
# TEST_DATABASE_uri = "postgresql"
#


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app('testing.cfg')

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture(scope="module")
def init_database(test_client):
    _db.create_all()

    yield

    _db.drop_all()
