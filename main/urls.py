from django.urls import path
from . import views
from .views import index, product_list, product_detail, search_products


app_name = 'main'

urlpatterns = [
     path('', views.index, name='index'),
     path('shop/', views.product_list, name='product_list'),
     path('shop/<slug:slug>/', views.product_detail,
         name='product_detail'),
     path('shop/category/<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
    path("search/", search_products, name="search_products"),
]