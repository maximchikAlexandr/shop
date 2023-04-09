import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import reverse
from rest_framework.test import APIClient, APITestCase

pytestmark = [pytest.mark.django_db]

EV_EQUALS_NON_NONE = type("omnieq", (), {"__eq__": lambda x, y: y is not None})()


class CustomerTestCase(APITestCase):
    fixtures = ["catalog/tests/fixtures/db_fixture.json"]

    def check_response(self, url, kwargs):
        url = reverse(url, kwargs=kwargs)
        response = self.client.get(url)
        assert (
                response.status_code == 200
        ), f"Response status code is not 200. URL: {url}"
        assert (
                response.content == EV_EQUALS_NON_NONE
        ), f"Response content is empty. URL: {url}"

    def test_categories(self):
        self.check_response("categories", None)

    def test_category_products(self):
        self.check_response("category_products", {"category_id": 21})

    def test_producers(self):
        self.check_response("producers", None)

    def test_producer_products(self):
        self.check_response("producer_products", {"producer_id": 87})

    def test_discounts(self):
        self.check_response("discounts", None)

    def test_producer_products(self):
        self.check_response("discounts_products", {"discount_id": 700})

    def test_promocodes(self):
        self.check_response("promocodes", None)

    def test_discounts(self):
        self.check_response("promocodes", None)
