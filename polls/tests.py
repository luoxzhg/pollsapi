from rest_framework.test import APITestCase

from . import apiviews


# Create your tests here.
class TestPoll(APITestCase):
    def setUp(self):
        self.uri = 'polls'

    def test_get_poll_list(self):
        response = self.client.get(self.uri)
        msg = "Expected Response Code 200, but received {}".format(response.status_code)
        self.assertEqual(response.status_code, 200, msg)

    def test_post_poll(self):
        self.client.login()
