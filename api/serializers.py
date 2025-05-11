from rest_framework import serializers
from django.contrib.auth import get_user_model
from services.models import ServiceCategory, Service, Appointment, RescheduleRequest

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','email','password','role')
    def create(self, validated):
        user = User(**validated)
        user.set_password(validated['password'])
        user.save()
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ('id','name','slug','description')

class ServiceSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Service
        fields = ('id','name','description','price','duration','master','category')

class AppointmentSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), source='service', write_only=True)
    class Meta:
        model = Appointment
        fields = (
            'id','service','service_id','date_time',
            'car_brand','car_year','car_number','vin_code','status'
        )
        read_only_fields = ('status',)

class RescheduleRequestSerializer(serializers.ModelSerializer):
    appointment_id = serializers.PrimaryKeyRelatedField(
        queryset=Appointment.objects.all(), source='appointment', write_only=True)
    class Meta:
        model = RescheduleRequest
        fields = ('id','appointment','appointment_id','new_date_time','comment','status')
        read_only_fields = ('status',)
