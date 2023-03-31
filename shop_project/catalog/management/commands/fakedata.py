from datetime import timedelta
from random import randint, choices

import faker_commerce
from django.core.management.base import BaseCommand
from django_seed import Seed
from faker import Faker

from catalog.models import Category, Discount, Producer, Promocode, Product


class Command(BaseCommand):
    help = "Filling database"
    __DEFAULT_COUNT_PRODUCERS = 200
    __DEFAULT_COUNT_CATEGORIES = 75
    __DEFAULT_COUNT_PRODUCTS = 2000
    __DEFAULT_COUNT_PROMOCODES = 250
    __DEFAULT_COUNT_DISCOUNTS = 20

    def __init__(self, *args, **kwargs):
        self.seeder = Seed.seeder()
        self.fake = Faker()
        self.fake.add_provider(faker_commerce.Provider)
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        self.__create_producers()
        self.__create_categories()
        self.__create_discounts()
        self.__create_promocodes()
        self.__create_products()
        return "Fake data is created"

    def __create_producers(self):
        self.seeder.add_entity(
            model=Producer,
            number=self.__DEFAULT_COUNT_PRODUCERS,
            customFieldFormatters={
                "name": lambda x: self.fake.company(),
                "description": lambda x: self.fake.paragraph(nb_sentences=3),
                "country": lambda x: self.fake.country(),
            },
        )
        self.seeder.execute()

    def __create_categories(self):
        self.seeder.add_entity(
            model=Category,
            number=self.__DEFAULT_COUNT_CATEGORIES,
            customFieldFormatters={
                "name": lambda x: self.fake.ecommerce_category(),
                "description": lambda x: self.fake.paragraph(nb_sentences=2),
            },
        )
        self.seeder.execute()

    def __create_discounts(self):
        self.seeder.add_entity(
            model=Discount,
            number=self.__DEFAULT_COUNT_DISCOUNTS,
            customFieldFormatters={
                "percent": lambda x: randint(1, 50),
                "name": lambda x: self.fake.sentence(nb_words=1)[:-1],
                "date_start": lambda x: self.fake.date_this_month(),
                "date_end": lambda x: self.fake.date_this_month()
                + timedelta(days=randint(5, 100)),
            },
        )
        self.seeder.execute()

    def __create_promocodes(self):
        self.seeder.add_entity(
            model=Promocode,
            number=self.__DEFAULT_COUNT_PROMOCODES,
            customFieldFormatters={
                "name": lambda x: self.fake.swift(length=8),
                "percent": lambda x: randint(1, 50),
                "date_start": lambda x: self.fake.date_this_month(),
                "date_end": lambda x: self.fake.date_this_month()
                + timedelta(days=randint(20, 200)),
                "is_cumulative": lambda x: self.fake.pybool(),
            },
        )
        self.seeder.execute()

    def __create_products(self):
        discounts = Discount.objects.all()
        categories = Category.objects.all()
        producers = Producer.objects.all()
        self.seeder.add_entity(
            model=Product,
            number=self.__DEFAULT_COUNT_PRODUCTS,
            customFieldFormatters={
                "name": lambda x: self.fake.ecommerce_name(),
                "price": lambda x: self.fake.ecommerce_price(),
                "count_on_stock": lambda x: randint(100, 10000),
                "articul": lambda x: self.fake.isbn10(),
                "description": lambda x: self.fake.paragraph(nb_sentences=2),
                "discount": lambda x: choices(discounts)[0],
                "category": lambda x: choices(categories)[0],
                "producer": lambda x: choices(producers)[0],
            },
        )
        self.seeder.execute()
