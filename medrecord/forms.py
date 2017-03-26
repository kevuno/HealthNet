from django import forms
from .models import MedicalRecord, Prescription, TestResult
from django.forms import widgets


class MedicalRecordModelForm(forms.ModelForm):

    class Meta:
        model = MedicalRecord

        fields = {
            'title',
            'file',
            'patient_ID',

        }
        widgets = {
            'patient_ID': widgets.Select(attrs={'class': 'form-control'})
        }


class PrescriptionModelForm(forms.ModelForm):

    class Meta:
        model = Prescription

        fields = {
            'patient',
            'medication',
            'dosage',
            'description',
            'quantity'
        }

        widgets = {
            'patient': widgets.HiddenInput(),
            'medication': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Medication'}),
            'dosage': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '10'}),
            'description': widgets.TextInput(attrs={'class': 'form-control'}),
            'quantity': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '10 mg'})
        }


class TestResultModelForm(forms.ModelForm):

    class Meta():
        model = TestResult

        fields = {
            'title',
            'description',
            'released',
            'patient_ID',
            'comment',
        }

        widgets = {
            'title': widgets.TextInput(attrs={'class': 'form-control'}),
            'description': widgets.TextInput(attrs={'class': 'form-control'}),
            'patient_ID': widgets.HiddenInput(),
        }
