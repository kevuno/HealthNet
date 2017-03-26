from django import forms
from django.forms import widgets
from django.utils import timezone
from userprofile.models import Patient
from appointment.models import Appointment
from messaging.models import Message
from django.contrib.auth.models import User


class DoctorAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment

        fields = [
            'description', 'location', 'date', 'time', 'endTime', 'patient_ID',
        ]
        exclude = [
            'doctor_ID',
        ]

        widgets = {
            'description': widgets.TextInput(attrs={'class': 'form-control'}),
            'location': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'date': widgets.SelectDateWidget(years=[timezone.now().year, timezone.now().year + 1]),
            'time': widgets.TimeInput(attrs={'type': 'time', 'class': 'form-control'}, format='%H:%M'),
            'endTime': widgets.TimeInput(attrs={'type': 'time', 'class': 'form-control'}, format='%H:%M'),
            'patient_ID': widgets.Select(attrs={'class': 'form-control'}),
        }


class DoctorMessageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DoctorMessageForm, self).__init__(*args, **kwargs)

        email_list = []
        x = 0
        while x < len(User.objects.all().values_list('email', flat=True)):
            first_name = User.objects.all().values()[x]['first_name']
            last_name = User.objects.all().values()[x]['last_name']
            email = User.objects.all().values_list('email', flat=True)[x]
            email_list.append((email, first_name + ' ' + last_name + '<' + email + '>'))
            x += 1
        EMAILS = tuple(email_list)

        self.fields['to'] = forms.ChoiceField(choices=EMAILS, widget=widgets.Select(attrs={'class': 'form-control'}))


    class Meta:
        model = Message

        fields = [
            'From', 'to', 'subject', 'message'
        ]
        exclude = [
            'date', 'time'
        ]

        widgets = {
            'From': widgets.TextInput(attrs={'readonly':'readonly','class': 'form-control'}),
            'to': widgets.Select(attrs={'class': 'form-control'}),
            'subject': widgets.TextInput(attrs={'class': 'form-control'}),
            'message': widgets.Textarea(attrs={'class': 'form-control'})
        }

class DoctorMedicalForm(forms.ModelForm):
    """
    The patient medical information form class. Inherits from ModelForm.
    Fields: gender, height,weight,emergency_contact,emergency_number,hospital.
    widgets: css bootstrap class attributes
    """

    class Meta:
        model = Patient
        fields = ('gender', 'height', 'weight', 'emergency_contact', 'emergency_number')
        widgets = {
            'gender': widgets.Select(attrs={'class': 'form-control'}),
            'height': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': "5'0''"}),
            'weight': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': "100"}),
            'emergency_contact': widgets.TextInput(attrs={'class': 'form-control'}),
            'emergency_number': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567890'})
        }