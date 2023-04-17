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
        """
        Create a list of dictionaries based on json fixtures.
        Fixtures are located in the path 'PATH_TO_FIXTURES'
        """
        for fix_path in self.fixtures:
            with open(fix_path, "r", encoding="utf-8") as fixture_file:
                fixture = json.load(fixture_file)
                attr_name = os.path.basename(fix_path)
                attr_name = attr_name.rstrip(".json")
            setattr(self, attr_name, [])

            for model in fixture:
                getattr(self, attr_name).append(model["fields"] | {"id": model["pk"]})

    def check_response(self, *, url, fixture, kwargs=None, nested_objs=None):
        """Check response
        nested_objs - fixtures for the nested serializers
        """
        url = reverse(url, kwargs=kwargs)
        response = self.client.get(url)

        assert response.status_code == 200, \
            f"The response status code is not 200. URL: {url}"

        assert isinstance(response.data, list), \
            f"Type of the data is not list. URL: {url}"

        if nested_objs is None:
            self.check_without_nested_serializers(response, url, fixture)
        else:
            self.check_with_nested_serializers(response, url, fixture, nested_objs)

    def check_without_nested_serializers(self, response, url, fixture):
        assert response.data == getattr(self, fixture), \
            f"The response data does not match original fixture. URL: {url}"

    def check_with_nested_serializers(self, response, url, fixture, names_of_sub_objs):
        response_sub_objs = {sub_obj: [] for sub_obj in names_of_sub_objs}
        response_data = [dict(obj) for obj in response.data]
        original_data = getattr(self, fixture)

        for orig_obj, resp_obj in zip(original_data, response_data):
            ddiff = dict(DeepDiff(orig_obj, resp_obj, ignore_order=True))
            response_sub_objs = self.add_response_sub_objs(ddiff, orig_obj, url,
                                                           names_of_sub_objs,
                                                           response_sub_objs)

        self.compare_sub_objs(names_of_sub_objs, response_sub_objs, url)

    @staticmethod
    def add_response_sub_objs(ddiff, orig_obj, url, names_of_sub_objs, response_sub_objs):
        for name_obj, changes_in_obj in ddiff['type_changes'].items():

            assert changes_in_obj["new_value"].get("id") is not None, \
                f"The nested object {name_obj} not contain field 'id'"

            assert changes_in_obj["old_value"] == changes_in_obj["new_value"]["id"], \
                f"Field 'id' in objects from the nested serializer do not match field 'id' from " \
                f"the original fixture {orig_obj}. URL: {url}"

            for sub_obj in names_of_sub_objs:
                if name_obj == f"root['{sub_obj.split('_')[1]}']":
                    response_sub_objs[sub_obj].append(changes_in_obj["new_value"])

        return response_sub_objs

    def compare_sub_objs(self, names_of_sub_objs, response_sub_objs, url):
        for sub_obj, changes_in_obj in response_sub_objs.items():
            assert len(changes_in_obj) > 0, \
                f"The nested serializer {sub_obj} not work correctly."

        for sub_obj in names_of_sub_objs:
            fixture = getattr(self, sub_obj)
            list_of_differences = [obj for obj in response_sub_objs[sub_obj] if obj not in fixture]
            assert list_of_differences == [], \
                f"Objects from the nested serializer do not match source fixture {sub_obj}. " \
                f"URL: {url}"

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
            nested_objs=[
                "catalog_discount",
                "catalog_category",
                "catalog_producer",
            ]
        )

    # def test_category_products(self):
    #     self.check_response(
    #         url="category_products", fixture="catalog_product",
    #         kwargs={"category_id": 21},
    #         nested_objs=[
    #             "catalog_discount",
    #             "catalog_category",
    #             "catalog_producer",
    #         ]
    #     )
    #
    # def test_discount_products(self):
    #     self.check_response(
    #         url="discounts_products", fixture="catalog_product",
    #         kwargs={"discount_id": 101},
    #         nested_objs=[
    #             "catalog_discount",
    #             "catalog_category",
    #             "catalog_producer",
    #         ]
    #     )
    #
    # def test_producer_products(self):
    #     self.check_response(
    #         url="producer_products", fixture="catalog_product",
    #         kwargs={"producer_id": 87},
    #         nested_objs=[
    #             "catalog_discount",
    #             "catalog_category",
    #             "catalog_producer",
    #         ]
    #     )
