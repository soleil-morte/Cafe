from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib import messages
from django.http import JsonResponse
from .models import *
from .forms import *

# Create your views here.
def Index(request):
    context = {
        'dishes_count': Dish.objects.count(),
        'products_count': Product.objects.count(),
        'tables_count': Table.objects.count(),
        'active_orders_count': Order.objects.filter(is_completed=False).count(),
    }
    return render(request, 'index.html', context)


# Продукты - CRUD
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продукт успешно добавлен!')
            return redirect('stock')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form, 'title': 'Добавить продукт'})

def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продукт успешно обновлен!')
            return redirect('stock')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form, 'title': 'Редактировать продукт'})

def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_name = product.name
    product.delete()
    messages.success(request, f'Продукт "{product_name}" удален!')
    return redirect('stock')

# Блюда - CRUD
def dish_list(request):
    dishes = Dish.objects.all()
    return render(request, 'dish_list.html', {'dishes': dishes})

def dish_add(request):
    if request.method == 'POST':
        dish_form = DishForm(request.POST)
        formset = DishIngredientFormSet(request.POST)
        if dish_form.is_valid() and formset.is_valid():
            dish = dish_form.save()
            formset.instance = dish
            formset.save()
            messages.success(request, 'Блюдо успешно добавлено!')
            return redirect('menu')
    else:
        dish_form = DishForm()
        formset = DishIngredientFormSet()
    return render(request, 'dish_form.html', {
        'dish_form': dish_form,
        'formset': formset,
        'title': 'Добавить блюдо'
    })

def dish_edit(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    if request.method == 'POST':
        dish_form = DishForm(request.POST, instance=dish)
        formset = DishIngredientFormSet(request.POST, instance=dish)
        if dish_form.is_valid() and formset.is_valid():
            dish_form.save()
            formset.save()
            messages.success(request, 'Блюдо успешно обновлено!')
            return redirect('menu')
    else:
        dish_form = DishForm(instance=dish)
        formset = DishIngredientFormSet(instance=dish)
    return render(request, 'dish_form.html', {
        'dish_form': dish_form,
        'formset': formset,
        'title': 'Редактировать блюдо'
    })

def dish_delete(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    dish_name = dish.name
    dish.delete()
    messages.success(request, f'Блюдо "{dish_name}" удалено!')
    return redirect('menu')

def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    ingredients = dish.ingredients.all()
    
    cost = 0
    ingredients_with_cost = []
    
    for ingredient in ingredients:
        # Теперь quantity - float, purchase_price - Decimal
        ingredient_cost = ingredient.quantity * float(ingredient.product.purchase_price)
        cost += ingredient_cost
        ingredients_with_cost.append({
            'ingredient': ingredient,
            'cost': ingredient_cost
        })
    
    profit = float(dish.price) - cost
    
    return render(request, 'dish_detail.html', {
        'dish': dish,
        'ingredients_with_cost': ingredients_with_cost,
        'cost': cost,
        'profit': profit
    })

# Столы - CRUD
def tables_list(request):
    tables = Table.objects.all()
    return render(request, 'tables.html', {'tables': tables})

def table_add(request):
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Стол успешно добавлен!')
            return redirect('tables')
    else:
        form = TableForm()
    return render(request, 'table_form.html', {'form': form, 'title': 'Добавить стол'})

def table_edit(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    if request.method == 'POST':
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            messages.success(request, 'Стол успешно обновлен!')
            return redirect('tables')
    else:
        form = TableForm(instance=table)
    return render(request, 'table_form.html', {'form': form, 'title': 'Редактировать стол'})

def table_delete(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    table_number = table.number
    table.delete()
    messages.success(request, f'Стол #{table_number} удален!')
    return redirect('tables')

def table_toggle(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    table.is_occupied = not table.is_occupied
    table.save()
    
    status = "занят" if table.is_occupied else "свободен"
    messages.success(request, f'Стол #{table.number} теперь {status}')
    return redirect('tables')

# Заказы
def orders_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})

def order_create(request):
    messages.info(request, 'Функция создания заказа в разработке')
    return redirect('orders')