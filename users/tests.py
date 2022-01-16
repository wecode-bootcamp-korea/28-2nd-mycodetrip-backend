from django.test import TestCase, Client
from unittest.mock import MagicMock, patch

class AuthorizationViewTest(TestCase):
    @patch('users.views.requests')
    def test_success_authorization_view_post_method(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                data = {
                    "id":123456789,
                    "properties": {
                        "nickname": "홍길동",
                    },
                    "kakao_account": {
                        "email":"sample@sample.com",
                    }
                }
                return data

            def raise_for_status(self):
                pass

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization": "access token"}
        response            = client.post("/users/authorize", **headers)

        self.assertEqual(response.status_code, 201)

    @patch("users.views.requests")
    def test_no_token_authorization_view_post_method(self, mocked_requests):
        client = Client()
        class MockedResponse:
            def json(self):
                data = {
                    "id":123456789,
                    "properties":{
                        "nickname":"홍길동"
                    },
                    "kakao_account":{
                        "email":"sample@sample.com",
                    },
                }
                return data
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_NoAuthorization":"access token"}
        response            = client.post("/users/authorize", **headers)

        self.assertEqual(response.status_code, 401)

    @patch("users.views.requests")
    def test_signin_kakao_view_post_invalid_token(self, mocked_requests):
        client = Client()
        class MockedResponse:
            def json(self):
                data = {
                    "error":12347,
                }
                return data
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization":"fake access token"}
        response            = client.post("/users/authorize", **headers)

        self.assertEqual(response.status_code, 403)
