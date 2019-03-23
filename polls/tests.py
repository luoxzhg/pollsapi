from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

from . import apiviews


# Create your tests here.
class TestUser(APITestCase):
    def setUp(self):
        self.username = 'test'
        self.email = 'test@test.com'
        self.password = 'testtest'
        self.uri = "/users/"

    def test_create_user(self):
        response = self.client.post(self.uri, {
            "username": self.username,
            "email": self.email,
            "password": self.password
        })
        msg = "Expected Response Code 201, but received {}".format(response.status_code)
        self.assertEqual(response.status_code, 201, msg)

    def test_create_user_without_username(self):
        response = self.client.post(self.uri, {
            "email": self.email,
            "password": self.password
        })
        msg = "Expected Response Code 400, but received {}".format(response.status_code)
        self.assertEqual(response.status_code, 400, msg)

    def test_create_user_without_password(self):
        response = self.client.post(self.uri, {
            "username": self.username,
            "email": self.email
        })
        msg = "Expected Response Code 400, but received {}".format(response.status_code)
        self.assertEqual(response.status_code, 400, msg)



def _create_user(self):
    UserModel = get_user_model()
    UserModel.objects.create_user(username=self.username,
                                  email=self.email,
                                  password=self.password)


class TestLogin(APITestCase):
    def setUp(self):
        self.uri = "/login/"
        self.username = "test"
        self.email = "test@test.com"
        self.password = "password"

    def test_login(self):
        _create_user(self)
        response = self.client.post(self.uri, {
            "username": self.username,
            "password": self.password
        })
        msg = "Expected Response Code 200, but received {}".format(response.status_code)
        self.assertEqual(response.status_code, 200, msg)

    def test_login_nonexists(self):
        response = self.client.post(self.uri, {
            "username": self.username,
            "password": self.password
        })
        msg = "Expected Response Code 400, but received {}".format(response.status_code)
        self.assertEqual(response.status_code, 400, msg)


class TestPoll(APITestCase):
    def setUp(self):
        self.username = "test"
        self.email = "test@test.com"
        self.password = "password"
        self.uri = "/polls/"
        self.user = _create_user(self)

    def test_get_poll_list(self):
        response = self.client.get(self.uri)
        msg = "Expected Response Code 200, but received {}".format(response.status_code)
        self.assertEqual(response.status_code, 200, msg)

    def test_post_poll_unauthentication(self):
        response = self.client.post(self.uri, {
            "question": "How are you?"
        })
        msg = "Expected Response Code 401, but received {}".format(response.status_code)
        self.assertEqual(response.status_code, 401, msg)

    def test_post_poll(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(self.uri, {
            "question": "How are you?"
        })
        msg = "Expected Response Code 201, but received {}".format(response.status_code)
        self.assertEqual(response.status_code, 201, msg)

    def test_get_poll_detail_nonexists(self):
        response = self.client.get(self.uri + '1/')
        msg = "Expected Response Code 404, but received {}".format(response.status_code)
        self.assertEqual(response.status_code, 404, msg)

    def test_get_poll_detail(self):
        self.test_post_poll()
        response = self.client.get(self.uri + '1/')
        msg = "Expected Response Code 200, but received {}".format(response.status_code)
        self.assertEqual(response.status_code, 200, msg)

