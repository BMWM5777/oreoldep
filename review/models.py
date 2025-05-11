# review/models.py
from django.conf import settings
from django.db import models
from main.models import Product

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True,
        verbose_name="Товар"
    )
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка", default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = (('user', 'product'),)  # один отзыв на пользователя + товар

    def __str__(self):
        target = self.product.name if self.product else "сайт"
        return f"Отзыв от {self.user.username} на «{target}»"

    def get_avatar(self):
        if getattr(self.user, 'image', None):
            return self.user.image.url
        return "/static/img/noimage.jpg"
