from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('payment/', include('payment.urls', namespace='payment')),
]

urlpatterns += i18n_patterns(
    path('', include('main.urls', namespace='main')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('user/', include('users.urls', namespace='user')),
    path('reviews/', include('review.urls', namespace='reviews')),
    path("i18n/", include("django.conf.urls.i18n")),
    path('services/', include('services.urls', namespace='services')),
    path('auction/', include('auction.urls', namespace='auction')),
    path('favorites/', include('favorites.urls', namespace='favorites')),
    path('chatbot/', include(('chatbot.urls', 'chatbot'), namespace='chatbot')),
    path('api/', include(('api.urls','api'), namespace='api')),

)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
