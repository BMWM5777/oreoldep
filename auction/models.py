from django.db import models
from django.conf import settings
from django.utils import timezone

AUCTION_TYPE_CHOICES = (
    ('live', 'Live'),
    ('fixed_time', 'Фиксированный'),
)

AUCTION_STATUS_CHOICES = (
    ('pending', 'Ожидает подтверждения'),
    ('approved', 'Подтвержден'),
    ('rejected', 'Отклонен'),
    ('completed', 'Завершён'),
    ('change_requested', 'Запрос на изменение'),
)

class Auction(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Продавец',
        related_name='auctions_sold'
    )
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='auction_images', blank=True, null=True, verbose_name='Изображение')
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стартовая цена')
    current_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Текущая цена', default=0)
    bid_step = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Шаг ставки')
    auction_type = models.CharField(max_length=20, choices=AUCTION_TYPE_CHOICES, verbose_name='Тип аукциона')
    start_time = models.DateTimeField(verbose_name='Дата и время начала', default=timezone.now)
    end_time = models.DateTimeField(verbose_name='Дата окончания')
    status = models.CharField(max_length=20, choices=AUCTION_STATUS_CHOICES, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    winner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Победитель',
        related_name='auctions_won'
    )
    admin_comment = models.TextField(blank=True, null=True, verbose_name='Комментарий администратора')
    notified = models.BooleanField(default=False, verbose_name="Победитель уведомлен")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Лот аукциона'
        verbose_name_plural = 'Лоты аукциона'

class AuctionImage(models.Model):
    auction = models.ForeignKey(
        Auction,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Лот'
    )
    image = models.ImageField(upload_to='auction_images/', verbose_name='Фото')

    def __str__(self):
        return f"Фото для {self.auction.title}"

    class Meta:
        verbose_name = 'Фото лота'
        verbose_name_plural = 'Фото лотов'


class Bid(models.Model):
    auction = models.ForeignKey(
        Auction,
        on_delete=models.CASCADE,
        related_name='bids',
        verbose_name='Аукцион'
    )
    bidder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Участник'
    )
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма ставки')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время ставки')

    def __str__(self):
        return f"{self.bidder.username} - {self.bid_amount}"

    class Meta:
        verbose_name = 'Ставка'
        verbose_name_plural = 'Ставки'
