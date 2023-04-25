from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата отримання товару'


    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'eaddress', 'state', 'number_nova_post', 'order_date', 'comment' ,
        )

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логін')
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логін')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())