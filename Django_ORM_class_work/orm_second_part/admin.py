from django.contrib import admin
from .models import Product, Order, OrderPosition
# Register your models here.


class OrderPositionInline(admin.TabularInline):
    model = OrderPosition
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ['category']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id']
    inlines = [OrderPositionInline,]