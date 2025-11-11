from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('menu/', menu_list, name='menu'),
    path('tables/', tables_list, name='tables'),
    path('stock/', stock_list, name='stock'),
    path('orders/', orders_list, name='orders'),
    

]