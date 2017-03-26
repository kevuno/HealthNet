from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .forms import MessageForm
from .models import Message
from django.views.generic import View
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from log.models import Entry
from userprofile.models import User

# Create your views here.
@login_required(login_url='/userprofile/login')
def index(request):
    """
    The central messaging page for the user.
    Has options to view messages and compose a new message
    :param request: user
    :return: renders messages_home.html
    """
    return render(request, 'healthnet/messaging/messages_home.html')


@login_required(login_url='/userprofile/login')
def inbox(request):
    """
    Lists the messages that the user currently has.
    :param request: user
    :return: renders messages_inbox.html
    """
    message_list = Message.objects.filter(to=request.user.email)
    context = {
        'message_list': message_list
    }
    return render(request, 'healthnet/messaging/messages_inbox.html', context)


@login_required(login_url='/userprofile/login')
def message_detail(request, message_id):
    """
    Displays information associated with the selected message:
    To, From, Date & Time sent, Subject, and the message itself.
    Can delete the message.
    :param request: user
    :param message_id: id of the current message
    :return: renders message_detail.html on success
    """
    message = Message.objects.get(pk=message_id)
    if request.method == "GET":
        return render(request, 'healthnet/messaging/message_detail.html', {'message': message})

    elif request.method == "POST":
        message.delete()

        # Add entry into the log
        logEntry = Entry()

        logEntry.user = request.user.username
        logEntry.trigger = "messaging.views.message_detail"
        logEntry.activity = "Deleted Message"
        logEntry.save()
        return HttpResponseRedirect("/messages/inbox")


class ComposeMessage(View):
    """
    View for creating a new message
    To, From, Subject, and the message itself.
    Records the date and time after form is validated.
    """

    template = 'healthnet/messaging/messages_compose.html'

    @method_decorator(login_required(login_url='/userprofile/login'))
    def get(self, request):
        form = MessageForm(initial={'From': request.user.email})
        return render(request, self.template, {'form': form})

    #need to check if email exists
    @method_decorator(login_required(login_url='/userprofile/login'))
    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            if User.objects.filter(email = message.to).exists():
                message.From = request.user.first_name + ' ' + request.user.last_name + '<' + request.user.email + '>'
                message.date = timezone.now()
                message.time = timezone.now()
                message.save()

                # Add entry into the log
                logEntry = Entry()

                # determining who sent the message
                sender = User.objects.get(email=request.user.email)

                logEntry.user = sender.username
                logEntry.trigger = "messaging.views.ComposeMessage"
                logEntry.activity = "Sent Message"
                logEntry.save()

                return HttpResponseRedirect('/messages')

            else:
                errormsg = '- The email that you tried to message does not exist.'
                return render(request, self.template, {'form': form, 'errormsg': errormsg})

        return render(request, self.template, {'form': form})
