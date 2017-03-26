from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import widgets

from django.utils import timezone

from .models import Doctor, Nurse, Patient
import re


class LoginForm(forms.ModelForm):
    """
    The login form class. Inherits from ModelForm.
    Fields: username, password.
    """

    class Meta:
        model = User
        fields = ('username', 'password')

        widgets = {
            'password': forms.PasswordInput
        }


class UserForm(forms.ModelForm):
    """
    The user form class. Inherits from ModelForm.
    Fields: first_name, last_name,email,username,password.
    widgets: css bootstrap class attributes
    """

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'email', 'username', 'password')

        widgets = {
            'first_name': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'email': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'example@example.com'}),
            'username': widgets.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        """
        This method makes sure that the email is in the correct format.
        """
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('Email addresses must be unique.')
        return email

    def clean_first_name(self):
        """
        This method makes sure that the first name is in the correct format.
        """
        first_name = self.cleaned_data.get('first_name')
        if not re.match('[a-zA-Z\'-]', first_name):
            raise forms.ValidationError('First name can only contain letters, apostrophes, and/or dashes.')
        return first_name

    def clean_last_name(self):
        """
        This method makes sure that the last name is in the correct format.
        """
        last_name = self.cleaned_data.get('last_name')
        if not re.match('[a-zA-Z\'-.]', last_name):
            raise forms.ValidationError('Last name can only contain letters, apostrophes, dashes, and/or periods.')
        return last_name


class DoctorForm(forms.ModelForm):
    """
    The Doctor form class. Inherits from ModelForm.
    Excludes the user data.
    """
    class Meta:
        model = Doctor
        exclude = {'user'}


class NurseForm(forms.ModelForm):
    """
    The Nurse form class. Inherits from ModelForm.
    Excludes the user data.
    """
    class Meta:
        model = Nurse
        exclude = {'user'}


class PatientForm(forms.ModelForm):
    """
    The patient form class. Inherits from ModelForm.
    Fields: date_of_birth, phone_number,address,city,insurance_provider,insurance_number,doctor.
    widgets: css bootstrap class attributes
    """

    class Meta:
        model = Patient
        fields = (
            'date_of_birth', 'phone_number', 'address', 'city', 'insurance_provider', 'insurance_number', 'doctor')
        widgets = {
            # 'date_of_birth': widgets.TextInput(attrs={'class':'form-control'}),
            'date_of_birth': widgets.SelectDateWidget(years=range(1899, timezone.now().year + 1)),
            'phone_number': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567890'}),
            'address': widgets.TextInput(attrs={'class': 'form-control'}),
            'city': widgets.TextInput(attrs={'class': 'form-control'}),
            'insurance_provider': widgets.TextInput(attrs={'class': 'form-control'}),
            'insurance_number': widgets.TextInput(
                attrs={'class': 'form-control', 'placeholder': '01234567890123456789'}),
            'doctor': widgets.Select(attrs={'class': 'form-control'})
        }

        exclude = {'user'}


class PatientMedicalForm(forms.ModelForm):
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
        exclude = {'user'}


class DischargeForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = {'hospital'}
        widgets = {
            'hospital': widgets.HiddenInput()
        }



class UpdatePatientForm(forms.ModelForm):
    """
    TODO: DELETE THIS CLASS
    """

    class Meta:
        model = Patient
        fields = ('address', 'city', 'phone_number', 'height',
                  'weight', 'emergency_contact', 'emergency_number',
                  'insurance_provider', 'insurance_number')
        widgets = {
            'address': widgets.TextInput(attrs={'class': 'form-control'}),
            'city': widgets.TextInput(attrs={'class': 'form-control'}),
            'phone_number': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567890'}),
            'height': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': "5'0''"}),
            'weight': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': "100"}),
            'emergency_contact': widgets.TextInput(attrs={'class': 'form-control'}),
            'emergency_number': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567890'}),
            'insurance_provider': widgets.TextInput(attrs={'class': 'form-control'}),
            'insurance_number': widgets.TextInput(
                attrs={'class': 'form-control', 'placeholder': '01234567890123456789'}),
        }
        exclude = {'user'}
