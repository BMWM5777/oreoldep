from django.urls import path
from . import views
from .views import my_auctions

app_name = 'auction'

urlpatterns = [
    path('', views.auction_list, name='list'),
    path('create/', views.create_auction, name='create'),
    path('my-auctions/', my_auctions, name='my_auctions'),
    path('<int:auction_id>/', views.auction_detail, name='detail'),
    path('edit/<int:auction_id>/', views.edit_auction, name='edit'),
    path('get-bids/<int:auction_id>/', views.get_bids, name='get_bids'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('modal-detail/<int:auction_id>/', views.auction_modal_detail, name='modal_detail'),
    path('get-auction-status/<int:auction_id>/', views.get_auction_status, name='get_auction_status'),
]
