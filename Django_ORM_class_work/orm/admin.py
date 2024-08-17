from django.contrib import admin
from .models import Car, Person
# Register your models here.


class PersonInline(admin.TabularInline):
    model = Person
    extra = 1

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines = [PersonInline]
    list_display = ['id', 'brand', 'model', 'color']
    list_filter = ['brand', 'model']
    list_editable = ['color']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_car_brand', 'get_car_model']
    list_filter = ['car__brand', 'car__model']

    def get_car_brand(self, obj):
        return obj.car.brand  # Доступ к полю car для вывода brand
    get_car_brand.short_description = 'Brand'  # Описание столбца в админке

    def get_car_model(self, obj):
        return obj.car.model
    get_car_model.short_description = 'Model'


