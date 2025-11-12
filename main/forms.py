from django import forms
from .models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'unit', 'quantity', 'purchase_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название продукта'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название блюда'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Описание блюда'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class DishIngredientForm(forms.ModelForm):
    class Meta:
        model = DishIngredient
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
        }

DishIngredientFormSet = forms.inlineformset_factory(
    Dish, DishIngredient, 
    form=DishIngredientForm,
    extra=10,
    can_delete=True
)

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['number', 'seats', 'is_occupied']
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_occupied': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }