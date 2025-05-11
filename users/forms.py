from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import User

class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="Имя")
    last_name = forms.CharField(required=True, label="Фамилия")
    username = forms.CharField(required=True, label="Имя пользователя")
    email = forms.EmailField(required=True, label="Почта")
    phone = forms.CharField(required=False, label="Телефон")
    
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
            'password1',
            'password2',
        )


class ProfileForm(UserChangeForm):
    image = forms.ImageField(required=False, label="Фото")
    first_name = forms.CharField(required=True, label="Имя")
    last_name = forms.CharField(required=True, label="Фамилия")
    username = forms.CharField(required=True, label="Имя пользователя")
    email = forms.EmailField(required=True, label="Почта")
    phone = forms.CharField(required=False, label="Телефон")
    car_brand = forms.CharField(required=False, label="Марка авто")
    car_year = forms.IntegerField(required=False, label="Год авто")
    car_number = forms.CharField(required=False, label="Гос. номер авто")
    vin_code = forms.CharField(required=False, label="VIN код авто")
    
    class Meta:
        model = User
        fields = (
            'image',
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
            'car_brand',
            'car_year',
            'car_number',
            'vin_code',
        )

class CarDataForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('car_brand', 'car_year', 'car_number', 'vin_code')
        labels = {
            'car_brand': "Марка авто",
            'car_year': "Год авто",
            'car_number': "Гос. номер авто",
            'vin_code': "VIN код авто",
        }
