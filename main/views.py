from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count
from django.core.paginator import Paginator
from .models import Product, Category
from cart.forms import CartAddProductForm
from review.models import Review
from django.http import JsonResponse
from orders.models import OrderItem

def popular_list(request):
    products = Product.objects.filter(available=True)[:5]
    return render(request,
                  'main/index/index.html',
                  {'products': products})

def product_detail(request, slug):

    product = get_object_or_404(Product, slug=slug, available=True)

    reviews_qs = product.reviews.all()
    avg_rating = reviews_qs.aggregate(avg=Avg('rating'))['avg']
    reviews_count = reviews_qs.count()

    reviews_qs = product.reviews.all()
    avg = reviews_qs.aggregate(avg=Avg('rating'))['avg']
    reviews_count = reviews_qs.count()

    cart_product_form = CartAddProductForm
    favorite_product_ids = set()
    if request.user.is_authenticated:
        favorite_product_ids = set(request.user.favorites.values_list('product_id', flat=True))
        has_purchased = OrderItem.objects.filter(
            order__user=request.user,
            product=product,
            order__paid=True
        ).exists()
        has_reviewed = Review.objects.filter(user=request.user, product=product).exists()
        can_review = has_purchased and not has_reviewed
    else:
        can_review = False

    return render(request, 'main/product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
        'favorite_product_ids': favorite_product_ids,
        'can_review': can_review,
        'avg_rating': avg_rating,
        'reviews_count': reviews_count,
    })

def product_list(request, category_slug=None):
    page_num = request.GET.get('page', 1)
    sort_option = request.GET.get('sort', 'default')
    category = None
    categories = Category.objects.all()

    qs = Product.objects.filter(available=True).annotate(
        avg_rating=Avg('reviews__rating'),
        reviews_count=Count('reviews'),
    )

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        qs = qs.filter(category=category)

    if sort_option == "price_desc":
        qs = qs.order_by("-price")
    elif sort_option == "price_asc":
        qs = qs.order_by("price")
    elif sort_option == "newest":
        qs = qs.order_by("-created")
    elif sort_option == "oldest":
        qs = qs.order_by("created")
    else:
        qs = qs.order_by("id")

    paginator = Paginator(qs, 12)
    page = paginator.page(int(page_num))
    products = list(page.object_list)
    for p in products:
        avg = p.avg_rating or 0.0
        full = int(avg)
        empty = 5 - full
        p.full_stars = range(full)
        p.empty_stars = range(empty)
        p.avg_rating = avg
    page.object_list = products

    if request.user.is_authenticated:
        favorite_ids = set(request.user.favorites.values_list('product_id', flat=True))
    else:
        favorite_ids = set()
    return render(request, 'main/product/list.html', {
        'category': category,
        'categories': categories,
        'products': page,
        'slug_url': category_slug,
        'current_sort': sort_option,
        'favorite_product_ids': favorite_ids,
    })

def search_products(request):
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        products = Product.objects.filter(name__icontains=query, available=True)
        categories = Category.objects.filter(name__icontains=query)

        for product in products:
            results.append({
                "name": product.name,
                "url": product.get_absolute_url(),
                "image": product.image.url if product.image else "/static/img/noimage.jpg"
            })

        for category in categories:
            results.append({
                "name": f"Категория: {category.name}",
                "url": category.get_absolute_url()
            })

    return JsonResponse({"results": results})

def index(request):
    products = Product.objects.filter(available=True)[:5]
    reviews = Review.objects.filter(product__isnull=True, rating__gte=3).order_by('-created_at')[:10]
    
    if request.user.is_authenticated:
        favorite_product_ids = set(request.user.favorites.values_list('product_id', flat=True))
    else:
        favorite_product_ids = set()
    
    context = {
        'products': products,
        'reviews': reviews,
        'favorite_product_ids': favorite_product_ids,
    }
    return render(request, "main/index/index.html", context)

