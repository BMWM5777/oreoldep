from django.shortcuts import render, redirect, \
    get_object_or_404
from django.views.decorators.http import require_POST
from main.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.conf import settings

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart-detail.html', {'cart': cart})

@require_POST
def cart_update(request, product_id):
    action = request.POST.get('action')
    product = get_object_or_404(Product, id=product_id)
    
    # Получаем корзину через ключ, заданный в настройках (например, "cart")
    cart_data = request.session.get(settings.CART_SESSION_ID, {})
    product_key = str(product_id)
    
    # Если товара ещё нет в корзине, добавляем его с нулевым количеством
    if product_key not in cart_data:
        cart_data[product_key] = {'quantity': 0, 'price': str(product.price)}
    
    if action == 'increment':
        cart_data[product_key]['quantity'] += 1
    elif action == 'decrement':
        if cart_data[product_key]['quantity'] > 1:
            cart_data[product_key]['quantity'] -= 1
        else:
            del cart_data[product_key]
    
    request.session[settings.CART_SESSION_ID] = cart_data
    request.session.modified = True
    return redirect('cart:cart_detail')