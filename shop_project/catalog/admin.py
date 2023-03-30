from django.contrib import admin

from catalog.models import Category, Discount, Producer, Promocode, Product


admin.site.register(Category)
admin.site.register(Discount)
admin.site.register(Producer)
admin.site.register(Promocode)
admin.site.register(Product)
