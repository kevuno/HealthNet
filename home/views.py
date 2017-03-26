from django.shortcuts import render
from log.models import Entry
from django.shortcuts import redirect
from django.contrib.auth.views import logout
from userprofile.factory import UserFactory


# Create your views here.
def index(request):
    """
    The homepage
    :param request: the user
    :return: redner the main index homepage
    """
    user = UserFactory.get_user(request)
    if UserFactory.isDoctor(user) or UserFactory.isNurse(user):
        return redirect('/employee')

    return render(request, 'healthnet/main_index.html', )


# Intercepts the login to record the successful login to the log
# Then redirects the url to user profile
def logLogin(request):
    """
    This intercepts the login
    records an entry into the log
    redirects the login default next page (8000/accounts/profile/) to 8000/userprofile
    :param request: the user logging in
    :return: redirect the 8000/userprofile
    """

    logEntry = Entry()
    logEntry.user = request.user.username
    logEntry.trigger = "home.views.logLogin"
    logEntry.activity = "Logged In"
    logEntry.save()

    if UserFactory.isPatient(UserFactory.get_user(request)):
        return redirect('/userprofile')
    else:
        return redirect('/employee')


def goodbye(request):
    """
    The goodbye page to display when a user logs out
    adds an entry into the log
    logs out request
    :param request: the user
    :return: confirmation goodbye page
    """

    logEntry = Entry()
    # logEntry.user = "TODO: Figure out how to determine who a logged out user was"
    logEntry.user = request.user.username
    logEntry.trigger = "home.views.goodbye"
    logEntry.activity = "Logged Out"
    logEntry.save()
    logout(request)

    return render(request, 'healthnet/goodbye.html', )
