"""
URL configuration for Django_ORM_class_work project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from orm.views import create_car, list_cars, list_cars_filter, list_cars_filter_contains, create_person, list_persons
from orm_second_part.views import list_orders

import debug_toolbar
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('new_car/', create_car),
    path('list_cars/', list_cars),
    path('cars_filter/', list_cars_filter),
    path('cars_contains/', list_cars_filter_contains),
    path('create_person/', create_person),
    path('list_persons/', list_persons),
    path('orders/', list_orders, name='list_orders'),


    path('__debug__/', include(debug_toolbar.urls)),
]
