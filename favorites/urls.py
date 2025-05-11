from django.urls import path
from .views import add_to_favorites, favorites_list

app_name = 'favorites'

urlpatterns = [
    path('add/<int:product_id>/', add_to_favorites, name='add_to_favorites'),
    path('list/', favorites_list, name='favorites_list'),
]
