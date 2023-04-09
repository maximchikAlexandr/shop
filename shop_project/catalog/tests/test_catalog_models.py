import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import reverse
from rest_framework.test import APIClient, APITestCase

pytestmark = [pytest.mark.django_db]

EVERYTHING_EQUALS_NON_NONE = type(
    "omnieq", (), {"__eq__": lambda x, y: y is not None}
)()


class CustomerTestCase(APITestCase):
    fixtures = ["catalog/tests/fixtures/db_fixture.json"]
    URLS_AND_KWARGS = (
        ("categories", None),
        ("category_products", {"category_id": 361}),
        ("producers", None),
        ("producer_products", {"producer_id": 87}),
        ("discounts", None),
        ("discounts_products", {"discount_id": 700}),
        ("promocodes", None),
        ("products", None),
    )

    def setUp(self) -> None:
        self.client = APIClient()
        password = make_password("12345qwerty!")
        self.user = get_user_model().objects.create(
            email="test@test2.com",
            password=password,
            is_active=True,
        )
        data = {"password": "12345qwerty!", "email": self.user.email}
        url = reverse("jwt-create")
        self.token = (
            "Bearer " + self.client.post(url, data=data, format="json").data["access"]
        )

    def test_catalog_models(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        for url, kwargs in self.URLS_AND_KWARGS:
            url = reverse(url, kwargs=kwargs)
            response = self.client.get(url)
            assert (
                response.status_code == 200
            ), f"Response status code is not 200. URL: {url}"
            assert (
                response.content == EVERYTHING_EQUALS_NON_NONE
            ), f"Response content is empty. URL: {url}"
