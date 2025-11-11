from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def index(request):
    context = {
        'dishes_count': Dish.objects.count(),
        'products_count': Product.objects.count(),
        'tables_count': Table.objects.count(),
        'active_orders_count': Order.objects.filter(is_completed=False).count(),
    }
    return render(request, 'index.html', context)

def menu_list(request):
    dishes = Dish.objects.all()
    return render(request, 'menu.html', {'dishes': dishes})

def tables_list(request):
    tables = Table.objects.all()
    return render(request, 'tables.html', {'tables': tables})

def stock_list(request):
    products = Product.objects.all()
    return render(request, 'stock.html', {'products': products})

def orders_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})


