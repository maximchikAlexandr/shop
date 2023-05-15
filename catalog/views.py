from django.db.models import F
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404

from drf_yasg.utils import swagger_auto_schema
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

    @swagger_auto_schema(responses={200: CategorySerializer}, tags=["catalog objects"])
    def get(self, request, *args, **kwargs):
        """Get the list of all categories."""
        return super().get(request, *args, **kwargs)


class CategoryProductsListView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        responses={200: ProductSerializer(many=True)}, tags=["products"]
    )
    def get(self, request, category_id):
        queryset = Product.objects.filter(category__id=category_id)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class DiscountProductsListView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        responses={200: ProductSerializer(many=True)}, tags=["products"]
    )
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

    @swagger_auto_schema(responses={200: ProducerSerializer}, tags=["catalog objects"])
    def get(self, request, *args, **kwargs):
        """Get the list of all producers."""
        return super().get(request, *args, **kwargs)


class ProducerProductsListView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        responses={200: ProductSerializer(many=True)}, tags=["products"]
    )
    def get(self, request, producer_id):
        queryset = Product.objects.filter(producer__id=producer_id)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class DiscountListView(ListAPIView):
    queryset = Discount.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = DiscountSerializer

    @swagger_auto_schema(responses={200: DiscountSerializer}, tags=["catalog objects"])
    def get(self, request, *args, **kwargs):
        """Get the list of all dicounts."""
        return super().get(request, *args, **kwargs)


class PromocodesListView(ListAPIView):
    queryset = Promocode.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PromocodeSerializer

    @swagger_auto_schema(responses={200: PromocodeSerializer}, tags=["catalog objects"])
    def get(self, request, *args, **kwargs):
        """Get the list of all promocodes."""
        return super().get(request, *args, **kwargs)


class ProductsListView(ListAPIView):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer

    @swagger_auto_schema(responses={200: PromocodeSerializer}, tags=["products"])
    def get(self, request, *args, **kwargs):
        """Get the list of all products."""
        return super().get(request, *args, **kwargs)


class BasketView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(responses={200: BasketSerializer}, tags=["basket"])
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

    @swagger_auto_schema(
        request_body=AddProductSerializer, responses={200: ""}, tags=["basket"]
    )
    def post(self, request):
        """
        number_of_items > 0 if need sum with current count of the products in basket
        number_of_items < 0 if if need subtqract from current count of the products in basket
        If you subtqract more than user has in teh basket
        """
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

    @swagger_auto_schema(
        request_body=DeleteProductSerializer, responses={200: ""}, tags=["basket"]
    )
    def delete(self, request):
        input_serializer = DeleteProductSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        product = get_object_or_404(Product, id=input_serializer.data.get("product_id"))

        Basket.objects.get(user=request.user, product=product).delete()

        return Response()


class OrderView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=OrderSerializer,
        responses={200: OrderSerializer},
        tags=["catalog objects"],
    )
    def post(self, request):
        input_serializer = OrderSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        order = input_serializer.save()

        return Response(input_serializer.data)
