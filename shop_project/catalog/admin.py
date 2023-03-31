from jedi.api.refactoring import inline

from catalog.models import Cashback, Category, Discount, Producer, Product, Promocode, Order, OrderProduct

from django.contrib import admin


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class CashbackAdmin(admin.ModelAdmin):
    list_display = ("percent", "threshold")


class ProducerAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    search_fields = ("name", "country")


class DiscountAdmin(admin.ModelAdmin):
    list_display = ("name", "percent", "date_start", "date_end")
    search_fields = ("name", "percent")


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "count_on_stock", "articul", "category", "producer")
    search_fields = ("name", "articul", "category__name", "producer__name")
    list_select_related = ("category", "producer")


class PromocodetAdmin(admin.ModelAdmin):
    list_display = ("name", "percent", "date_start", "date_end", "is_cumulative")
    search_fields = ("name",)


class OrderProductsInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ("price", )

    def price(self, obj):
        return obj.product.price


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "date_created", "delivery_notif_in_time", "user", "result",
                    "delivery_status", "payment_status")
    search_fields = ("id", "user__name")
    inlines = [OrderProductsInline]
    list_select_related = ("user", )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Cashback, CashbackAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Producer, ProducerAdmin)
admin.site.register(Promocode, PromocodetAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
