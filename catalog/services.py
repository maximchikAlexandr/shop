from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from catalog.models import Discount
from users.models import CustomUser


class EmailSender:
    COUNT_PRODUCTS = 3
    HTML_TEMPLATE = "catalog/receipt_email.html"

    def __get_products_for_newsletter(self):
        random_discount = (
            Discount.objects
            .filter(date_end__gte=datetime.now())
            .order_by("?")
            .first()
        )

        products = (
            random_discount.product_set
            .only("name", "description", "price")
            .order_by("?")[: self.COUNT_PRODUCTS]
        )
        return products

    @staticmethod
    def __get_emails_for_newsletter():
        return [
            user.email
            for user in (
                CustomUser.objects.filter(discounts_newsletter=True).only("email")
            )
        ]

    def send_newsletter(self):
        emails = self.__get_emails_for_newsletter()
        products = self.__get_products_for_newsletter()
        html_message = render_to_string(
           self.HTML_TEMPLATE, context={"products": products}
        )
        plain_message = strip_tags(html_message)
        send_mail(
            subject="Actual discounts",
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails,
            fail_silently=False,
            auth_user=None,
            auth_password=None,
            connection=None,
            html_message=html_message,
        )
