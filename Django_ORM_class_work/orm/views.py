from django.shortcuts import render
from django.http import HttpResponse
from orm.models import Car, Person
import random

# Create your views here.

def create_car(request):
    car = Car(
        brand=random.choice(["BMW", "Audi", "Volkswagen"]),
        model=random.choice(["X5", "A6", "Passat"]),
        color=random.choice(["red", "blue", "green"]),
        )
    car.save()
    return HttpResponse(f"Добавлена новая машина: {car.brand} {car.model} {car.color}")



def list_cars(request):
    cars_objects = Car.objects.all()
    cars = []
    for car in cars_objects:
        owners =  ', '.join([owners.name for owners in car.owners.all()])
        cars.append(f"{car.id}: {car.brand} {car.model} {car.color} | Владельцы: {owners}")
    return HttpResponse('<br>'.join(cars))


def list_cars_filter(request):
    cars_objects = Car.objects.filter(brand="BMW")
    cars = [f"{car.id}: {car.brand} {car.model} {car.color}" for car in cars_objects]
    return HttpResponse('<br>'.join(cars))


def list_cars_filter_contains(request):
    cars_objects = Car.objects.filter(model__contains="5")
    cars = [f"{car.id}: {car.brand} {car.model} {car.color}" for car in cars_objects]
    return HttpResponse('<br>'.join(cars))


def create_person(request):
    cars = Car.objects.all()
    for car in cars:
        person = Person.objects.create(name=f"Person {car.id}", car=car)
    return HttpResponse(f"Все получилось! Персоны: {[p.name for p in Person.objects.all()]}")


def list_persons(request):
    person_objects = Person.objects.all()
    person = [f"{person.id}: {person.name} {person.car.brand} {person.car.model} {person.car.color}" for person in person_objects]
    return HttpResponse('<br>'.join(person))