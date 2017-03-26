from .models import Doctor, Patient, Nurse, Hospital
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


class UserFactory(object):
    """ Factor that returns a type of user based on who is making
        the request

    """

    @staticmethod
    def get_user(request):

        try:
            user = Patient.objects.get(user=request.user.id)
        except ObjectDoesNotExist:
            try:
                user = Doctor.objects.get(user=request.user.id)
            except ObjectDoesNotExist:
                try:
                    user = Nurse.objects.get(user=request.user.id)
                except ObjectDoesNotExist:
                    return None

        return user

    def isNurse(user):
        """
        Checks if the user given is a nurse
        :param user: The given user
        :return: Boolean
        """
        return type(user) == Nurse

    def isDoctor(user):
        """
        Checks if the user given is a doctor
        :param user: The given user
        :return: Boolean
        """
        return type(user) == Doctor

    def isPatient(user):
        """
        Checks if the user given is a patient
        :param user: The given user
        :return: Boolean
        """
        return type(user) == Patient

    @staticmethod
    def getOtherPatients(doctor):
        """
        Process a doctor  passed in a view, and obtain the list of patients
        from hospitals not in the doctor hospital.

        :param doctor: The doctor passed in the view transfer_patient
        :return: An array of patients
        """
        doctor_hospital = doctor.hospital
        try:
            return Patient.objects.exclude(hospital=doctor_hospital)

        except ObjectDoesNotExist:
            return None

    @staticmethod
    def getPatients(doctor):
        """
        Process a request passed in a view, and obtain the list of patients
        from the given doctor

        :param doctor: The request doctor in the view transfer_patient
        :return: An array of patients
        """
        doctor_id = doctor.id
        try:
            return Patient.objects.filter(doctor= doctor_id)

        except ObjectDoesNotExist:
            return None