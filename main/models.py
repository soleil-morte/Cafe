from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

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
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} - {self.price} руб."

class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='ingredients')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)  
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} {self.product.unit}"


class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)  
    seats = models.PositiveIntegerField(default=4)     
    is_occupied = models.BooleanField(default=False)  

    def __str__(self):
        return f"Стол {self.number}"


class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    dishes = models.ManyToManyField(Dish, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    
    def total_price(self):
        return sum(item.total for item in self.order_items.all())
    
    def __str__(self):
        return f"Заказ #{self.id} - Стол {self.table.number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total(self):
        return self.dish.price * self.quantity
    
    def __str__(self):
        return f"{self.dish.name} x{self.quantity}"
