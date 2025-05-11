from django.urls import path
from .views import add_review, all_reviews, add_product_review

app_name = 'reviews'

urlpatterns = [
    path("add/", add_review, name="add_review"),
    path("", all_reviews, name="all_reviews"),
    path('product/<slug:slug>/add/', add_product_review, name='add_product_review')
]
