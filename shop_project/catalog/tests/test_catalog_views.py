import json
import os

import pytest
from deepdiff import DeepDiff
from django.conf import settings
from django.shortcuts import reverse
from rest_framework.test import APITestCase

pytestmark = [pytest.mark.django_db]

PATH_TO_FIXTURES = "catalog/tests/fixtures/"


class ClientEndpointsTestCase(APITestCase):
    fixtures = [
        f"{PATH_TO_FIXTURES}/{fix}"
        for fix in os.listdir(f"{settings.BASE_DIR}/{PATH_TO_FIXTURES}")
    ]

    def setUp(self):
        for fix_path in self.fixtures:
            with open(fix_path, "r", encoding="utf-8") as fixture_file:
                fixture = json.load(fixture_file)
                attr_name = os.path.basename(fixture_file.name)
                attr_name = attr_name.rstrip(".json")
            setattr(self, attr_name, [])

            for model in fixture:
                getattr(self, attr_name).append(model["fields"] | {"id": model["pk"]})

    def check_response(self, *, url, fixture, kwargs=None, nested_fixtures=None):
        """Check response
        nested_fixtures - fixtures for the nested serializers
        """
        url = reverse(url, kwargs=kwargs)
        response = self.client.get(url)

        assert response.status_code == 200, \
            f"The response status code is not 200. URL: {url}"

        assert isinstance(response.data, list), \
            f"Type of the data is not list. URL: {url}"

        if nested_fixtures is None:
            self.check_without_nested_serializers(response, url, fixture)
        else:
            self.check_with_nested_serializers(response, url, fixture, nested_fixtures)

    def check_without_nested_serializers(self, response, url, fixture):
        assert response.data == getattr(self, fixture), \
            f"The response data does not match original fixture. URL: {url}"

    def check_with_nested_serializers(self, response, url, fixture, nested_fixtures):
        for fix in nested_fixtures:
            locals()[f"nested_{fix}"] = []

        response_data = [dict(obj) for obj in response.data]
        original_data = getattr(self, fixture)

        for orig_obj, resp_obj in zip(original_data, response_data):
            ddiff = dict(DeepDiff(orig_obj, resp_obj, ignore_order=True))
            for model, change in ddiff['type_changes'].items():
                assert change["old_value"] == change["new_value"]["id"]
                if model == "root['discount']":
                    locals()["nested_catalog_discount"].append(change["new_value"])
                elif model == "root['category']":
                    locals()["nested_catalog_category"].append(change["new_value"])
                elif model == "root['producer']":
                    locals()["nested_catalog_producer"].append(change["new_value"])

        for fix in nested_fixtures:
            assert [i for i in locals()[f"nested_{fix}"] if i not in getattr(self, fix)] == []


    def test_categories(self):
        self.check_response(
            url="categories", fixture="catalog_category"
        )

    def test_producers(self):
        self.check_response(
            url="producers", fixture="catalog_producer"
        )

    def test_discounts(self):
        self.check_response(
            url="discounts", fixture="catalog_discount"
        )

    def test_promocodes(self):
        self.check_response(
            url="promocodes", fixture="catalog_promocode"
        )

    def test_products(self):
        self.check_response(
            url="products",
            fixture="catalog_product",
            kwargs=None,
            nested_fixtures=[
                "catalog_discount",
                "catalog_category",
                "catalog_producer",
            ]
        )
    #
    # def test_category_products(self):
    #     self.check_response(
    #         url="category_products", fixture="catalog_product",
    #         kwargs={"category_id": 21}, has_nested_serializers=True
    #     )
    #
    # def test_producer_products(self):
    #     self.check_response(
    #         url="discounts_products", fixture="catalog_product",
    #         kwargs={"discount_id": 101}, has_nested_serializers=True
    #     )
    #
    # def test_producer_products(self):
    #     self.check_response(
    #         url="producer_products", fixture="catalog_product",
    #         kwargs={"producer_id": 87}, has_nested_serializers=True
    #     )
