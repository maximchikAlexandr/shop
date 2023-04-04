from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Category, Discount, Producer, Product, Promocode
from catalog.serializers import (
    CategorySerializer,
    DiscountSerializer,
    ProducerSerializer,
    ProductSerializer,
    PromocodeSerializer,
)


class CategoriesListView(ListAPIView):
    queryset = Category.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer


class CatigoryProductsListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, category_id):
        queryset = Product.objects.filter(category__id=category_id)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class ProducersListView(ListAPIView):
    queryset = Producer.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProducerSerializer


class ProducerProductsListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, producer_id):
        queryset = Product.objects.filter(producer__id=producer_id)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class DiscountListView(ListAPIView):
    queryset = Discount.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = DiscountSerializer


class PromocodesListView(ListAPIView):
    queryset = Promocode.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PromocodeSerializer


class ProductsListView(ListAPIView):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
