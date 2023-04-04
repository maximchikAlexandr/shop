from django.urls import path
from catalog.views import (
    CategoriesListView,
    CatigoryProductsListView,
    DiscountListView,
    ProducersListView,
    PromocodesListView,
    ProductsListView,
    ProducerProductsListView,
)

urlpatterns = [
    path("catigories/", CategoriesListView.as_view(), name="categories"),
    path("catigories/<int:category_id>/", CatigoryProductsListView.as_view(), name="category_products"),

    path("producers/", ProducersListView.as_view(), name="producers"),
    path("producers/<int:producer_id>/", ProducerProductsListView.as_view(), name="producer_products"),

    path("discounts/", DiscountListView.as_view(), name="discounts"),
    path("promocodes/", PromocodesListView.as_view(), name="promocodes"),
    path("products/", ProductsListView.as_view(), name="products"),
]
