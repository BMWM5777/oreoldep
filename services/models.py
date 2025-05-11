from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django import forms
from django.utils.translation import gettext_lazy as _

class ServiceCategory(models.Model):
    name = models.CharField(max_length=25, unique=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=50, unique=True, blank=True, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'Категория услуги'
        verbose_name_plural = 'Категории услуг'
    
    def get_absolute_url(self):
        return reverse("services:service_list_by_category", args=[self.slug])
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)[:25]
            slug = base_slug
            counter = 1
            while ServiceCategory.objects.filter(slug=slug).exists():
                slug = f"{base_slug[:22]}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, verbose_name="Категория")
    name = models.CharField(max_length=100, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание услуги")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.DurationField(verbose_name="Время выполнения")
    master = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        limit_choices_to={'role': 'master'}, verbose_name="Мастер"
    )

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name

class Appointment(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Клиент")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга")
    date_time = models.DateTimeField(verbose_name="Дата и время записи")
    car_brand = models.CharField(max_length=50, blank=True, null=True, verbose_name="Марка авто")
    car_year = models.PositiveIntegerField(blank=True, null=True, verbose_name="Год авто")
    car_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Гос. номер авто")
    vin_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="VIN код авто")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")
    STATUS_CHOICES = (
    ('pending', _("Ожидание")),
    ('confirmed', _("Подтверждено")),
    ('canceled', _("Отменено"))
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус записи")


    class Meta:
        verbose_name = "Запись на услугу"
        verbose_name_plural = "Записи на услуги"

    def __str__(self):
        return f"{self.client.username} - {self.service.name} ({self.date_time})"
    

class RescheduleRequest(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, verbose_name="Запись на услугу")
    new_date_time = models.DateTimeField(verbose_name="Новая дата и время")
    comment = models.TextField(verbose_name="Комментарий мастера")
    STATUS_CHOICES = (
        ('pending', _("Ожидает подтверждения")),
        ('approved', _("Подтвержден")),
        ('rejected', _("Отклонен")),
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_("Статус запроса")
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата запроса"))

    class Meta:
        verbose_name = _("Запрос на перенос услуги")
        verbose_name_plural = _("Запросы на перенос услуг")

    def __str__(self):
        return f"Перенос для {self.appointment} - {self.status}"
