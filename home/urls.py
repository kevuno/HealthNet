from django.conf.urls import url
from . import views

app_name='home'

urlpatterns = [

    # :8000/
    url(r'^$', views.index, name='index'),

    # :8000/goodbye   ( :8000/userprofile/logout redirects here )
    url(r'goodbye/?', views.goodbye),

    # from userprofile/login django generates /accounts/profile when using login feature.
    # From this url, the view adds to the log, then redirects to /userprofile
    url(r'accounts/profile/?', views.logLogin),
    ]

