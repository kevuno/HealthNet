from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from userprofile.models import Doctor, Patient, Nurse, Hospital
from appointment.models import Appointment
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populates the DB with Objects for Demonstration'

    def _create_superuser(self):
        admin = User.objects.create_superuser(username='admin', password='brogrammers', email='admin@healthnet.net')
        admin.save()

    def _create_hospitals(self):
        hospital_list = [
            Hospital(name='Not in hospital'),
            Hospital(name='Strong Hospital'),
            Hospital(name='Thompson Hospital'),
            Hospital(name='John Hopkins Hospital'),
            Hospital(name='Geneva Hospital')
        ]

        for hospital in hospital_list:
            hospital.save()

    def _create_doctors(self):

        user_list = [
            User.objects.create_user(username='doctor', password='brogrammers', email='d@healthnet.net',
                                     first_name='Nancy', last_name='Dickey'),
            User.objects.create_user(username='doctorj', password='brogrammers', email='dj@healthnet.net',
                                     first_name='Julius', last_name='Erving'),
            User.objects.create_user(username='doctorwho', password='brogrammers', email='dw@healthnet.net',
                                     first_name='Matt', last_name='Smith'),
            User.objects.create_user(username='doctorock', password='brogrammers', email='do@healthnet.net',
                                     first_name='Otto', last_name='Octavius')
        ]

        for user in user_list:
            user.is_staff = True
            user.save()
            doctor = Doctor(user=user)
            doctor.save()

    def _create_nurses(self):

        user_list = [
            User.objects.create_user(username='nurse', password='brogrammers', email='n@healthnet.net',
                                     first_name='Carla', last_name='Espinosa'),
            User.objects.create_user(username='nursegregg', password='brogrammers', email='ng@healthnet.net',
                                     first_name='Gregg', last_name='Focker'),

        ]

        for user in user_list:
            user.is_staff = True
            user.save()
            nurse = Nurse(user=user)
            nurse.save()

    def _create_patients(self):
        user1 = User.objects.create_user(username='kevin', password='kevin', email='kb@healthnet.net',
                                         first_name='Kevin', last_name='B')
        user2 = User.objects.create_user(username='mason', password='mason', email='mm@healthnet.net',
                                         first_name='Mason', last_name='M')
        user3 = User.objects.create_user(username='nik', password='nik', email='nt@healthnet.net',
                                         first_name='Nik', last_name='T')
        user4 = User.objects.create_user(username='ed', password='ed', email='ew@healthnet.net',
                                         first_name='Ed', last_name='W')
        user5 = User.objects.create_user(username='jake', password='jake', email='jy@healthnet.net',
                                         first_name='Jake', last_name='Y')

        user1.save()
        user2.save()
        user3.save()
        user4.save()
        user5.save()

        patient1 = Patient(user=user1, doctor=Doctor.objects.get(id=1), height="5'11\"",
                           hospital=Hospital.objects.get(id=1))
        patient2 = Patient(user=user2, doctor=Doctor.objects.get(id=1), height="5'11\"",
                           hospital=Hospital.objects.get(id=1))
        patient3 = Patient(user=user3, doctor=Doctor.objects.get(id=2), height="5'11\"",
                           hospital=Hospital.objects.get(id=2))
        patient4 = Patient(user=user4, doctor=Doctor.objects.get(id=2), height="5'11\"",
                           hospital=Hospital.objects.get(id=2))
        patient5 = Patient(user=user5, doctor=Doctor.objects.get(id=3), height="5'11\"",
                           hospital=Hospital.objects.get(id=3))

        patient1.save()
        patient2.save()
        patient3.save()
        patient4.save()
        patient5.save()

    def _create_appointments(self):

        app_list = [
            Appointment(patient_ID=Patient.objects.get(id=1), doctor_ID=Doctor.objects.get(id=1), location='Rochester',
                        date=timezone.now(),
                        time=timezone.now(), endTime=timezone.now() + timezone.timedelta(hours=1),
                        description='Stitches'),
            Appointment(patient_ID=Patient.objects.get(id=1), doctor_ID=Doctor.objects.get(id=1), location='Rochester',
                        date=timezone.now() + timezone.timedelta(days=1),
                        time=timezone.now(), endTime=timezone.now() + timezone.timedelta(hours=1),
                        description='Physical'),
            Appointment(patient_ID=Patient.objects.get(id=1), doctor_ID=Doctor.objects.get(id=1), location='Rochester',
                        date=timezone.now() + timezone.timedelta(days=3),
                        time=timezone.now(), endTime=timezone.now() + timezone.timedelta(hours=1),
                        description='Therapy'),
            Appointment(patient_ID=Patient.objects.get(id=2), doctor_ID=Doctor.objects.get(id=1), location='Rochester',
                        date=timezone.now(),
                        time=timezone.now() + timezone.timedelta(hours=2),
                        endTime=timezone.now() + timezone.timedelta(hours=3),
                        description='Orthopedics'),
            Appointment(patient_ID=Patient.objects.get(id=2), doctor_ID=Doctor.objects.get(id=1), location='Rochester',
                        date=timezone.now() + timezone.timedelta(days=2),
                        time=timezone.now(), endTime=timezone.now() + timezone.timedelta(hours=1),
                        description='Triple Bi Pass'),
            Appointment(patient_ID=Patient.objects.get(id=3), doctor_ID=Doctor.objects.get(id=2),
                        location='Canandaiguia', date=timezone.now(),
                        time=timezone.now(), endTime=timezone.now() + timezone.timedelta(hours=1),
                        description='Rehabilitation'),
            Appointment(patient_ID=Patient.objects.get(id=3), doctor_ID=Doctor.objects.get(id=2),
                        location='Canandaiguia',
                        date=timezone.now() + timezone.timedelta(days=1),
                        time=timezone.now(), endTime=timezone.now() + timezone.timedelta(hours=1),
                        description='Ligament tear'),
            Appointment(patient_ID=Patient.objects.get(id=4), doctor_ID=Doctor.objects.get(id=2),
                        location='Canandaiguia', date=timezone.now(),
                        time=timezone.now() + timezone.timedelta(hours=2),
                        endTime=timezone.now() + timezone.timedelta(hours=3),
                        description='ACL Tear'),
            Appointment(patient_ID=Patient.objects.get(id=4), doctor_ID=Doctor.objects.get(id=2),
                        location='Canandaiguia',
                        date=timezone.now() + timezone.timedelta(days=4),
                        time=timezone.now(), endTime=timezone.now() + timezone.timedelta(hours=1),
                        description='Eye examination'),
            Appointment(patient_ID=Patient.objects.get(id=5), doctor_ID=Doctor.objects.get(id=3), location='Maryland',
                        date=timezone.now(),
                        time=timezone.now(), endTime=timezone.now() + timezone.timedelta(hours=1),
                        description='Physical')
        ]

        for app in app_list:
            app.save()

    def handle(self, *args, **options):
        self._create_superuser()
        self._create_hospitals()
        self._create_doctors()
        self._create_nurses()
        self._create_patients()
        self._create_appointments()
