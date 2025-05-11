from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (5, '⭐⭐⭐⭐⭐'),
        (4, '⭐⭐⭐⭐☆'),
        (3, '⭐⭐⭐☆☆'),
        (2, '⭐⭐☆☆☆'),
        (1, '⭐☆☆☆☆'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        label="Оцените нас"
    )

    class Meta:
        model = Review
        fields = ['text', 'rating']
        labels = {
            'text': 'Ваш отзыв',
        }
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Введите ваш отзыв...'}),
        }
