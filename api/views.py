from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    UserRegistrationSerializer, CategorySerializer, ServiceSerializer,
    AppointmentSerializer, RescheduleRequestSerializer
)
from django.contrib.auth import get_user_model
from services.models import ServiceCategory, Service, Appointment, RescheduleRequest

User = get_user_model()

# Регистрация
class RegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

# Категории и услуги
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = CategorySerializer

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.select_related('category').all()
    serializer_class = ServiceSerializer
    filterset_fields = ('category__slug',)

# Записи клиента
class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'master':
            # мастер видит только свои
            return Appointment.objects.filter(service__master=user)
        # клиент видит свои
        return Appointment.objects.filter(client=user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reschedule(self, request, pk=None):
        appt = self.get_object()
        serializer = RescheduleRequestSerializer(
            data={'appointment_id': appt.id, **request.data}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def approve(self, request, pk=None):
        appt = self.get_object()
        if request.user.role != 'master' or appt.service.master != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        appt.status = 'confirmed'
        appt.save()
        return Response(self.get_serializer(appt).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        appt = self.get_object()
        if request.user.role != 'master' or appt.service.master != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        appt.status = 'canceled'
        appt.save()
        return Response(self.get_serializer(appt).data)

# RescheduleRequest отдельный (если нужно лог посмотреть)
class RescheduleRequestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RescheduleRequest.objects.select_related('appointment').all()
    serializer_class = RescheduleRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)
