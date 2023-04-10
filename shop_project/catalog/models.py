from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q, F

from users.models import CustomUser


class Cashback(models.Model):
    percent = models.IntegerField()
    threshold = models.IntegerField()

    def __str__(self):
        return f"{self.percent} % - {self.threshold}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Producer(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}; {self.country}"


class Discount(models.Model):
    percent = models.IntegerField()
    name = models.CharField(max_length=100)
    date_start = models.DateField()
    date_end = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.percent}%"


class Product(models.Model):
    name = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    count_on_stock = models.IntegerField()
    articul = models.CharField(max_length=50)
    description = models.TextField()
    discount = models.ForeignKey(
        Discount, on_delete=models.SET_NULL, null=True, blank=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    producer = models.ForeignKey(
        Producer, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.name} - {self.category.name}"


class Promocode(models.Model):
    name = models.CharField(max_length=100)
    percent = models.IntegerField()
    date_start = models.DateField()
    date_end = models.DateField()
    is_cumulative = models.BooleanField()

    def __str__(self):
        return f"{self.name} - {self.percent}%"


class Basket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(null=True)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(count__gte=0),
                name='count',
            ),
        ]


class Order(models.Model):
    DELIVERY_METHOD = (
        ("Courier", "Courier"),
        ("Self-delivery", "Self-delivery"),
        ("Post", "Post"),
        ("Post box", "Post box"),
    )
    DELIVERY_STATUS = (
        ("Paid", "Paid"),
        ("In process", "In process"),
    )

    PAYMENT_METHOD = (
        ("Cash", "Cash"),
        ("Card", "Card"),
        ("Card online", "Card online"),
    )

    PAYMENT_STATUS = (
        ("Paid", "Paid"),
        ("In process", "In process"),
    )
    DELIVERY_NOTIF_IN_TIME = (
        (24, 24),
        (6, 6),
        (1, 1),
    )

    date_created = models.DateTimeField()
    promocode = models.ForeignKey(
        Promocode, on_delete=models.SET_NULL, null=True, blank=True
    )
    delivery_method = models.CharField(
        choices=DELIVERY_METHOD,
        max_length=15,
        default="Self-delivery",
    )
    delivery_address = models.CharField(max_length=256)
    delivery_status = models.CharField(
        choices=DELIVERY_STATUS,
        max_length=15,
        default="In process",
    )
    delivery_notif_in_time = models.IntegerField(
        choices=DELIVERY_NOTIF_IN_TIME,
        null=True,
        default=None,
    )
    payment_method = models.CharField(
        choices=PAYMENT_METHOD,
        max_length=15,
        default="Card",
    )
    payment_status = models.CharField(
        choices=PAYMENT_STATUS,
        max_length=15,
        default="In process",
    )
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True
    )
    result = models.DecimalField(max_digits=15, decimal_places=2)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
