from django import forms
from django.forms import widgets
from .models import Message
from django.contrib.auth.models import User


class MessageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        email_list = []
        x = 0
        while x < len(User.objects.all().values_list('email', flat=True)):
            first_name = User.objects.all().values()[x]['first_name']
            last_name = User.objects.all().values()[x]['last_name']
            email = User.objects.all().values_list('email', flat=True)[x]
            if not ((User.objects.all().values()[x]['is_superuser'])):
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
            'subject': widgets.TextInput(attrs={'class': 'form-control'}),
            'message': widgets.Textarea(attrs={'class': 'form-control'})
        }