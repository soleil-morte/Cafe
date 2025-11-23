from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Menejer'),
        ('waiter', 'Ofitsiant'),
        ('cook', 'Oshpaz'),
        ('chef', 'Bosh Oshpaz'),
        ('cashier', 'Kassir'),
        ('storekeeper', 'Omborchi'),
    ]
    
    phone_regex = RegexValidator(
        regex=r'^\+998\d{9}$',
        message="Telefon raqam +998xxxxxxx formatida bo'lishi kerak."
    )
    
    phone = models.CharField(max_length=13, unique=True, null=True, blank=True, validators=[phone_regex])
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=120)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='waiter')
    date_joined = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if self.phone:
            cleaned_number = ''.join(filter(str.isdigit, self.phone))
            if cleaned_number.startswith('998') and len(cleaned_number) == 12:
                self.phone = f"+{cleaned_number}"
            elif not cleaned_number.startswith('+998'):
                raise ValueError("Telefon raqam noto'g'ri formatda")
            
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"

    # Методы для проверки ролей
    def is_administrator(self):
        return self.role == 'admin'
    
    def is_manager(self):
        return self.role == 'manager'
    
    def is_waiter(self):
        return self.role == 'waiter'
    
    def is_cook(self):
        return self.role == 'cook'
    
    def is_chef(self):
        return self.role == 'chef'
    
    def is_cashier(self):
        return self.role == 'cashier'
    
    def is_storekeeper(self):
        return self.role == 'storekeeper'

    class Meta:
        swappable = 'AUTH_USER_MODEL'
     
        
class Product(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20, choices=[
        ('kg', 'кг'), ('liters', 'л'), ('pieces', 'шт'), ('g', 'г')
    ])
    quantity = models.FloatField(default=0)
    reserved_quantity = models.FloatField(default=0)  # Новое поле для резервирования
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"
    
    def available_quantity(self):
        """Доступное количество (общее - зарезервированное)"""
        return max(0, self.quantity - self.reserved_quantity)
    
    def reserve(self, amount):
        """Зарезервировать количество"""
        if amount <= 0:
            return True
            
        if self.available_quantity() >= amount:
            self.reserved_quantity += amount
            self.save()
            return True
        return False
    
    def release_reservation(self, amount):
        """Освободить резервирование"""
        self.reserved_quantity = max(0, self.reserved_quantity - amount)
        self.save()
    
    def commit_reservation(self, amount):
        """Подтвердить резервирование - списать продукты"""
        if amount <= self.reserved_quantity:
            self.quantity -= amount
            self.reserved_quantity -= amount
            self.save()
            return True
        return False

class Dish(models.Model):
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    portions = models.PositiveIntegerField(default=0, verbose_name='Доступные порции')
    
    def __str__(self):
        return f"{self.name} - {self.price} сум."
    
    def add_portions(self, quantity):
        """Добавить порции и списать продукты со склада"""
        # Проверяем хватает ли продуктов
        for ingredient in self.ingredients.all():
            required_quantity = ingredient.get_quantity_in_product_units() * quantity
            if ingredient.product.quantity < required_quantity:
                return False, f"Недостаточно {ingredient.product.name}"
        
        # Списываем продукты
        for ingredient in self.ingredients.all():
            required_quantity = ingredient.get_quantity_in_product_units() * quantity
            ingredient.product.quantity -= required_quantity
            ingredient.product.save()
        
        # Добавляем порции
        self.portions += quantity
        self.save()
        return True, "Успешно"
    
    def use_portions(self, quantity):
        """Использовать порции для заказа"""
        if self.portions >= quantity:
            self.portions -= quantity
            self.save()
            return True
        return False

class DishIngredient(models.Model):
    UNIT_CHOICES = [
        ('kg', 'кг'), ('g', 'г'), ('liters', 'л'), ('ml', 'мл'), ('pieces', 'шт'),
    ]
    
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='ingredients')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='g')
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} {self.get_unit_display()}"
    
    def get_quantity_in_product_units(self):
        """Конвертирует количество в единицы измерения продукта на складе"""
        if self.unit == self.product.unit:
            return self.quantity
        
        conversion_rates = {
            ('kg', 'g'): 1000, ('g', 'kg'): 0.001,
            ('liters', 'ml'): 1000, ('ml', 'liters'): 0.001,
            ('pieces', 'kg'): 0.1, ('kg', 'pieces'): 10,
            ('pieces', 'g'): 100, ('g', 'pieces'): 0.01,
        }
        
        rate = conversion_rates.get((self.unit, self.product.unit))
        if rate:
            return self.quantity * rate
        else:
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
