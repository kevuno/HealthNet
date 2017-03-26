from django import forms
from django.forms import widgets
from django.utils import timezone

from .models import Appointment


# @login_required
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment

        fields = [
            'description', 'location', 'date', 'time', 'endTime'
        ]
        exclude = [
            'patient_ID', 'doctor_ID'
        ]

        widgets = {
            'description': widgets.TextInput(attrs={'class': 'form-control'}),
            'location': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'date': widgets.SelectDateWidget(years=[timezone.now().year, timezone.now().year + 1]),
            'time': widgets.TimeInput(attrs={'type': 'time', 'class': 'form-control'}, format='%H:%M'),
            'endTime': widgets.TimeInput(attrs={'type': 'time', 'class': 'form-control'}, format='%H:%M'),
            # 'patient_ID': forms.MultipleHiddenInput()
        }


class UpdateAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment

        fields = [
            'description', 'location', 'date', 'time', 'endTime'
        ]

        widgets = {
            'description': widgets.TextInput(attrs={'class': 'form-control'}),
            'location': widgets.TextInput(attrs={'class': 'form-control'}),
            'date': widgets.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': widgets.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'endTime': widgets.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            # 'patient_ID': forms.MultipleHiddenInput()
        }

        exclude = [
            'patient_ID', 'doctor_ID'
        ]
