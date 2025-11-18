from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.
        
class Product(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20, choices=[
        ('kg', 'кг'),
        ('liters', 'л'), 
        ('pieces', 'шт'),
        ('grams', 'г')
    ])
    quantity = models.FloatField(default=0) 
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"

class Dish(models.Model):
    image = models.ImageField( upload_to='dishes/', blank=True, null=True,)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} - {self.price} сум."

class DishIngredient(models.Model):
    UNIT_CHOICES = [
        ('kg', 'кг'),
        ('g', 'г'), 
        ('liters', 'л'),
        ('ml', 'мл'),
        ('pieces', 'шт'),
    ]
    
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='ingredients')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='g') 
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} {self.get_unit_display()}"
    
    def get_quantity_in_product_units(self):
        """Конвертирует количество в единицы измерения продукта на складе"""
        # Если единицы совпадают, возвращаем как есть
        if self.unit == self.product.unit:
            return self.quantity
        
        # Таблица конвертации
        conversion_rates = {
            # кг ↔ г
            ('kg', 'g'): 1000,
            ('g', 'kg'): 0.001,
            # литры ↔ мл
            ('liters', 'ml'): 1000,
            ('ml', 'liters'): 0.001,
            # штуки (предполагаем средний вес)
            ('pieces', 'kg'): 0.1,    # 1 шт ≈ 0.1 кг
            ('kg', 'pieces'): 10,     # 1 кг ≈ 10 шт
            ('pieces', 'g'): 100,     # 1 шт ≈ 100 г
            ('g', 'pieces'): 0.01,    # 1 г ≈ 0.01 шт
        }
        
        rate = conversion_rates.get((self.unit, self.product.unit))
        if rate:
            return self.quantity * rate
        else:
            # Если конвертация не определена, возвращаем исходное количество
            return self.quantity


class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)  
    seats = models.PositiveIntegerField(default=4)     
    is_occupied = models.BooleanField(default=False)  

    def __str__(self):
        return f"Стол {self.number}"


class Order(models.Model):
    ORDER_TYPES = [
        ('dine_in', 'В зале'),
        ('takeaway', 'Навынос'),
        ('delivery', 'Доставка'),
    ]
    
    order_type = models.CharField(max_length=20, choices=ORDER_TYPES, default='dine_in')
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True) 
    customer_name = models.CharField(max_length=100, blank=True, verbose_name='Имя клиента')
    phone_number = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    address = models.TextField(blank=True, verbose_name='Адрес доставки')
    dishes = models.ManyToManyField(Dish, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    
    def total_price(self):
        total = Decimal('0')
        for item in self.order_items.all():
            total += item.dish.price * item.quantity
        return total
    
    def __str__(self):
        if self.table:
            return f"Заказ #{self.id} - Стол {self.table.number}"
        elif self.customer_name:
            return f"Заказ #{self.id} - {self.customer_name}"
        else:
            return f"Заказ #{self.id} - {self.get_order_type_display()}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total(self):
        return self.dish.price * self.quantity
    
    def __str__(self):
        return f"{self.dish.name} x{self.quantity}"
