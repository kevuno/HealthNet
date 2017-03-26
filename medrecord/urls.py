from django.conf.urls import url

from . import views

app_name = 'medrecord'
urlpatterns = [

    # medrecord
    url(r'^$', views.UploadFile.as_view(), name='index'),

    # /medrecord/upload
    url(r'^upload/?$', views.UploadFile.as_view(), name='upload'),

    # /medrecord/view/uploads
    url(r'^view/uploads/?$', views.view_uploads, name='view uploads'),

    # /medrecord/view/tests
    url(r'^view/tests/?$', views.view_tests, name='view tests'),

    # /medrecord/view/tests/#
    url(r'^view/tests/(?P<test_id>[0-9]+)?$', views.doctor_test_details, name='patients test list'),

    # /medrecord/view/prescriptions
    # Doctors viewing a list of prescriptions
    url(r'^view/prescriptions/?$', views.doctor_view_prescriptions, name='view prescriptions'),

    url(r'^view/prescriptions/(?P<prescription_id>[0-9]+)/?$', views.doctor_prescription_detail, name='prescription detail'),

    # /medrecord/prescriptions
    # This is for the patients viewing a list of prescriptions
    url(r'^prescriptions/?$', views.patient_view_prescriptions, name='prescriptions'),

    # /medrecord/prescriptions/#
    # This is for the patients viewing a specific prescriptions
    url(r'^prescriptions/(?P<prescription_id>[0-9]+)/?$', views.prescription_detail, name='detail'),

    # /medrecord/tests
    # For patients to view their tests
    url(r'^tests/?$', views.patient_view_tests, name='patients test list'),

    # /medrecord/test/#
    # For patients to view their test details
    url(r'^tests/(?P<test_id>[0-9]+)?$', views.patient_view_tests_details, name='patients test detail'),


]

