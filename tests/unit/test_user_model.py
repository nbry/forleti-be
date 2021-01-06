""" Tests for User Model """
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

# def test_a_transaction(db_session):
#     user = db_session.query(User).get(1)
#     assert user.username == "bobby"
