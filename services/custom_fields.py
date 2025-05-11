import datetime
from django import forms
from django.core.exceptions import ValidationError

class DurationField(forms.Field):
    widget = forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'placeholder': 'ЧЧ:ММ'})

    def to_python(self, value):
        if not value:
            return None
        try:
            t = datetime.datetime.strptime(value, '%H:%M')
        except ValueError:
            raise ValidationError("Введите время в формате ЧЧ:ММ")
        return datetime.timedelta(hours=t.hour, minutes=t.minute)

    def prepare_value(self, value):
        if isinstance(value, datetime.timedelta):
            total_seconds = int(value.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours:02d}:{minutes:02d}"
        return value
