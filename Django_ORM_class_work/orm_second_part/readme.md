### Django ORM - Продвинутые возможности

Этот проект демонстрирует продвинутые возможности системы ORM (Object-Relational Mapping) в Django, с акцентом на связи «многие ко многим», пользовательские промежуточные модели, а также интеграцию Django Debug Toolbar для отладки и оптимизации производительности. Кроме того, он иллюстрирует, как настроить интерфейс администратора Django с использованием классов InlineModelAdmin для более эффективного управления связанными моделями.

### Возможности

1. **Связи "многие ко многим" с использованием промежуточной модели**: Проект демонстрирует использование пользовательских промежуточных моделей (`OrderPosition`) для добавления дополнительных данных (например, количества) в связи "многие ко многим".
2. **Django Debug Toolbar**: Интегрирована для мониторинга запросов и оптимизации производительности.
3. **Кастомизация админки с помощью Inline**: Использует `TabularInline` в админке Django для управления экземплярами `OrderPosition` непосредственно из интерфейса модели `Order`.

### Модели

### Product

Представляет продукт в магазине.

**Поля:**

- `name`: Название продукта.
- `price`: Цена продукта.
- `category`: Категория, к которой относится продукт.

```python

class Product(models.Model):
    name = CharField(max_length=100)
    price = DecimalField(max_digits=10, decimal_places=2)
    category = CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

```

### Order

Представляет заказ клиента, который может содержать несколько продуктов.

**Поля:**

- `products`: Связь "многие ко многим" с моделью `Product` через модель `OrderPosition`.

```python

class Order(models.Model):
    products = models.ManyToManyField(Product, related_name='orders', through='OrderPosition')

```

### OrderPosition

Пользовательская промежуточная модель, представляющая продукт в заказе с дополнительными атрибутами, такими как количество.

**Поля:**

- `product`: Внешний ключ на модель `Product`.
- `order`: Внешний ключ на модель `Order`.
- `quantity`: Количество продукта в заказе.

```python

class OrderPosition(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='positions')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='positions')
    quantity = IntegerField()

```

### Представления

### list_orders

Представление для отображения заказов и их фильтрации по цене продукта с использованием GET-параметра.

```python

from django.shortcuts import render
from orm_second_part.models import Order, Product, OrderPosition

def list_orders(request):
    orders_filter = request.GET.get('filter')

    if orders_filter:
        try:
            orders_filter = float(orders_filter)
        except ValueError:
            orders_filter = 0
    else:
        orders_filter = 0

    orders = Order.objects.all()

    context = {
        'orders': orders,
        'filter': orders_filter
    }

    return render(request, 'list_orders.html', context)

```

### Шаблоны

### list_orders.html

Отображает список заказов и связанных с ними продуктов, отфильтрованных по указанной цене.

```html
htmlКопировать код
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Orders List</title>
</head>
<body>
    <div>
        <h1>Orders</h1>
        <ul>
            {% for order in orders %}
                <li>Заказ номер: {{ order.id }}.
                    {% if filter %} Фильтр: {{ filter }} {% endif %}
                </li>
                <ol>
                    {% for item in order.positions.all %}
                        {% if filter <= item.product.price %}
                            <li>{{ item.product.name }} - {{ item.product.price }} (кол.: {{ item.quantity }} шт.)</li>
                        {% endif %}
                    {% endfor %}
                </ol>
            {% endfor %}
        </ul>
    </div>
</body>
</html>

```

### Конфигурация администратора

### Регистрация моделей в `admin.py`

Для эффективного управления `Order` и `OrderPosition` через Django admin используется `TabularInline` для отображения экземпляров `OrderPosition` в интерфейсе модели `Order`.

```python

from django.contrib import admin
from .models import Product, Order, OrderPosition

class OrderPositionInline(admin.TabularInline):
    model = OrderPosition
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderPositionInline]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']

@admin.register(OrderPosition)
class OrderPositionAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity']

```

### Отладка и оптимизация с Django Debug Toolbar

Для отладки и оптимизации запросов к базе данных интегрирована Django Debug Toolbar. Этот инструмент помогает выявлять узкие места в производительности, отслеживая SQL-запросы и другие метрики прямо в среде разработки.

### Установка

```bash

pip install django-debug-toolbar

```

### Конфигурация в `settings.py`

```python

INSTALLED_APPS = [
    ...,
    'django.contrib.staticfiles',
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    ...,
]

INTERNAL_IPS = [
    '127.0.0.1',
]

STATIC_URL = '/static/'

```

### Конфигурация URL в `urls.py`

```python

from django.urls import include, path
import debug_toolbar

urlpatterns = [
    ...,
    path('__debug__/', include(debug_toolbar.urls)),
]

```

### Как запустить проект

1. **Клонируйте репозиторий:**
    
    ```bash
    git clone https://github.com/dm-morozov/Netology_27_Django_ORM_classwork.git
    cd Netology_27_Django_ORM_classwork
    
    ```
    
2. **Установите зависимости:**
    
    ```bash
    pip install -r requirements.txt
    
    ```
    
3. **Примените миграции:**
    
    ```bash
    python manage.py migrate
    
    ```
    
4. **Создайте суперпользователя (для доступа к админке):**
    
    ```bash
    python manage.py createsuperuser
    
    ```
    
5. **Запустите сервер:**
    
    ```bash
    python manage.py runserver
    
    ```
    
6. **Доступ к приложению:**
    - Приложение: http://127.0.0.1:8000/orders/
    - Админка: http://127.0.0.1:8000/admin/

### Заключение

Этот проект демонстрирует продвинутые возможности Django ORM, включая пользовательские связи "многие ко многим" и расширенные возможности админки, обеспечивая прочную основу для создания надежных и оптимизированных веб-приложений на Django.