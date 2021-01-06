"""
TESTS FOR USER ROUTES

NOTE: db (fixture) is often required as an argument for these test to provide
context to the fixtures.
"""

# DEFAULT VARIABLES
EXISTING_USER_USERNAME = "JaneDoe"
EXISTING_USER_PASS = "password1"
NEW_USERNAME = "NewUser"
NEW_EMAIL = "NewUser@emailtest.com"
NEW_PASSWORD = "password2"
PRAETORIAN_DEFAULT_AUTH_FAIL_MSG = "The username and/or password are incorrect"


def test_login_route_with_correct_credentials(client, db):
    """
    GIVEN a Flask app instance
    WHEN submitting a POST request to /login route with correct JSON input
    THEN ensure proper user login and JSON (with token) is returned
    """
    json_body = {"username": EXISTING_USER_USERNAME, "password": EXISTING_USER_PASS}
    res = client.post('/login', json=json_body)
    res_message = res.json["message"]
    res_token = res.json["token"]

    assert res.status_code == 200
    assert res_message == f"Success! Logged in to {EXISTING_USER_USERNAME}'s account"
    assert res_token


def test_protected_route_with_token(client, db):
    """
    GIVEN a Flask app instance
    WHEN submitting a get request to a protected route (like /settings/account)
    THEN ensure user can access the page
    """

    # These following lines should work if first test runs properly:
    json_body = {"username": EXISTING_USER_USERNAME, "password": EXISTING_USER_PASS}
    res = client.post('/login', json=json_body)
    token = res.json["token"]

    # Should not work without token in header:
    res_protected = client.get('/settings/account')
    assert res_protected.status_code == 401

    # Should work with token in the header
    headers = {"Authorization": f"Bearer {token}"}
    res_protected_with_headers = client.get('/settings/account', headers=headers)
    assert res_protected_with_headers.status_code == 200


def test_login_route_with_incorrect_credentials(client, db):
    """
    GIVEN a Flask app instance
    WHEN submitting a POST request to /login route with incorrect JSON input
    THEN ensure user is not logged in and appropriate JSON is returned
    """
    json_body = {"username": EXISTING_USER_USERNAME, "password": "INCORRECT_PASSWORD"}
    res = client.post('/login', json=json_body)
    res_message = res.json["message"]

    # Failed authorization should result with flask praetorian's default auth failure message
    assert res.status_code == 401
    assert res_message == PRAETORIAN_DEFAULT_AUTH_FAIL_MSG


def test_signup_route(client, db):
    """
    GIVEN a Flask app instance
    WHEN submitting a post request to /signup route with correct/unique credentials
    THEN ensure proper JSON is returned user flow behaves as expected
    """

    json_body = {"username": NEW_USERNAME, "password": NEW_PASSWORD, "email": NEW_EMAIL}
    res = client.post('/signup', json=json_body)
    res_message = res.json["message"]
    res_token = res.json["token"]

    assert res.status_code == 200
    assert res_message == f"Successfully created account for {NEW_USERNAME}"
    assert res_token


def test_signup_route_with_duplicate_user(client, db):
    """
    GIVEN a Flask app instance
    WHEN submitting a post request to /signup route with credentials matching that
        of a user already in the database
    THEN ensure signup fails and appropriate message is returned
    """
    json_body = {"username": EXISTING_USER_USERNAME, "password": EXISTING_USER_PASS}
    res = client.post('/signup', json=json_body)
    res_message = res.json["message"]

    assert res.status_code == 400
    assert res_message == "User with that username/email already exists!"

# ****************************
# TO BE IMPLEMENTED AT PRODUCTION (ERRORS NOT BE HANDLED AT THE PRESENT TIME)
# ****************************

# def test_signup_route_with_missing_info(client, db):
#     """
#     GIVEN a Flask app instance
#     WHEN submitting a post request to /signup route with missing data (i.e. username, email)
#     THEN ensure proper JSON is returned user flow behaves as expected
#     """
#
#     json_body = {}
#     res = client.post('/signup', json=json_body)
#
#     assert res.status_code == 400
