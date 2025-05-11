from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse_lazy

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('orders_history/', views.orders_view, name='orders_history'),
    path('car-data/', views.car_data_view, name='car_data'),
    path('logout/', views.logout, name='logout'),
    path('password-reset/', 
     auth_views.PasswordResetView.as_view(
         template_name='users/password_reset.html',
         email_template_name='users/password_reset_email.html',
         success_url=reverse_lazy('users:password_reset_done')
     ), name='password_reset'),

    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html',
             success_url=reverse_lazy('users:password_reset_complete')
         ), name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ), name='password_reset_complete'),
]
