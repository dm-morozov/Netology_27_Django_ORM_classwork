# Знакомство с Django ORM

## Описание

Этот проект демонстрирует использование Django ORM для создания и работы с моделями, представлениями и административной панелью Django. В проекте реализованы две модели: `Car` (машина) и `Person` (персона). Модели связаны между собой через отношение `ForeignKey`, где каждая персона связана с машиной. В проекте показано:

- Создание моделей Django
- Настройка административной панели для управления моделями
- Создание представлений для работы с моделями
- Фильтрация и запросы данных с использованием Django ORM

---

## Структура проекта

### Модели

Проект содержит две основные модели:

- **Car (Машина)**
    
    ```python
    
    class Car(models.Model):
        brand = models.CharField(max_length=50)
        model = models.CharField(max_length=50)
        color = models.CharField(max_length=20)
    
    ```
    
- **Person (Персона)**
    
    ```python
    
    class Person(models.Model):
        name = models.CharField(max_length=50)
        car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='owners')
    
    ```
    

Модель `Car` представляет машину с полями `brand` (бренд), `model` (модель) и `color` (цвет). Модель `Person` представляет человека с полем `name` (имя) и связью с машиной через `ForeignKey`. Атрибут `related_name='owners'` позволяет получать всех владельцев машины через модель `Car`.

---

### Настройка административной панели

Для удобного управления данными через административную панель Django, модели зарегистрированы в файле `admin.py`.

- **CarAdmin**: Управление объектами модели `Car` с отображением и редактированием связанных объектов `Person` напрямую с админ-страницы машины.
    
    ```python
    
    class PersonInline(admin.TabularInline):
        model = Person
        extra = 1
    
    @admin.register(Car)
    class CarAdmin(admin.ModelAdmin):
        inlines = [PersonInline]
        list_display = ['id', 'brand', 'model', 'color']
        list_filter = ['brand', 'model']
        list_editable = ['color']
    
    ```
    
- **PersonAdmin**: Отображение связанных с персонами машин, таких как бренд и модель.
    
    ```python
    
    @admin.register(Person)
    class PersonAdmin(admin.ModelAdmin):
        list_display = ['id', 'name', 'get_car_brand', 'get_car_model']
        list_filter = ['car__brand', 'car__model']
    
        def get_car_brand(self, obj):
            return obj.car.brand
        get_car_brand.short_description = 'Brand'
    
        def get_car_model(self, obj):
            return obj.car.model
        get_car_model.short_description = 'Model'
    
    ```
    

---

### Представления (Views)

Представления служат для работы с данными моделей и включают следующие функции:

- **create_car**: Создание случайной машины и сохранение её в базе данных.
    
    ```python
    
    def create_car(request):
        car = Car(
            brand=random.choice(["BMW", "Audi", "Volkswagen"]),
            model=random.choice(["X5", "A6", "Passat"]),
            color=random.choice(["red", "blue", "green"]),
        )
        car.save()
        return HttpResponse(f"Добавлена новая машина: {car.brand} {car.model} {car.color}")
    
    ```
    
- **list_cars**: Список всех машин с указанием владельцев.
    
    ```python
    
    def list_cars(request):
        cars_objects = Car.objects.all()
        cars = []
        for car in cars_objects:
            owners = ', '.join([owners.name for owners in car.owners.all()])
            cars.append(f"{car.id}: {car.brand} {car.model} {car.color} | Владельцы: {owners}")
        return HttpResponse('<br>'.join(cars))
    
    ```
    
- **list_cars_filter**: Фильтрация машин по бренду (например, "BMW").
    
    ```python
    
    def list_cars_filter(request):
        cars_objects = Car.objects.filter(brand="BMW")
        cars = [f"{car.id}: {car.brand} {car.model} {car.color}" for car in cars_objects]
        return HttpResponse('<br>'.join(cars))
    
    ```
    
- **list_cars_filter_contains**: Фильтрация машин по наличию определённой строки в модели.
    
    ```python
    
    def list_cars_filter_contains(request):
        cars_objects = Car.objects.filter(model__contains="5")
        cars = [f"{car.id}: {car.brand} {car.model} {car.color}" for car in cars_objects]
        return HttpResponse('<br>'.join(cars))
    
    ```
    
- **create_person**: Создание персоны для каждой существующей машины в базе данных.
    
    ```python
    
    def create_person(request):
        cars = Car.objects.all()
        for car in cars:
            person = Person.objects.create(name=f"Person {car.id}", car=car)
        return HttpResponse(f"Все получилось! Персоны: {[p.name for p in Person.objects.all()]}")
    
    ```
    
- **list_persons**: Список всех персон с указанием их машин.
    
    ```python
    
    def list_persons(request):
        person_objects = Person.objects.all()
        persons = [f"{person.id}: {person.name} {person.car.brand} {person.car.model} {person.car.color}" for person in person_objects]
        return HttpResponse('<br>'.join(persons))
    
    ```
    

---

### Фильтрация и модификаторы запросов

В проекте используются различные модификаторы запросов Django ORM, такие как:

- `filter(brand="BMW")`
- `filter(model__contains="5")`

Эти фильтры позволяют осуществлять выборку записей на основе заданных условий.

---

## Связанные концепции

### ForeignKey и related_name

Поле `ForeignKey` определяет отношение "многие-к-одному" между моделями `Person` и `Car`. Атрибут `related_name='owners'` позволяет через объект машины получить всех её владельцев.

### Inlines в административной панели

С помощью `TabularInline` можно управлять связанными моделями (например, объектами `Person`) непосредственно на странице редактирования модели `Car` в административной панели.

---

## Как настроить проект

1. Создайте модели `Car` и `Person` в проекте Django.
2. Зарегистрируйте модели в административной панели и настройте их отображение.
3. Напишите представления для создания, фильтрации и отображения данных моделей.
4. Используйте запросы Django ORM для выборки и фильтрации данных.

---

### Заключение

Этот проект демонстрирует основные принципы работы с Django ORM, включая создание и настройку моделей, представлений и админ-панели. Мы изучили способы создания и управления отношениями между моделями, фильтрации данных и отображения информации в административной панели. Такой подход позволяет быстро разрабатывать и поддерживать веб-приложения на базе Django.

---

## Что изучили

- Основы работы с моделями Django (создание моделей и связи между ними)
- Использование `ForeignKey` для связывания объектов
- Настройка административной панели через классы `ModelAdmin` и `Inlines`
- Использование фильтров и модификаторов запросов в Django ORM для выборки данных
- Создание и обработка запросов в представлениях


## Работа с ORM (2 часть)

### Что мы изучили

На этом занятии мы углубленно изучили продвинутые возможности Django ORM (Object-Relational Mapping). Мы рассмотрели следующие концепции:

1. **Связь "многие ко многим" (Many-to-Many)**:
    - Изучили, как устанавливать связи "многие ко многим" между моделями в Django.
    - Узнали, как использовать параметр `through` для создания промежуточной модели, чтобы добавить дополнительные данные (например, количество) к связи "многие ко многим".
2. **Django Debug Toolbar**:
    - Рассмотрели установку и настройку Django Debug Toolbar для мониторинга SQL-запросов и оптимизации производительности приложения.
    - Научились использовать эту библиотеку для отладки запросов и выявления узких мест в приложении.
3. **Кастомизация админки с помощью Inline**:
    - Изучили использование `TabularInline` и `StackedInline` в Django Admin для отображения и редактирования связанных объектов (моделей) на одной странице в интерфейсе администратора.
    - Рассмотрели, как добавить и настроить отображение промежуточных моделей в админке для удобного управления данными.

### Что мы сделали

1. **Создание моделей**:
    - Создали модель `Product` для представления продуктов в базе данных с полями `name`, `price` и `category`.
    - Создали модель `Order` для представления заказов, связав её с моделью `Product` через связь "многие ко многим" с использованием промежуточной модели `OrderPosition`.
    - Создали промежуточную модель `OrderPosition` для хранения дополнительных данных о продуктах в заказе (например, количество товара).
2. **Настройка представлений (Views)**:
    - Создали представление `list_orders` для отображения списка заказов и фильтрации продуктов по цене. Использовали GET параметр `filter` для фильтрации.
3. **Создание шаблонов (Templates)**:
    - Разработали HTML-шаблон `list_orders.html` для отображения списка заказов и связанных продуктов с учетом фильтрации по цене.
4. **Кастомизация Django Admin**:
    - Настроили Django Admin для управления моделями `Product`, `Order` и `OrderPosition`.
    - Использовали `TabularInline` для отображения `OrderPosition` прямо в админке заказов (`OrderAdmin`), что позволяет удобно редактировать связанные объекты.
5. **Интеграция Django Debug Toolbar**:
    - Установили и настроили Django Debug Toolbar для отладки и мониторинга SQL-запросов.
    - Добавили нужные настройки в `settings.py` и `urls.py` для корректной работы Django Debug Toolbar в проекте.

### Как запустить проект

1. **Клонировать репозиторий**:
    
    ```bash
    git clone https://github.com/dm-morozov/Netology_27_Django_ORM_classwork.git
    cd Netology_27_Django_ORM_classwork
    
    ```
    
2. **Установить зависимости**:
    ```bash
    pip install -r requirements.txt
    
    ```
    
3. **Применить миграции**:
    ```bash

    python manage.py migrate
    
    ```
    
4. **Создать суперпользователя** (для доступа к админке):
    ```bash

    python manage.py createsuperuser
    
    ```
    
5. **Запустить сервер**:
    ```bash

    python manage.py runserver
    
    ```
    
6. **Доступ к приложению**:
    - Приложение: http://127.0.0.1:8000/orders/
    - Админка: http://127.0.0.1:8000/admin/

### Вывод

На этом занятии мы изучили продвинутые возможности Django ORM, включая создание и использование промежуточных моделей, кастомизацию админки и интеграцию инструментов отладки, что позволяет создавать более мощные и оптимизированные веб-приложения на Django