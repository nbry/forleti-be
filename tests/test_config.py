"""
Yo dawg I heard you like tests, so...

test_config.py tests the instance config settings for the different environments:
1. development
2. production
3. testing
"""
from project import create_app
from project.models.user import User


def test_testing_fixture(app, client, db):
    """
    GIVEN test_client (i.e. the flask_app fixture)
    WHEN fixture is created
    THEN fixture should have correct config settings and two users in the testing db
    """

    # Ensure test client is running
    response = client.get('/poke')
    assert response.status_code == 200

    # Ensure correct database is being used
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'postgresql:///forleti_test_db'

    # Ensure database is running and has two users
    # Possibly redundant since the test would fail if db was faulty
    assert db

    # Ensure test database has two users (JaneDoe and JohnApple), as defined in:
    # "tests/conftest.py" (under "def db(client)")
    users = db.session.query(User).all()
    assert len(users) == 3
    assert users[1].username == "JaneDoe"
    assert users[2].username == "JohnApple"

    # Ensure that user created with User.signup() is in database
    # FURTHER NOTE: Upon testing, this user comes back before the others.
    assert users[0].username == "RegularSteve"


def test_testing_config():
    """
    GIVEN an instance of create_app named "app"
    WHEN app is given TESTING configuration settings from instance/testing.cfg
    THEN app should have the expected config settings
    NOTE: This test also acts as a functional test for the project's create_app function
    """
    app = create_app('testing.cfg')

    # app should have DEBUG configuration
    assert app.config['DEBUG']

    # app database URI should be testing database (currently: forleti_test_db on postgreSQL)
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'postgresql:///forleti_test_db'


def test_development_config():
    """
    GIVEN an instance of create_app named app
    WHEN app is given DEVELOPMENT configuration settings from instance/development.cfg
    THEN app should have the expected config settings
    NOTE: This test also acts as a functional test for the project's create_app function
    """
    app = create_app('development.cfg')

    # app should have DEBUG configuration
    assert app.config['DEBUG']

    # app database URI should be development database (currently: forleti_db on postgreSQL)
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'postgresql:///forleti_db'
