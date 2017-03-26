from django.conf.urls import url

from . import views

app_name = 'employee'
urlpatterns = [

    # /employee
    url(r'^$', views.home, name='home'),

    url(r'^appointment$/?', views.DoctorCreateAppointment.as_view(), name='doctor_appointment'),

    url(r'^appointment/view$/?', views.view_appointments, name='view_appointments'),

    url(r'^appointment/(?P<appointment_id>[0-9]+)/?$', views.doctor_appointment_detail, name='detail'),

    url(r'^appointment/(?P<appointment_id>[0-9]+)/edit/?$', views.DoctorAppointmentEdit.as_view(), name='edit'),

    url(r'^calendar/?', views.calendar, name='doctor_appointment'),

    url(r'^patient_list/?$', views.view, name='patient_list'),

    url(r'^patient_options/?$', views.patient_options, name='patient_options'),

    url(r'^transfer_patient/?$', views.transfer_patient, name='transfer_patient'),

    url(r'^admit_patient/?$', views.admit_patient, name='admit_patient'),

    url(r'^(?P<patient_id>[0-9]+)/?$', views.patient_options, name='patient_options'),

    url(r'^messages/inbox/?$', views.DoctorInbox, name='doctor_inbox'),

    url(r'^messages/compose/?$', views.DoctorComposeMessage.as_view(), name='doctor_compose'),

    url(r'^messages/(?P<message_id>[0-9]+)/?$', views.doctor_message_detail, name='detail')
]
