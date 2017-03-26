from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from appointment.models import Appointment
from userprofile.models import Patient, Doctor, Nurse, Hospital
from log.models import Entry
from django.views.generic import View
from .forms import DoctorAppointmentForm, DoctorMessageForm, DoctorMedicalForm
from medrecord.forms import PrescriptionModelForm, TestResultModelForm
from userprofile.factory import UserFactory
from userprofile.models import User
from django.utils import timezone
from messaging.models import Message
from userprofile.forms import DischargeForm
from appointment.forms import AppointmentForm, UpdateAppointmentForm
import json


class DoctorCreateAppointment(View):
    """ Create a new appointment

    :param request: The user who is making the request
    :return: On GET, a new create appointment form. On POST, if the
        from is valid, save the appointment and redirect to the appointment
        app home page. If invalid, re-render the form or display an Http error message.
    """
    template_name = 'healthnet/employee/appointment.html'

    @method_decorator(login_required(login_url='/userprofile/login'))
    def get(self, request):
        user = UserFactory.get_user(request)

        if UserFactory.isNurse(user):
            possible_patients = Patient.objects.filter(hospital=user.hospital)
        elif UserFactory.isDoctor(user):
            possible_patients = Patient.objects.filter(doctor_id=user.id)
        else:
            return HttpResponse("You are not cleared access to this.")

        form = DoctorAppointmentForm()
        form.fields['patient_ID'].queryset = possible_patients
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required(login_url='/userprofile/login'))
    def post(self, request):
        form = DoctorAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)

            # make sure to check if time start is greater than time end.
            if appointment.valid_end_time() and appointment.valid_date():
                # Nurses can only view the patients from the hospital the nurse belongs to
                # Doctors can only view their own patients
                user = UserFactory.get_user(request)
                if(UserFactory.isDoctor(request.user)):
                    appointment.doctor_ID = request.user.id
                elif(UserFactory.isNurse(request.user)):
                    appointment.doctor_ID = Patient.objects.get(id=appointment.patient_ID).doctor.id

                # filter appointments that have the appointments doctor and are on the same date
                # if appointment to be created starts within duration of start time, do not create
                try:
                    existing_appointment_list = Appointment.objects.filter(doctor_ID=user.id).filter(
                        date=appointment.date)
                    for existing_appointment in existing_appointment_list:
                        if existing_appointment.time <= appointment.time <= existing_appointment.endTime:
                            errormsg = 'Time not available'
                            return render(request, self.template_name, {'form': form, 'errormsg': errormsg})

                except ObjectDoesNotExist:
                    pass  # no need to check
                else:
                    pass

                appointment.save()

                logEntry = Entry()
                logEntry.user = request.user.username
                logEntry.trigger = "appointment.views.create"
                logEntry.activity = "Created Appointment"
                logEntry.save()
                return HttpResponseRedirect('/employee/appointment/view')

            # need to return an error message saying why page is being re-rendered
            elif not appointment.valid_date():
                errormsg = '- Appointment must be scheduled at a future date.'
                return render(request, self.template_name, {'form': form, 'errormsg': errormsg})

            elif not appointment.valid_end_time():
                errormsg = '- Appointment end time must be after start time.'
                return render(request, self.template_name, {'form': form, 'errormsg': errormsg})

            # need to return an error message saying why page is being re-rendered
            else:
                errormsg = '- Doctor is busy at this time, please try a different time or date.'
                return render(request, self.template_name, {'form': form, 'errormsg': errormsg})

        return render(request, self.template_name, {'form': form})


class DoctorAppointmentEdit(View):
    """ Edit existing appointments
        using the UpdateAppointmentsForm

    """

    update_form_class = UpdateAppointmentForm
    template_name = 'healthnet/employee/doctor_edit_appointment.html'

    # @login_required(login_url='/userprofile/login')
    def get(self, request, appointment_id):

        """ When loading the page, the fields
            should be filled with their existing values

        :param request: The user who is requesting the page
        :param appointment_id: The unique id of the appointment to be edited
        :return: If the request is valid, a page that has a form loaded with the current
            appointment information. Otherwise, an HttpResponse with an error message
        """

        if request.user.is_authenticated():
            appointment = Appointment.objects.get(id=appointment_id)

            # Obtain the user from the UserFactory class
            user = UserFactory.get_user(request)



            if user != None and appointment.can_view(user):
                appointment_update_form = self.update_form_class(None)

                # Loading form with Appointment Data

                form_data = {'description': appointment.description,
                             'location': appointment.location,
                             'date': appointment.date,
                             'time': appointment.time,
                             'endTime': appointment.endTime, }

                appointment_update_form = self.update_form_class(initial=form_data)

                return render(request, self.template_name, {'appointment_update_form': appointment_update_form})
            else:
                return HttpResponse("You tried editing an appointment that is not yours")
        return redirect('/userprofile/login')

    # @login_required(login_url='/userprofile/login')
    def post(self, request, appointment_id):

        """ Submitting the for will update the current appointment

        :param request: The user who is requesting the page
        :param appointment_id: The unique id of the Appointment to be updated
        :return: If there form is valid, redirect the user to the views page.
            If the form is not valid, re-render the page
        """

        if request.user.is_authenticated():
            appointment = Appointment.objects.get(id=appointment_id)
            appointment_update_form = self.update_form_class(request.POST, instance=appointment)
            if appointment_update_form.is_valid():
                appointment.save()

                logEntry = Entry()
                logEntry.user = request.user.username
                logEntry.trigger = "appointment.views.AppointmentEdit"
                logEntry.activity = "Updated Appointment"
                logEntry.save()

                return redirect('/employee/appointment/view')

            return render(request, self.template_name, {'appointment_update_form': appointment_update_form})
        return redirect('/userprofile/login')


@login_required(login_url='/userprofile/login')
def home(request):
    return render(request, template_name='healthnet/employee/doctor_home.html')


@login_required(login_url='/userprofile/login')
def calendar(request):
    """ Load the calendar Page

    :param request: The user who is making the request
    :return: Render the Fullcalendar page
    """
    return render(request, 'healthnet/employee/doctor_calendar.html')


@login_required(login_url='/userprofile/login')
def patient_options(request, patient_id):
    """ View employee's options for a single patient. Inherits the view class.
    """
    try:
        patient = Patient.objects.get(pk=patient_id)
        request.patient = patient
    except Patient.DoesNotExist:
        raise Http404("Patient does not exist")

    # Obtain the user from the UserFactory class
    user = UserFactory.get_user(request)

    # block null user
    if user == None:
        return HttpResponse("You aren't a real doctor or nurse, get outta here!!")

    doctor = UserFactory.get_user(request)
    possible_patients = UserFactory.getPatients(doctor)

    # Get the forms
    prescription_form = PrescriptionModelForm
    test_form = TestResultModelForm
    discharge_form = DischargeForm
    medical_form = DoctorMedicalForm
    patient_info = patient.getInfo()

    patient_name = patient.__str__()
    user_is_doctor = UserFactory.isDoctor(user)
    prescription_form.field_order = ['patient', 'medication', 'dosage', 'quantity', 'description']
    test_form.field_order = ['title', 'description', 'released']

    context = {
        'patient_info': patient_info,
        'user': user,
        'prescription_form': prescription_form,
        'test_form': test_form,
        'discharge_form': discharge_form,
        'patient_name': patient_name,
        'user_is_doctor': user_is_doctor,
        'patient': patient,
        'medical_form': medical_form
    }
    # Get request to render page.
    if request.method == "GET":
        return render(request, 'healthnet/employee/patient_options.html', context)
    # Form is submitted and processed.
    elif request.method == "POST":
        prescription_form = prescription_form(request.POST)
        discharge_form = discharge_form(request.POST)
        medical_form = medical_form(request.POST, instance= patient)
        test_form = test_form(request.POST)
        if prescription_form.is_valid():
            prescription = prescription_form.save(commit=False)
            prescription.patient = patient
            prescription.save()
            logEntry = Entry()
            logEntry.user = request.user.username
            logEntry.trigger = "employee.views.patient_options"
            logEntry.activity = "Created prescription for " + str(patient.user.username)
            logEntry.save()
            return render(request, 'healthnet/employee/patient_options.html', context)
        elif medical_form.is_valid():
            medical_form.save()
            patient = Patient.objects.get(pk=patient_id)
            patient_info = patient.getInfo()
            context = {
                'patient_info': patient_info,
                'user': user,
                'prescription_form': prescription_form,
                'test_form': test_form,
                'discharge_form': discharge_form,
                'patient_name': patient_name,
                'user_is_doctor': user_is_doctor,
                'patient': patient,
                'medical_form': medical_form
            }
            logEntry = Entry()
            logEntry.user = request.user.username
            logEntry.trigger = "employee.views.patient_options"
            logEntry.activity = "Updated " + str(patient.user.username) + "'s medical information"
            logEntry.save()
            return render(request, 'healthnet/employee/patient_options.html', context)
        elif discharge_form.is_valid():
            prev_hospital = patient.hospital
            patient.hospital = Hospital.objects.get(name = "Not in hospital")
            patient.save()
            logEntry = Entry()
            logEntry.user = request.user.username
            logEntry.trigger = "employee.views.patient_options"
            logEntry.activity = "Discharged " + str(patient.user.username) + " from " + str(prev_hospital)
            logEntry.save()
            return render(request, 'healthnet/employee/patient_options.html', context)
        elif test_form.is_valid():
            test = test_form.save(commit=False)
            test.patient_ID = patient
            test.save()
            logEntry = Entry()
            logEntry.user = request.user.username
            logEntry.trigger = "employee.views.patient_options"
            logEntry.activity = "Created test for " + str(patient.user.username)
            logEntry.save()
            return render(request, 'healthnet/employee/patient_options.html', context)
        else:
            # How to redirect to same url and pop up window
            context['errormsg'] = "Error in form, did not save."

            return render(request, 'healthnet/employee/patient_options.html', context)

@login_required(login_url='/userprofile/login')
def transfer_patient(request):
    """
        View to transfer patient for other hospital to his/her list of patients
    """
    doctor = UserFactory.get_user(request)
    if(request.method == "GET"):

        patient_list = UserFactory.getOtherPatients(doctor)


        context = {
            'patient_list': patient_list
        }
        return render(request, 'healthnet/employee/transfer_patient.html', context)
    elif(request.method == "POST"):
        patient_id = request.POST.get('patient', None)
        patient = Patient.objects.get(id = patient_id)
        patient.hospital = doctor.hospital
        patient.doctor = doctor
        patient.save()
        logEntry = Entry()
        logEntry.user = request.user.username
        logEntry.trigger = "employee.views.patient_tranfer"
        logEntry.activity = str(patient.user.username) + " transfered to " + str(patient.hospital)
        logEntry.save()        
        return HttpResponseRedirect('patient_list')


def admit_patient(request):
    """
        View to admit patient to a hospital from a list of patients not in hospitals
    """
    employee = UserFactory.get_user(request)

    hospital = Hospital.objects.get(name="Not in hospital")

    if (request.method == "GET"):

        patient_list = Patient.objects.filter(hospital=hospital)

        context = {
            'patient_list': patient_list
        }
        return render(request, 'healthnet/employee/admit_patient.html', context)
    elif (request.method == "POST"):
        patient_id = request.POST.get('patient', None)
        patient = Patient.objects.get(id=patient_id)
        patient.hospital = employee.hospital
        patient.save()
        logEntry = Entry()
        logEntry.user = request.user.username
        logEntry.trigger = "employee.views.patient_admit"
        logEntry.activity = str(patient.user.username) + " admitted to " + str(patient.hospital)
        logEntry.save()
        return HttpResponseRedirect('patient_list')

@login_required(login_url='/userprofile/login')
def view(request):
    """ Get a list of user patients

    :param request: The user who is making the request
    :return: A page that renders the list of the given employee's patients
    """

    # Build the list of patients based on the user

    patient_list = []

    user = UserFactory.get_user(request)

    if UserFactory.isNurse(user):
        patient_list = Patient.objects.filter(hospital=user.hospital)
    elif UserFactory.isDoctor(user):
        patient_list = Patient.objects.filter(doctor_id=user.id)
    else:
        return HttpResponse("You are not cleared access to this.")

    context = {
        'patient_list': patient_list
    }
    return render(request, 'healthnet/employee/patient_list.html', context)


@login_required(login_url='/userprofile/login')
def view_appointments(request):
    """ Get a list of user appointments

    :param request: The user who is making the request
    :return: A page that renders the list of existing appointments
    """

    # Build the list of appointment based on the type of user

    appointment_list = []

    user = UserFactory.get_user(request)
    if UserFactory.isNurse(user):
        appointment_list = Appointment.objects.filter(patient_ID__hospital=user.hospital)
    elif UserFactory.isDoctor(user):
        appointment_list = Appointment.objects.filter(doctor_ID=user.id).order_by('date')
    elif UserFactory.isPatient(user):
        appointment_list = Appointment.objects.filter(patient_ID=user.id).order_by('date')
    else:
        return HttpResponse("You tried accessing an appointment that is not yours")

    context = {
        'appointment_list': appointment_list
    }
    return render(request, 'healthnet/employee/view_appointments.html', context)


@login_required(login_url='/userprofile/login')
def doctor_appointment_detail(request, appointment_id):
    """ View details of an appointment

    :param request: The user who is requesting the page
    :param appointment_id: The unique id of the appointment to query
    :return: If the request is valid, return a page that renders the Appointment Information.
        If the request is invalid, return an Web page displaying error text.
    """

    # See if the appointment exists
    try:
        appointment = Appointment.objects.get(pk=appointment_id)
    except Appointment.DoesNotExist:
        raise Http404("Appointment does not exist")

    # Obtain the user from the UserFactory class
    user = UserFactory.get_user(request)

    # Nurses and Doctors are able to view any patients appointment
    # Patients can only view their appointments

    if user != None and appointment.can_view(user):

        if request.method == "GET":
            return render(request, 'healthnet/employee/doctor_appointment_details.html', {'appointment': appointment})

        # If the user selects Delete page

        elif request.method == "POST":
            appointment.delete()
            logEntry = Entry()
            logEntry.user = request.user.username
            logEntry.trigger = "appointment.views.appointment_detail"
            logEntry.activity = "Deleted Appointment"
            logEntry.save()

            return HttpResponseRedirect("/employee/appointment/view")
    else:
        return HttpResponse("You tried accessing an appointment that is not yours")


def DoctorInbox(request):
    message_list = Message.objects.filter(to=request.user.email)
    context = {
        'message_list': message_list
    }
    return render(request, 'healthnet/employee/employee_messages_inbox.html', context)


class DoctorComposeMessage(View):
    template = 'healthnet/employee/employee_messages_compose.html'

    @method_decorator(login_required(login_url='/userprofile/login'))
    def get(self, request):
        form = DoctorMessageForm(initial={'From': request.user.email})
        return render(request, self.template, {'form': form})

    # need to check if email exists
    @method_decorator(login_required(login_url='/userprofile/login'))
    def post(self, request):
        form = DoctorMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            if User.objects.filter(email=message.to).exists():
                message.From = request.user.first_name + ' ' + request.user.last_name + '<' + request.user.email + '>'
                message.date = timezone.now()
                message.time = timezone.now()
                message.save()

                # Add entry into the log
                logEntry = Entry()

                # determining who sent the message
                sender = User.objects.get(email=request.user.email)

                logEntry.user = sender.username
                logEntry.trigger = "messaging.views.ComposeMessage"
                logEntry.activity = "Sent Message"
                logEntry.save()

                return HttpResponseRedirect('/employee/messages/inbox')

            else:
                errormsg = '- The email that you tried to message does not exist.'
                return render(request, self.template, {'form': form, 'errormsg': errormsg})

        return render(request, self.template, {'form': form})

@login_required(login_url='/userprofile/login')
def doctor_message_detail(request, message_id):
    """
    Displays information associated with the selected message:
    To, From, Date & Time sent, Subject, and the message itself.
    Can delete the message.
    :param request: user
    :param message_id: id of the current message
    :return: renders message_detail.html on success
    """
    message = Message.objects.get(pk=message_id)
    if request.method == "GET":
        return render(request, 'healthnet/employee/employee_messages_detail.html', {'message': message})

    elif request.method == "POST":
        message.delete()

        # Add entry into the log
        logEntry = Entry()

        logEntry.user = request.user.username
        logEntry.trigger = "employee.views.doctor_message_detail"
        logEntry.activity = "Deleted Message"
        logEntry.save()
        return HttpResponseRedirect("/employee/messages/inbox")
