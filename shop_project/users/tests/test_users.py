import os

import pytest
from rest_framework.test import APIClient, APITestCase
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

pytestmark = [pytest.mark.django_db]
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')

class UsersTestCase(APITestCase):

    def setUp(self) -> None:
        """Создает исходные объекты для теста"""
        self.client = APIClient()
        password = make_password("12345qwerty")
        self.user = get_user_model().objects.create(
            email="test@mail.com",
            password=password,
            is_active=True
        )
        data = {
            "password": "12345qwerty",
            "email": self.user.email
        }
        url = reverse("jwt-create")

        self.token = "Bearer " + self.client.post(
            url,
            data=data,
            format="json"
        ).data["access"]

    def test_auth(self):
        url = reverse("hello")
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data == "Hello world!"
