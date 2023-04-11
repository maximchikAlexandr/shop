import pytest

from django.shortcuts import reverse
from rest_framework.test import APITestCase

from conftest import EV_EQUALS_NON_NONE

pytestmark = [pytest.mark.django_db]


class ClientEndpointsTestCase(APITestCase):
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

    def check_response_list(self, url, kwargs):
        url = reverse(url, kwargs=kwargs)
        response = self.client.get(url)
        assert (
            response.status_code == 200
        ), f"Response status code is not 200. URL: {url}"
        assert isinstance(response.data, list)
        # дописать сравнение с json
        # assert response.data =
        assert (
            response.content == EV_EQUALS_NON_NONE
        ), f"Response content is empty. URL: {url}"
        # доделать
        # assert response.data[0]["discount"] == discount
        # assert response.data[0]["producer"] == producer
        # assert response.data[0]["category"] == category

    def test_categories(self):
        self.check_response_list("categories", None)

    def test_category_products(self):
        self.check_response("category_products", {"category_id": 21})

    def test_producers(self):
        self.check_response_list("producers", None)

    def test_producer_products(self):
        self.check_response("producer_products", {"producer_id": 87})

    def test_discounts(self):
        self.check_response_list("discounts", None)

    def test_producer_products(self):
        self.check_response("discounts_products", {"discount_id": 700})

    def test_promocodes(self):
        self.check_response_list("promocodes", None)

    def test_discounts(self):
        self.check_response_list("promocodes", None)
