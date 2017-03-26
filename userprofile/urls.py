from django.conf.urls import url
from . import views
from home.views import goodbye
from django.contrib.auth.views import login

app_name = 'userprofile'

urlpatterns = [

    # /userprofile
    url(r'^$', views.indexView, name='index'),

    # /userprofile/register
    url(r'^register/?$', views.PatientUserFormView.as_view(), name='register'),

    # /userprofile/logout redirects to :8000/goodbye while logging the user out
    url(r'^logout/?$', goodbye, name='logout'),

    #url(r'^view/?$', views.profile_view, name='view'),

    url(r'^update/?$', views.UpdateProfileView.as_view(), name='edit'),
    url(r'^export/?$', views.export, name='export'),

    # This is going to redirect to accounts/profile/ but I can't figure out how to change that
    # so I am just going to have healthnet/urls.py redirect :8000/accounts/profile/ to :8000/userprofile
    # in the home app
    url(r'^login/?$', login, {'template_name': 'healthnet/login.html'}),

]
