from catalog.views import (
    BasketView,
    CategoriesListView,
    CategoryProductsListView,
    DiscountListView,
    DiscountProductsListView,
    OrderView,
    ProducerProductsListView,
    ProducersListView,
    ProductsListView,
    PromocodesListView,
)
from django.urls import path

urlpatterns = [
    # clients views
    path("catigories/", CategoriesListView.as_view(), name="categories"),
    path(
        "catigories/<int:category_id>/",
        CategoryProductsListView.as_view(),
        name="category_products",
    ),
    path("producers/", ProducersListView.as_view(), name="producers"),
    path(
        "producers/<int:producer_id>/",
        ProducerProductsListView.as_view(),
        name="producer_products",
    ),
    path("discounts/", DiscountListView.as_view(), name="discounts"),
    path(
        "discounts/<slug:discount_id>/",
        DiscountProductsListView.as_view(),
        name="discounts_products",
    ),
    path("promocodes/", PromocodesListView.as_view(), name="promocodes"),
    path("products/", ProductsListView.as_view(), name="products"),
    # customer views
    path("cart/", BasketView.as_view(), name="user-basket"),
    path("orders/", OrderView.as_view(), name="create-order"),
]
