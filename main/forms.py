from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(  # Добавляем поле username
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email manzilingiz'
        })
    )
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'To\'liq ismingiz'
        })
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+998901234567'
        })
    )
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Lavozim'
    )

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'phone', 'role', 'password1', 'password2']
    
    
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parol'
        })
    )

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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unit'].choices = Product._meta.get_field('unit').choices

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'price', 'image', 'portions']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название блюда'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Описание блюда'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'portions': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 0,
                'placeholder': 'Планируемое количество на день'
            }),
        }

class DishIngredientForm(forms.ModelForm):
    class Meta:
        model = DishIngredient
        fields = ['product', 'quantity', 'unit']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
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
            'number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Номер стола'}),
            'seats': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Количество мест'}),
            'is_occupied': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_number(self):
        number = self.cleaned_data['number']
        if Table.objects.filter(number=number).exists():
            raise forms.ValidationError("Стол с таким номером уже существует")
        return number
    
    
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_type', 'table', 'customer_name', 'phone_number', 'address']
        widgets = {
            'order_type': forms.Select(attrs={'class': 'form-control'}),
            'table': forms.Select(attrs={'class': 'form-control'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя клиента'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер телефона'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Адрес доставки'}),
        }