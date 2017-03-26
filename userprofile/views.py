from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import Group
from django.views import generic
from django.views.generic import View
from log.models import Entry
from django.utils import timezone
from medrecord.models import Prescription, TestResult

from .models import Patient, Doctor

from .forms import UserForm, DoctorForm, NurseForm, PatientForm, LoginForm, PatientMedicalForm, UpdatePatientForm
from userprofile.factory import UserFactory

@login_required(login_url='/userprofile/login')
def indexView(request):
    """
    Renders the main view. Requires a logged user
    :param request: The browser request
    :return: The view
    """

    user = UserFactory.get_user(request)
    if user != None:
        return render(request, 'healthnet/userprofile.html', {'profileUser': user})
    else:
        return HttpResponse("Cannot display profile imformation at this time.")

@login_required(login_url='/userprofile/login')
def export(request):

    # Add entry to the log
    username = request.user.username

    logEntry = Entry()
    logEntry.user = username
    logEntry.trigger = "userprofile.views.export"
    logEntry.activity = "Exported Information"
    logEntry.save()

    userPrescriptions = Prescription.objects.filter(patient=request.user.patient)

    prescriptionsString = ""

    for p in userPrescriptions:
        prescriptionsString += str(p.medication) + "\n"
        prescriptionsString += "\t" + "Description: " + str(p.description) + "\n"
        prescriptionsString += "\t" + "Dosage:  " + str(p.dosage) + "\n"
        prescriptionsString += "\t" + "Quantity: " + str(p.quantity) + "\n"

    userTests = TestResult.objects.filter(patient_ID=request.user.patient)

    testsString = ""

    for t in userTests:
        if t.released == True:
            testsString += str(t.title) + "\n"
            testsString += "\t"+ str(t.description) + "\n"

    # Convert user's medical information into a text document

    fileContent = "Medical Information for: " + str(request.user.first_name) + " " + str(request.user.last_name) + "\n"\
                  "Request Time: " + str(timezone.localtime(timezone.now())) + "\n" \
                  "==================================================================\n" \
                  "MEDICAL INFORMATION\n" \
                  "Date of Birth:     " + str(request.user.patient.date_of_birth) + "\n" \
                  "Gender:            " + str(request.user.patient.gender) + "\n" \
                  "Height:            " + str(request.user.patient.height) + "\n" \
                  "Weight:            " + str(request.user.patient.weight) + "\n" \
                  "Phone Number:      " + str(request.user.patient.phone_number) + "\n" \
                  "Address:           " + str(request.user.patient.address) + "\n" \
                  "Emergency Contact: " + str(request.user.patient.emergency_contact) + "\n" \
                  "Emergency Number:  " + str(request.user.patient.emergency_number) + "\n" \
                  "Doctor:            " + str(request.user.patient.doctor.user.get_full_name()) + "\n" \
                  "Hospital:          " + str(request.user.patient.hospital.name) + "\n" \
                  "==================================================================\n" \
                  "PRESCRIPTIONS\n" \
                  "\n" + prescriptionsString +\
                  "==================================================================\n" \
                  "TESTS\n" \
                  "\n" + testsString
    res = HttpResponse(fileContent)
    res['Content-Disposition'] = 'attachment; filename=Medical_Information_'+str(request.user.username)+'.txt'
    return res


class PatientUserFormView(View):
    """
    View class for the form of creating a new user. Inherits the View class.
    """
    form_class = UserForm
    secondary_form_class = PatientForm
    third_form_class = PatientMedicalForm
    template_name = 'healthnet/patient_registration.html'

    def get(self, request):
        """
        Display the user_form, patient_form and patient_medical_form, with blank fields
        for new Patient to register.
        :param request: The browser request.
        :return: The form view
        """
        user_form = self.form_class(None)
        patient_form = self.secondary_form_class(None)
        patient_form.fields["doctor"].queryset = Doctor.objects.all()
        patient_medical_form = self.third_form_class(None)

        return render(request, self.template_name, {'user_form': user_form,
                                                    'patient_form': patient_form,
                                                    'patient_medical_form': patient_medical_form})

    # process form
    def post(self, request):
        """
        Processes the form for creating a user
        :param request: The browser request
        :return: The response view; the form view if the inputs where invalid
        or the user profile index if they were valid.
        """
        user_form = self.form_class(request.POST)
        patient_form = self.secondary_form_class(request.POST)
        patient_medical_form = self.third_form_class(request.POST)

        if user_form.is_valid() and patient_form.is_valid() and patient_medical_form.is_valid():

            user = user_form.save(commit=False)
            user.first_name.capitalize()
            user.last_name.capitalize()


            # Clean data so that it will enter db nicely
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']

            # Change users input for formatting purposes
            user.email = user_form.cleaned_data['email']

            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']

            # Cannot set user's password to normal text, have to use set_password
            user.set_password(password)

            # Save model instance to db
            user.save()

            # Hook up user to patient
            patient = patient_form.save(commit=False)

            # connect medical form to patient
            medical = patient_medical_form.save(commit=False)
            patient.gender = medical.gender
            patient.height = medical.height
            patient.weight = medical.weight
            patient.emergency_contact = medical.emergency_contact
            patient.emergency_number = medical.emergency_number

            # intentionally neglect to save medical form

            patient.user = user
            patient.save()

            logEntry = Entry()
            logEntry.user = username
            logEntry.trigger = "userprofile.views.PatientUserFormView"
            logEntry.activity = "Created Account"
            logEntry.save()

            # Returns User object if credentials are correct (logs them in)
            patient.user = authenticate(username=username, password=password)

            if patient.user is not None:
                if patient.user.is_active:
                    login(request, patient.user)
                    return redirect('userprofile:index')

        return render(request, self.template_name, {'user_form': user_form,
                                                    'patient_form': patient_form,
                                                    'patient_medical_form': patient_medical_form})


# @login_required(login_url="/userprofile/login")

class UpdateProfileView(View):
    """
    View class for the form of updating a user. Inherits the View class.
    """
    update_form_class = UpdatePatientForm
    template_name = 'healthnet/update_profile.html'

    # display a form for Patient to update some fields
    @method_decorator(login_required(login_url='/userprofile/login'))
    def get(self, request):
        """
        Display the patient_form with the information of the patient inside the fields.
        :param request: The browser request.
        :return: The form view
        """
        user_id = request.user.id
        #       print(user_id   )
        patient = Patient.objects.get(user=user_id)

        form_data = {'address': patient.address,
                     'city': patient.city,
                     'phone_number': patient.phone_number,
                     'height': patient.height,
                     'weight': patient.weight,
                     'emergency_contact': patient.emergency_contact,
                     'emergency_number': patient.emergency_number,
                     'insurance_provider': patient.insurance_provider,
                     'insurance_number': patient.insurance_number}

        patient_update_form = self.update_form_class(initial=form_data)

        return render(request, self.template_name, {'patient_update_form': patient_update_form})

    # process form
    @method_decorator(login_required(login_url='/userprofile/login'))
    def post(self, request):
        """
        Processes the form for updating a patient.
        :param request: The browser request
        :return: The response view; the form view if the inputs where invalid
        or the user profile index if they were valid.
        """
        user_id = request.user.id
        patient = Patient.objects.get(user=user_id)
        patient_update_form = self.update_form_class(request.POST, instance=patient)

        if patient_update_form.is_valid():
            # Save model instance to db
            #        patient_update_form.update()
            patient.save()

            logEntry = Entry()
            logEntry.user = request.user.username
            logEntry.trigger = "userprofile.views.UpdateProfileView"
            logEntry.activity = "Updated Patient"
            logEntry.save()

            return redirect('userprofile:index')

        return render(request, self.template_name, {'patient_update_form': patient_update_form})
