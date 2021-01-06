import pytest
from project.models.user import User
from project import create_app
from project.extensions import db as _db, guard


@pytest.fixture(scope="module")
def app():
    flask_app = create_app('testing.cfg')
    yield flask_app


@pytest.fixture(scope="module")
def client(app):
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture(scope="module")
def db(app):
    _db.create_all()

    # Add two users to testing database
    # Note that password must be manually hashed
    raw_pass1 = guard.hash_password("password1")
    test_user1 = User(username="JaneDoe",
                      email="JaneDoe@emailtest.com",
                      hashed_password=raw_pass1,
                      created="1/1/2021 00:00:00 AM")

    raw_pass2 = guard.hash_password("password2")
    test_user2 = User(username="JohnApple",
                      email="JohnApple@emailtest.com",
                      hashed_password=raw_pass2,
                      created="1/1/2021 00:00:00 AM")

    # Add the two users and commit changes
    _db.session.add(test_user1)
    _db.session.add(test_user2)
    _db.session.commit()

    yield _db

    _db.session.close()
    _db.drop_all()
