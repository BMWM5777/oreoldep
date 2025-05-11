from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegistrationView, CategoryViewSet, ServiceViewSet,
    AppointmentViewSet, RescheduleRequestViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('services', ServiceViewSet, basename='service')
router.register('appointments', AppointmentViewSet, basename='appointment')
router.register('reschedules', RescheduleRequestViewSet, basename='reschedule')

urlpatterns = [
    # auth
    path('register/', RegistrationView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # API
    path('', include(router.urls)),
]
