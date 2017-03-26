from django.conf.urls import url

from . import views

app_name = 'appointment'
urlpatterns = [

    # /appointments
    url(r'^$', views.index, name='index'),

    # appointments/create
    url(r'^create/?$', views.CreateAppointment.as_view(), name='create'),

    # appointments/view
    url(r'^view/?$', views.view, name='view'),

    # ex: /appointments/5/
    url(r'^(?P<appointment_id>[0-9]+)/?$', views.appointment_detail, name='detail'),

    # ex: /polls/5/edit/
    url(r'^(?P<appointment_id>[0-9]+)/edit/?$', views.AppointmentEdit.as_view(), name='edit'),

    # appointments/calendar
    url(r'^calendar/?$', views.calendar, name='calendar'),

    # appointments/feed (this is the json feed for the calendar)
    url(r'^feed/?$', views.patient_calendar_feed, name='feed')
]
