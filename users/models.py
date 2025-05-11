from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = (
    ('client', 'Клиент'),
    ('master', 'Мастер'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    image = models.ImageField(upload_to='users_image', blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='client',
        verbose_name='Роль'
    )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    car_brand = models.CharField(max_length=50, blank=True, null=True, verbose_name='Марка авто')
    car_year = models.PositiveIntegerField(blank=True, null=True, verbose_name='Год авто')
    car_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Гос. номер авто')
    vin_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='VIN код авто')
    
    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.username
