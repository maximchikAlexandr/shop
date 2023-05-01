from django.db.models import F
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Basket, Category, Discount, Producer, Product, Promocode
from catalog.serializers import (
    AddProductSerializer,
    BasketSerializer,
    CategorySerializer,
    DeleteProductSerializer,
    DiscountSerializer,
    OrderSerializer,
    ProducerSerializer,
    ProductSerializer,
    PromocodeSerializer,
)


class CategoriesListView(ListAPIView):
    queryset = Category.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer


class CategoryProductsListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, category_id):
        queryset = Product.objects.filter(category__id=category_id)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class DiscountProductsListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, discount_id):
        if discount_id == "null":
            queryset = Product.objects.filter(discount__id__isnull=True)
        else:
            queryset = Product.objects.filter(discount__id=discount_id)
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


class BasketView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        basket = (
            Product.objects.prefetch_related("basket_set")
            .filter(basket__user=user)
            .values(
                "name",
                "price",
                "discount",
                number_of_items=F("basket__count"),
                discount_percent=F("discount__percent"),
                discount_date_end=F("discount__date_end"),
            )
        )
        serializer = BasketSerializer({"products": basket})
        return Response(serializer.data)

    def post(self, request):
        input_serializer = AddProductSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        product = get_object_or_404(Product, id=input_serializer.data.get("product_id"))
        basket, created = Basket.objects.get_or_create(
            user=request.user, product=product
        )
        if created:
            basket.count = input_serializer.data.get("number_of_items")
        else:
            basket.count += input_serializer.data.get("number_of_items")

        if basket.count == 0:
            basket.delete()
        else:
            basket.save()
        return Response()

    def delete(self, request):
        input_serializer = DeleteProductSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        product = get_object_or_404(Product, id=input_serializer.data.get("product_id"))

        Basket.objects.get(user=request.user, product=product).delete()

        return Response()


class OrderView(APIView):
    permission_classes = (IsAuthenticated,)

    @atomic
    def post(self, request):
        input_serializer = OrderSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        order = input_serializer.save()

        return Response(input_serializer.data)
