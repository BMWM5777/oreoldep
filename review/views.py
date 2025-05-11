from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm
from orders.models import OrderItem
from main.models import Product

def index(request):
    reviews = Review.objects.all().order_by("-created_at")
    return render(request, "main/index/index.html", {"reviews": reviews})

@login_required
def add_product_review(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    bought = OrderItem.objects.filter(
        order__user=request.user,
        order__paid=True,
        product=product
    ).exists()
    if not bought:
        messages.error(request, "Отзывы можно оставлять только на купленные товары.")
        return redirect(product.get_absolute_url())
    exists = Review.objects.filter(user=request.user, product=product).exists()
    if exists:
        messages.info(request, "Вы уже оставили отзыв на этот товар.")
        return redirect(product.get_absolute_url())

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            rv = form.save(commit=False)
            rv.user = request.user
            rv.product = product
            rv.save()
            messages.success(request, "Спасибо! Ваш отзыв опубликован.")
            return redirect(product.get_absolute_url())
    else:
        form = ReviewForm()
    return render(request, "review/add_product_review.html", {
        'form': form,
        'product': product,
    })

@login_required
def add_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect("main:index")
        else:
            print(form.errors)
    else:
        form = ReviewForm()
    
    return render(request, "review/add_review.html", {"form": form})


def all_reviews(request):
    reviews = Review.objects.all().order_by("-created_at")
    return render(request, "review/reviews.html", {"reviews": reviews})

