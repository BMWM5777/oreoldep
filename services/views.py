from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import json
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Service, ServiceCategory, Appointment, RescheduleRequest
from .forms import AppointmentForm, RescheduleRequestForm
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, time, timedelta
from django.http import JsonResponse
from utils.decorators import require_auth

def service_list(request):
    categories = ServiceCategory.objects.all()
    services = Service.objects.select_related('category', 'master').all()
    return render(request, 'services/service_list.html', {
        'categories': categories,
        'services': services,
        'selected_category': None,
        'current_sort': '',
    })


@login_required
def appointment_detail(request, appointment_id):
    if request.user.role == 'client':
        appointment = get_object_or_404(Appointment, id=appointment_id, client=request.user)
    elif request.user.role == 'master':
        appointment = get_object_or_404(Appointment, id=appointment_id, service__master=request.user)
    else:
        appointment = get_object_or_404(Appointment, id=appointment_id)
    
    reschedule_requests = RescheduleRequest.objects.filter(appointment=appointment)
    return render(request, 'services/appointment_detail.html', {
        'appointment': appointment,
        'reschedule_requests': reschedule_requests,
    })


@login_required
def reschedule_request_create(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.user.role != 'master' or appointment.service.master != request.user:
        messages.error(request, "У вас нет прав для изменения этой записи")
        return redirect('services:appointment_detail', appointment_id=appointment_id)
    
    if request.method == 'POST':
        form = RescheduleRequestForm(request.POST)
        if form.is_valid():
            reschedule = form.save(commit=False)
            reschedule.appointment = appointment
            reschedule.save()
            messages.success(request, "Запрос на перенос успешно создан")
            return redirect('services:appointment_detail', appointment_id=appointment_id)
        else:
            messages.error(request, "Проверьте корректность введённых данных")
    else:
        form = RescheduleRequestForm()
    return render(request, 'services/reschedule_request_form.html', {
        'form': form,
        'appointment': appointment,
    })

@login_required
def reschedule_request_update(request, request_id):
    reschedule_request = get_object_or_404(RescheduleRequest, id=request_id)
    if reschedule_request.appointment.client != request.user:
        messages.error(request, "У вас нет прав для изменения этого запроса")
        return redirect('services:appointment_detail', appointment_id=reschedule_request.appointment.id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            reschedule_request.status = 'approved'
            appointment = reschedule_request.appointment
            appointment.date_time = reschedule_request.new_date_time
            appointment.save()
            messages.success(request, "Запрос подтверждён, запись обновлена")
            send_reschedule_notification(reschedule_request)
        elif action == 'reject':
            reschedule_request.status = 'rejected'
            messages.info(request, "Запрос отклонён")
            send_reschedule_notification(reschedule_request)
        reschedule_request.save()
        return redirect('services:appointment_detail', appointment_id=reschedule_request.appointment.id)
    
    return render(request, 'services/reschedule_request_detail.html', {
        'reschedule_request': reschedule_request,
    })

@require_auth()
def client_appointments(request):
    appointments = Appointment.objects.filter(client=request.user).order_by('-date_time')
    

    status_filter = request.GET.get('status')
    date_filter = request.GET.get('date')
    
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    if date_filter:
        appointments = appointments.filter(date_time__date=date_filter)
    

    paginator = Paginator(appointments, 10)
    page = request.GET.get('page')
    try:
        appointments = paginator.page(page)
    except PageNotAnInteger:
        appointments = paginator.page(1)
    except EmptyPage:
        appointments = paginator.page(paginator.num_pages)
    
    reschedule_requests = RescheduleRequest.objects.filter(appointment__in=appointments).order_by('-created')
    
    return render(request, 'services/client_appointments.html', {
        'appointments': appointments,
        'reschedule_requests': reschedule_requests,
        'status_choices': Appointment.STATUS_CHOICES,
    })

@login_required
def master_appointments(request):
    if request.user.role != 'master':
        messages.error(request, _("Доступ запрещён"))
        return redirect('main:product_list')
    
    appointments = Appointment.objects.filter(service__master=request.user).order_by('-date_time')
    

    status_filter = request.GET.get('status')
    date_filter = request.GET.get('date')
    
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    if date_filter:
        appointments = appointments.filter(date_time__date=date_filter)
    

    paginator = Paginator(appointments, 10)
    page = request.GET.get('page')
    try:
        appointments = paginator.page(page)
    except PageNotAnInteger:
        appointments = paginator.page(1)
    except EmptyPage:
        appointments = paginator.page(paginator.num_pages)
    
    return render(request, 'services/master_appointments.html', {
        'appointments': appointments,
        'status_choices': Appointment.STATUS_CHOICES,
    })

def send_appointment_created_emails(appointment):

    client_subject = "СТО Ореол - Запись оформлена"
    client_message = f"""
    Уважаемый(ая) {appointment.client.username},
    
    Вы успешно записались на услугу "{appointment.service.name}".
    
    Детали записи:
    - Дата и время: {appointment.date_time.strftime('%d.%m.%Y %H:%M')}
    - Мастер: {appointment.service.master.get_full_name()}
    - Автомобиль: {appointment.car_brand} {appointment.car_year} ({appointment.car_number})

    - Контакты мастера: 
      Телефон: {appointment.service.master.phone}
      Email: {appointment.service.master.email}
    
    Статус записи: {appointment.get_status_display()}
    """
    if appointment.client.email:
        send_mail(
            client_subject,
            client_message.strip(),
            settings.DEFAULT_FROM_EMAIL,
            [appointment.client.email],
            fail_silently=True
        )


    master_subject = "СТО Ореол - Новая запись"
    master_message = f"""
    Уважаемый(ая) {appointment.service.master.username},
    
    У вас новая запись на услугу "{appointment.service.name}".
    
    Детали записи:
    - Клиент: {appointment.client.get_full_name()}
    - Дата и время: {appointment.date_time.strftime('%d.%m.%Y %H:%M')}
    - Автомобиль: {appointment.car_brand} {appointment.car_year} ({appointment.car_number})
    - VIN: {appointment.vin_code}
    
    Контакты клиента:
    - Телефон: {appointment.client.phone}
    - Email: {appointment.client.email}
    """
    if appointment.service.master.email:
        send_mail(
            master_subject,
            master_message.strip(),
            settings.DEFAULT_FROM_EMAIL,
            [appointment.service.master.email],
            fail_silently=True
        )

@require_auth()
def appointment_create(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, user=request.user)
        if form.is_valid():
            new_appointment = form.save(commit=False)
            new_appointment.service = service
            new_appointment.client = request.user

            start_time = new_appointment.date_time
            end_time = start_time + service.duration
            buffer_time = timedelta(minutes=5)
            
            # Ищем записи, которые пересекаются с новым интервалом (учитываем буфер)
            overlapping = Appointment.objects.filter(
                service__master=service.master
            ).filter(
                date_time__lt=end_time + buffer_time
            ).filter(
                date_time__gt=start_time - service.duration - buffer_time
            )
            
            if overlapping.exists():
                # Находим последнее занятие в пересечении
                latest_overlap = overlapping.order_by('-date_time').first()
                # Рассчитываем, когда освободится мастер:
                available_from = latest_overlap.date_time + latest_overlap.service.duration + buffer_time
                messages.error(
                    request,
                    _("Выбранное время занято. Вы можете записаться после {}.").format(
                        available_from.strftime('%H:%M')
                    )
                )
                # Возвращаем форму с сообщением об ошибке
                return redirect('services:appointment_create', service_id=service_id)
            
            new_appointment.save()
            send_appointment_created_emails(new_appointment)
            messages.success(request, _("Вы успешно записались на услугу"))
            return redirect('services:client_appointments')
        else:
            messages.error(request, _("Пожалуйста, заполните все обязательные поля корректно"))
    else:
        form = AppointmentForm(user=request.user)
    
    return render(request, 'services/appointment_form.html', {
        'form': form,
        'service': service,
    })


@login_required
def appointment_update(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.user.role != 'master' or appointment.service.master != request.user:
        messages.error(request, _("Доступ запрещён"))
        return redirect('services:master_appointments')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            appointment.status = 'confirmed'
            messages.success(request, _("Запись принята"))
            send_status_notification(appointment, 'confirmed')
        elif action == 'reject':
            appointment.status = 'canceled'
            messages.success(request, _("Запись отклонена"))
            send_status_notification(appointment, 'canceled')
        appointment.save()
    
    return redirect('services:master_appointments')


def service_list_by_category(request, category_slug):
    selected_category = get_object_or_404(ServiceCategory, slug=category_slug)
    services = Service.objects.filter(category=selected_category).select_related('category', 'master')
    categories = ServiceCategory.objects.all()
    return render(request, 'services/service_list.html', {
        'categories': categories,
        'services': services,
        'selected_category': selected_category,
        'current_sort': '',
    })

def send_status_notification(appointment, context):
    subject = "Изменение статуса записи"
    message = f"""
    Уважаемый(ая) {appointment.client.username},
    
    Статус вашей записи на услугу "{appointment.service.name}" 
    изменен на «{appointment.get_status_display()}».
    
    Дата и время: {timezone.localtime(appointment.date_time).strftime('%d.%m.%Y %H:%M')}
    """
    if appointment.client.email:
        send_mail(
            subject,
            message.strip(),
            settings.DEFAULT_FROM_EMAIL,
            [appointment.client.email],
            fail_silently=True
        )

def send_reschedule_notification(reschedule):
    subject = "Статус запроса на перенос"
    message = f"""
    Уважаемый(ая) {reschedule.appointment.client.username},
    
    Ваш запрос на перенос записи был {reschedule.get_status_display().lower()}.
    
    Новая дата: {timezone.localtime(reschedule.new_date_time).strftime('%d.%m.%Y %H:%M')}
    Комментарий: {reschedule.comment}
    """
    if reschedule.appointment.client.email:
        send_mail(
            subject,
            message.strip(),
            settings.DEFAULT_FROM_EMAIL,
            [reschedule.appointment.client.email],
            fail_silently=True
        )

@login_required
def master_appointments_calendar(request):
    # Проверяем роль: только мастер имеет доступ к календарю
    if request.user.role != 'master':
        messages.error(request, _("Доступ запрещён"))
        return redirect('main:product_list')

    # Получаем только подтвержденные записи мастера
    appointments = Appointment.objects.filter(service__master=request.user, status='confirmed')
    
    events = []
    for appointment in appointments:
        event = {
            'title': appointment.service.name,
            'start': appointment.date_time.isoformat(),
            'url': reverse('services:appointment_detail', args=[appointment.id]),
        }
        if appointment.service.duration:
            end_time = appointment.date_time + appointment.service.duration
            event['end'] = end_time.isoformat()
        events.append(event)

    events_json = json.dumps(events)
    return render(request, 'services/master_appointments_calendar.html', {
        'events_json': events_json
    })


@login_required
def available_slots(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    day_str = request.GET.get('day')
    if not day_str:
        return JsonResponse({'error': 'Day not provided'}, status=400)
    
    try:
        day = datetime.strptime(day_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)
    
    # Рабочие часы мастера – условно с 09:00 до 21:00 (можно настроить в сервисе или профиле мастера)
    start_work = datetime.combine(day, time(hour=9, minute=0))
    end_work = datetime.combine(day, time(hour=21, minute=0))
    
    # Получаем все записи мастера для заданного дня
    overlapping = Appointment.objects.filter(
        service__master=service.master,
        date_time__date=day
    ).order_by('date_time')
    
    buffer_time = timedelta(minutes=5)
    appointment_duration = service.duration  # Длительность услуги (timedelta)
    
    # Новый алгоритм: перебираем все потенциальные интервалы слотов за день
    available_slots = []
    slot_interval = appointment_duration + buffer_time
    potential = start_work
    while potential + appointment_duration <= end_work:
        # Проверяем, существует ли конфликт с уже назначенными записями
        conflict = overlapping.filter(
            date_time__lt=potential + appointment_duration + buffer_time,
            date_time__gt=potential - buffer_time
        ).exists()
        if not conflict:
            available_slots.append(potential.strftime('%H:%M'))
        potential += slot_interval

    return JsonResponse({'slots': available_slots})
