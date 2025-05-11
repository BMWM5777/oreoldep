from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('category/<slug:category_slug>/', views.service_list_by_category, name='service_list_by_category'),
    path('appointment/create/<int:service_id>/', views.appointment_create, name='appointment_create'),
    path('appointment/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('appointment/update/<int:appointment_id>/', views.appointment_update, name='appointment_update'),
    path('reschedule/create/<int:appointment_id>/', views.reschedule_request_create, name='reschedule_create'),
    path('reschedule/<int:request_id>/', views.reschedule_request_update, name='reschedule_update'),
    path('my-appointments/', views.client_appointments, name='client_appointments'),
    path('master/appointments/', views.master_appointments, name='master_appointments'),
    path('category/<slug:category_slug>/', views.service_list_by_category, name='service_list_by_category'),
    path('master/appointments/calendar/', views.master_appointments_calendar, name='master_appointments_calendar'),
    path('available-slots/<int:service_id>/', views.available_slots, name='available_slots'),
]
