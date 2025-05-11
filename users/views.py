from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import UserLoginForm, UserRegistrationForm, \
    ProfileForm, CarDataForm
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from orders.models import Order, OrderItem
import logging
logger = logging.getLogger(__name__)


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password'] 
            user = auth.authenticate(username=username,
                                     password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:product_list'))
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            logger.info(f"Пользователь {user.username} успешно создан")
            auth.login(request, user)
            messages.success(
                request, f'{user.username}, Successful Registration'
            )
            return HttpResponseRedirect(reverse('user:login'))
        else:
            logger.error(f"Ошибка регистрации: {form.errors}")
            messages.error(request, 'Ошибка регистрации. Проверьте введённые данные.')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/registration.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user,
                           files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile was changed')
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)
    
    orders = Order.objects.filter(user=request.user).prefetch_related(
        Prefetch(
            'items',
            queryset=OrderItem.objects.select_related('product'),
        )
    ).order_by('-id')
    return render(request, 'users/profile.html',
                  {'form': form,
                   'orders': orders})


@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user).prefetch_related(
        Prefetch('items', queryset=OrderItem.objects.select_related('product'))
    ).order_by('-id')
    return render(request, 'users/orders_history.html', {'orders': orders})

@login_required
def car_data_view(request):
    if request.method == 'POST':
        form = CarDataForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные об авто обновлены')
            return HttpResponseRedirect(reverse('users:car_data'))
    else:
        form = CarDataForm(instance=request.user)
    return render(request, 'users/car_data.html', {'form': form})

def logout(request):
    auth.logout(request)
    return redirect(reverse('main:product_list'))
