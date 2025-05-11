from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from main.models import Product
from .models import Favorite
from django.contrib import messages

@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            product=product
        )
        if not created:
            favorite.delete()
            messages.success(request, 'Товар успешно удален из избранного')
        else:
            messages.success(request, 'Товар добавлен в избранное')
    except Exception as e:
        messages.error(request, f'Ошибка: {str(e)}')
    
    return redirect(request.META.get('HTTP_REFERER', 'main:index'))

@login_required
def favorites_list(request):
    user_favorites = Favorite.objects.filter(user=request.user).select_related('product')
    products = [fav.product for fav in user_favorites]
    return render(request, 'favorites/favorites_list.html', {'products': products})
