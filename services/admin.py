from django.contrib import admin
from .models import ServiceCategory, Service, Appointment, RescheduleRequest
from .forms import ServiceForm

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    form = ServiceForm
    list_display = ('name', 'category', 'price', 'duration', 'master')
    list_filter = ('category', 'master')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'date_time', 'created')
    list_filter = ('service', 'date_time')

@admin.register(RescheduleRequest)
class RescheduleRequestAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'new_date_time', 'status', 'created')
    list_filter = ('status',)
