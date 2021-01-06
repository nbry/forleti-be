""" TESTS FOR USER MODELS.

1. Testing the 2 users in the fixture
2. Testing for adding a new user
3. Testing flask praetorian methods on User model
4. Testing other methods (e.g. signup) from User model

"""
from project.extensions import guard
from project.models.user import User


def test_new_instance_of_user():
    """
    GIVEN a User model
    WHEN a new User is instantiated
    THEN check that the username and email are defined correctly
    """

    new_user = User(username="bobby", email="bobby@bobby.com")
    assert new_user.username == "bobby"
    assert new_user.email == "bobby@bobby.com"


def test_users_in_db_fixture(client, db):
    """
    GIVEN the testing database fixture
    WHEN default users are analyzed
    THEN ensure users can be retrieved and their information returns as expected
    """

    # Query database and get first
    users = db.session.query(User).all()

    # First user should be JaneDoe
    assert users[0].username == "JaneDoe"
    assert users[0].email == "JaneDoe@emailtest.com"

    # Since "id" is the primary key on the User model,
    # as the first user, JaneDoe should have an ID of 1.
    # Check if UserModel "identity" method is working

    assert users[0].identity == 1

    # Now do the same for the second user, JohnApple
    assert users[1].username == "JohnApple"
    assert users[1].email == "JohnApple@emailtest.com"
    assert users[1].identity == 2


def test_user_model_praetorian_methods(db):
    """
    GIVEN test fixtures and two default users
    WHEN User model praetorian methods are used
    THEN ensure methods are return expected results
    """

    users = db.session.query(User).all()

    # Assuming this works if test_users_in_db_fixture() works
    jane_doe = users[0]

    # User model methods should return user properly
    assert jane_doe == User.lookup("JaneDoe")
    assert jane_doe == User.lookup_by_email("JaneDoe@emailtest.com")
    assert jane_doe == User.identify(1)


def test_new_user_signup(client, db):
    """
    GIVEN a User model
    WHEN User.signup() is called and stored in a variable "new_user"
    THEN check if new_user contains correct attributes and functions properly
    """

    # Sign up user using this method
    test_user3 = User.signup("SarahSmith", "password3", "SarahSmith@email.com")

    # Assert user in database
    assert test_user3 == db.session.query(User).filter_by(username="SarahSmith").first()

    # Assert user properties are correct
    assert test_user3.username == "SarahSmith"
    assert test_user3.email == "SarahSmith@email.com"

    # Ensure user can be authenticated
    assert test_user3 == guard.authenticate("SarahSmith", "password3")
