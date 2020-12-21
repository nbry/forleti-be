from unittest import TestCase

from app import app


class TestPage(TestCase):
    """ Testing Test page route ('/Test') """

    def test_html(self):
        with app.test_client() as client:
            res = client.get('/test')
            json = res.get_json()

            self.assertEqual(res.status_code, 200)
            self.assertEqual({"message": "hello world"}, json)
