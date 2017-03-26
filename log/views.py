from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from log.models import Entry
from userprofile.models import Patient, Doctor, Nurse, Hospital
from datetime import datetime



@staff_member_required
def stats_alt(request):
    """
    Handles statistics by finding values, calculating numbers
    pushes variables to the statistics template
    :param request: user
    :return: render statistics html
    """



    template_name = 'healthnet/employee/statistics.html'

    # ------------------------------
    #  Patient pie chart stats
    # ------------------------------
    total_male_patients = Patient.objects.filter(gender__istartswith='M').count()
    total_female_patients = Patient.objects.filter(gender__istartswith='F').count()

    # ------------------------------
    #  Activity bar graph stats
    # ------------------------------
    total_logins = Entry.objects.filter(activity__exact='Logged In').count()
    total_logouts = Entry.objects.filter(activity__exact='Logged Out').count()
    total_appointments_created = Entry.objects.filter(activity__exact='Created Appointment').count()
    total_appointments_updated = Entry.objects.filter(activity__exact='Updated Appointment').count()
    total_appointments_deleted = Entry.objects.filter(activity__exact='Deleted Appointment').count()
    total_accounts_created = Entry.objects.filter(activity__exact='Created Account').count()
    total_accounts_updated = Entry.objects.filter(activity__exact='Updated Patient').count()
    total_messages_sent = Entry.objects.filter(activity__exact='Sent Message').count()
    total_messages_deleted = Entry.objects.filter(activity__exact='Deleted Message').count()
    total_transfer_patients = Entry.objects.filter(activity__contains='Transferred').count()
    total_medical_updates = Entry.objects.filter(activity__contains='Medical information').count()
    total_export_informations = Entry.objects.filter(activity__contains='Exported').count()
    total_tests_created = Entry.objects.filter(activity__contains='test').count()
    total_prescriptions_created = Entry.objects.filter(activity__contains='prescription').count()

    # ------------------------------
    #  Hospital pie chart stats
    # ------------------------------
    distinct_hospitals = Hospital.objects.distinct()
    num_hospitals = distinct_hospitals.count()
    hospital_loop_range = range(0, num_hospitals)

    hospital_names = []
    num_patients_in_each_hospital = []
    for k in distinct_hospitals:
        hospital_names.append(k.name)

    for i in hospital_loop_range:
        patient_count = Patient.objects.filter(hospital__name=hospital_names[i])
        num_patients_in_each_hospital.append(patient_count.count())

    # ------------------------------
    #  Doctors pie chart stats
    # ------------------------------
    doctors = Doctor.objects.all()
    num_doctors = doctors.count()
    doctor_loop_range = range(0, num_doctors)

    doctor_names = []
    num_patients_for_each_doctor = []
    for k in doctors:
        doctor_names.append(k.user.first_name)

    for i in doctor_loop_range:
        patient_count = Patient.objects.filter(doctor__user__first_name=doctor_names[i])
        num_patients_for_each_doctor.append(patient_count.count())

    # ------------------------------
    #  Site Activity time chart
    # ------------------------------
    log_entries = Entry.objects.all()
    total_log_entries = log_entries.count()
    log_loop_range = range(0, total_log_entries)

    # Yes, this is a VERY barbaric way of doing things
    # There is probably a much easier and better way of doing things but...
    list_of_years = []
    list_of_months = []
    list_of_days = []

    for i in log_entries:
        list_of_years.append(i.time.year)
        list_of_months.append(i.time.month - 1)
        list_of_days.append(i.time.day)



    context = {
            'total_male_patients': total_male_patients,
            'total_female_patients': total_female_patients,
            'total_logins': total_logins,
            'total_logouts': total_logouts,
            'total_appointments_created': total_appointments_created,
            'total_appointments_updated': total_appointments_updated,
            'total_appointments_deleted': total_appointments_deleted,
            'total_accounts_created': total_accounts_created,
            'total_accounts_updated': total_accounts_updated,
            'total_messages_sent': total_messages_sent,
            'total_messages_deleted': total_messages_deleted,
            'total_transfer_patients': total_transfer_patients,
            'total_medical_updates': total_medical_updates,
            'distinct_hospitals' : distinct_hospitals,
            'num_hospitals': num_hospitals,
            'hospital_loop_range': hospital_loop_range,
            'num_patients_in_each_hospital': num_patients_in_each_hospital,
            'hospital_names': hospital_names,
            'doctor_loop_range': doctor_loop_range,
            'num_patients_for_each_doctor': num_patients_for_each_doctor,
            'doctor_names': doctor_names,
            'list_of_years': list_of_years,
            'list_of_months':  list_of_months,
            'list_of_days': list_of_days,
            'log_loop_range': log_loop_range,
            'total_export_informations': total_export_informations,
            'total_tests_created': total_tests_created,
            'total_prescriptions_created': total_prescriptions_created

        }

    return render(request, template_name, context)