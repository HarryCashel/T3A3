import unittest
from tests.helpers import Helpers
from main import create_app, db


class TestBooks(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        db.create_all()

        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db-custom", "seed"])

    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_user_register(self):
        endpoint = "/users/register"
        body = {
            "full_name": "Carry Hashel",
            "email": "testing1@fake.com",
            "password": "123456"
        }
        response, data = Helpers.post_request(endpoint, body=body)
        response2, data2 = Helpers.post_request(endpoint, body=body)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["email"], "testing1@fake.com")
        self.assertEqual(data["full_name"], "Carry Hashel")

        