from django.shortcuts import render
from orm_second_part.models import Order, Product, OrderPosition
# Create your views here.


def list_orders(request):
    orders_filter = request.GET.get('filter')

    if orders_filter:
        try:
            orders_filter = float(orders_filter)
            print('Число')
        except ValueError:
            print('НЕ число')
            orders_filter = 0
    else:
        orders_filter = 0
    
    orders = Order.objects.all()

    context = {
        'orders': orders,
        'filter': orders_filter
    }

    return render(request, 'list_orders.html', context)