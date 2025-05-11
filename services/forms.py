from django import forms
from .models import Appointment, RescheduleRequest, Service
from .custom_fields import DurationField
from datetime import time

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date_time', 'car_brand', 'car_year', 'car_number', 'vin_code']
        widgets = {
            'date_time': forms.HiddenInput(attrs={'id': 'selected-datetime'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.required = (name != 'vin_code')

        if not self.instance.pk and self.user:
            self.fields['car_brand'].initial = self.user.car_brand
            self.fields['car_year'].initial = self.user.car_year
            self.fields['car_number'].initial = self.user.car_number
            self.fields['vin_code'].initial = self.user.vin_code

    def clean_date_time(self):
        dt = self.cleaned_data.get('date_time')

        if dt:

            if dt.time() < time(9, 0) or dt.time() > time(20, 0):
                raise forms.ValidationError("Выберите время между 09:00 и 20:00")

            if dt.weekday() == 6:
                raise forms.ValidationError("Записи принимаются с понедельника по субботу")

            existing_appointment = Appointment.objects.filter(date_time=dt).exists()
            if existing_appointment:
                raise forms.ValidationError("Это время уже занято. Выберите другое.")

        return dt


class RescheduleRequestForm(forms.ModelForm):
    class Meta:
        model = RescheduleRequest
        fields = ['new_date_time', 'comment']
        widgets = {
            'new_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_new_date_time(self):
        dt = self.cleaned_data.get('new_date_time')

        if dt:
            if dt.time() < time(9, 0) or dt.time() > time(20, 0):
                raise forms.ValidationError("Выберите время между 09:00 и 20:00")
            if dt.weekday() == 6:
                raise forms.ValidationError("Записи принимаются с понедельника по субботу")

            existing_appointment = Appointment.objects.filter(date_time=dt).exists()
            if existing_appointment:
                raise forms.ValidationError("Это время уже занято. Выберите другое.")

        return dt



class ServiceForm(forms.ModelForm):
    duration = DurationField()

    class Meta:
        model = Service
        fields = ['category', 'name', 'description', 'price', 'duration', 'master']
