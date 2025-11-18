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
        dish_form = DishForm(request.POST, request.FILES)  # Добавляем request.FILES!
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
        dish_form = DishForm(request.POST, request.FILES, instance=dish)  # Добавляем request.FILES!
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
    if request.method == 'POST':
        order = Order.objects.create(
            order_type=request.POST.get('order_type', 'takeaway'),
            customer_name=request.POST.get('customer_name', ''),
            phone_number=request.POST.get('phone_number', ''),
            address=request.POST.get('address', ''),
        )
        messages.success(request, f'Заказ #{order.id} создан!')
        return redirect('table_order_by_id', order_id=order.id)
    
    return render(request, 'order_create.html', {
        'title': 'Создать заказ'
    })


def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_number = order.id
    order.delete()
    messages.success(request, f'Заказ #{order_number} удален!')
    return redirect('orders')



def table_order(request, table_id=None, order_id=None):
    # Поддерживаем оба варианта: по table_id и по order_id
    if table_id:
        # Старый вариант: создаем заказ для стола
        table = get_object_or_404(Table, id=table_id)
        order, created = Order.objects.get_or_create(
            table=table,
            is_completed=False
        )
        
        # Если заказ создан впервые, занимаем стол
        if created and not table.is_occupied:
            table.is_occupied = True
            table.save()
            messages.success(request, f'Стол {table.number} теперь занят!')
    else:
        # Новый вариант: работа с существующим заказом
        order = get_object_or_404(Order, id=order_id)
    
    dishes = Dish.objects.all()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_item':
            dish_id = request.POST.get('dish_id')
            quantity = int(request.POST.get('quantity', 1))
            
            dish = get_object_or_404(Dish, id=dish_id)
            
            # Добавляем блюдо в заказ
            order_item, created = OrderItem.objects.get_or_create(
                order=order,
                dish=dish,
                defaults={'quantity': quantity}
            )
            
            if not created:
                order_item.quantity += quantity
                order_item.save()
                
            messages.success(request, f'{dish.name} заказ добавлен!')
            
        elif action == 'update_quantity':
            order_item_id = request.POST.get('order_item_id')
            quantity = int(request.POST.get('quantity', 1))
    
            print(f"Updating item {order_item_id} to quantity {quantity}")  # Для дебага
    
            try:
                order_item = OrderItem.objects.get(id=order_item_id, order=order)
                if quantity >= 1:
                    order_item.quantity = quantity
                    order_item.save()
                    print(f"Successfully updated to {quantity}")
                else:
                    order_item.delete()
                    print("Item deleted")
            except OrderItem.DoesNotExist:
                print("Item not found")
                messages.error(request, 'Позиция не найдена')
                
        elif action == 'remove_item':
            order_item_id = request.POST.get('order_item_id')
            OrderItem.objects.filter(id=order_item_id, order=order).delete()
            messages.success(request, 'Блюдо удалено из заказа!')
            
        elif action == 'complete_order':
            # Списание продуктов со склада
            success = deduct_products_from_stock(order)
            
            if success:
                # Завершаем заказ
                order.is_completed = True
                order.save()
                
                # Освобождаем стол если он был занят
                if order.table:
                    order.table.is_occupied = False
                    order.table.save()
                
                messages.success(request, f'Заказ #{order.id} завершен! Продукты списаны со склада.')
            else:
                messages.error(request, 'Недостаточно продуктов на складе для завершения заказа!')
            
            return redirect('orders')
            
        if table_id:
            return redirect('table_order', table_id=table_id)
        else:
            return redirect('table_order_by_id', order_id=order.id)  # Исправлено: order.id вместо order_id
    
    order_items = order.order_items.all()
    
    # Расчет суммы заказа с чаевыми
    subtotal = order.total_price()
    service_fee = subtotal * Decimal('0.10')
    total_with_service = subtotal + service_fee
    
    context = {
        'order': order,
        'dishes': dishes,
        'order_items': order_items,
        'subtotal': subtotal,
        'service_fee': service_fee,
        'total_with_service': total_with_service,
    }
    
    # Если это заказ без стола, передаем table как None
    if not table_id:
        context['table'] = None
    else:
        context['table'] = table
    
    return render(request, 'table_order.html', context)

def deduct_products_from_stock(order):
    # Списание продуктов со склада на основе заказа с конвертацией единиц
    try:
        products_to_deduct = {}
        
        # Проходим по всем позициям заказа
        for order_item in order.order_items.all():
            dish = order_item.dish
            quantity_ordered = order_item.quantity
            
            # Проходим по всем ингредиентам блюда
            for ingredient in dish.ingredients.all():
                product = ingredient.product
                
                # Конвертируем количество в единицы продукта на складе
                quantity_needed = ingredient.get_quantity_in_product_units() * quantity_ordered
                
                # Добавляем к общему количеству для списания
                if product.id in products_to_deduct:
                    products_to_deduct[product.id] += quantity_needed
                else:
                    products_to_deduct[product.id] = quantity_needed
        
        # Проверяем достаточно ли продуктов на складе
        for product_id, quantity_needed in products_to_deduct.items():
            product = Product.objects.get(id=product_id)
            if product.quantity < quantity_needed:
                return False  # Недостаточно продуктов
        
        # Списание продуктов
        for product_id, quantity_needed in products_to_deduct.items():
            product = Product.objects.get(id=product_id)
            product.quantity = max(0, product.quantity - quantity_needed)
            product.save()
        
        return True
        
    except Exception as e:
        print(f"Ошибка при списании продуктов: {e}")
        return False