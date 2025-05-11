from django import forms
from django.forms import modelformset_factory
from .models import Auction, AuctionImage

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'image', 'starting_price', 'bid_step', 'auction_type', 'start_time', 'end_time']
        labels = {
            'title': 'Название лота',
            'description': 'Описание',
            'image': 'Главное изображение',
            'starting_price': 'Стартовая цена',
            'bid_step': 'Шаг ставки',
            'auction_type': 'Тип аукциона',
            'start_time': 'Дата и время начала',
            'end_time': 'Дата и время окончания'
        }
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
class AuctionImageForm(forms.ModelForm):
    class Meta:
        model = AuctionImage
        fields = ['image']
        labels = {
            'image': 'Дополнительное фото'
        }

AuctionImageFormSet = modelformset_factory(
    AuctionImage,
    form=AuctionImageForm,
    extra=3,
    can_delete=False,
    fields=('image',)
)

class BidForm(forms.Form):
    bid_amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Ваша ставка (тенге.)")
