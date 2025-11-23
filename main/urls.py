from django.urls import path
from .views import *

urlpatterns = [
   path('', Index, name='index'),
    
     # Продукты
    path('stock/', product_list, name='stock'),
    path('stock/add/', product_add, name='product_add'),
    path('stock/<int:product_id>/edit/', product_edit, name='product_edit'),
    path('stock/<int:product_id>/delete/', product_delete, name='product_delete'),
    
    # Блюда
    path('menu/', dish_list, name='menu'),
    path('menu/add/', dish_add, name='dish_add'),
    path('menu/<int:dish_id>/', dish_detail, name='dish_detail'),
    path('menu/<int:dish_id>/edit/', dish_edit, name='dish_edit'),
    path('menu/<int:dish_id>/delete/', dish_delete, name='dish_delete'),
    
    # Столы
    path('tables/', tables_list, name='tables'),
    path('tables/add/', table_add, name='table_add'),
    path('tables/<int:table_id>/edit/', table_edit, name='table_edit'),
    path('tables/<int:table_id>/delete/', table_delete, name='table_delete'),
    path('tables/<int:table_id>/toggle/', table_toggle, name='table_toggle'), 
    path('tables/<int:table_id>/order/', table_order, name='table_order'), 
    
    # Заказы
    path('orders/', orders_list, name='orders'),
    path('orders/create/', order_create, name='order_create'),
    path('orders/<int:order_id>/', table_order, name='table_order_by_id'), 
    path('orders/<int:order_id>/delete/', order_delete, name='order_delete'),
    
    # Регистрация
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    path('dish/<int:dish_id>/add-portions/', add_portions, name='add_portions'),
]


# Функция для обратной совместимости
def table_order_legacy(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    # Создаем заказ для стола
    order = Order.objects.create(
        order_type='dine_in',
        table=table
    )
    # Занимаем стол
    table.is_occupied = True
    table.save()
    
    return redirect('table_order', order_id=order.id)