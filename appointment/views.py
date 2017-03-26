from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
import json
from .forms import AppointmentForm, UpdateAppointmentForm
from .models import Appointment
from userprofile.models import Patient, Doctor, Nurse
from log.models import Entry
from django.views.generic import View

from userprofile.factory import UserFactory


@login_required(login_url='/userprofile/login')
def appointment_detail(request, appointment_id):
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
            return render(request, 'healthnet/appointment/appointment_detail.html', {'appointment': appointment, 'base_template' : "base.hhtml"})

        # If the user selects Delete page

        elif request.method == "POST":
            appointment.delete()
            logEntry = Entry()
            logEntry.user = request.user.username
            logEntry.trigger = "appointment.views.appointment_detail"
            logEntry.activity = "Deleted Appointment"
            logEntry.save()

            return HttpResponseRedirect("/appointments/view")
    else:
        return HttpResponse("You tried accessing an appointment that is not yours")


class AppointmentEdit(View):
    """ Edit existing appointments
        using the UpdateAppointmentsForm

    """

    update_form_class = UpdateAppointmentForm
    template_name = 'healthnet/appointment/update_appointment.html'

    #@login_required(login_url='/userprofile/login')
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

            # Nurses and Doctors are able to view any patients appointment
            # Patients can only view their appointments

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

    #@login_required(login_url='/userprofile/login')
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

                return redirect('/appointments/view')

            return render(request, self.template_name, {'appointment_update_form': appointment_update_form})
        return redirect('/userprofile/login')

@login_required(login_url='/userprofile/login')
def view(request):
    """ Get a list of user appointments

    :param request: The user who is making the request
    :return: A page that renders the list of existing appointments
    """

    # Build the list of appointment based on the type of user

    appointment_list = []

    user = UserFactory.get_user(request)

    if UserFactory.isNurse(user):
        appointment_list = Appointment.objects.all().order_by('date')
    elif UserFactory.isDoctor(user):
        appointment_list = Appointment.objects.filter(doctor_ID=user.id).order_by('date')
    elif UserFactory.isPatient(user):
        appointment_list = Appointment.objects.filter(patient_ID=user.id).order_by('date')
    else:
        return HttpResponse("You tried accessing an appointment that is not yours")

    context = {
        'appointment_list': appointment_list
    }
    return render(request, 'healthnet/appointment/appointments_view.html', context)


@login_required(login_url='/userprofile/login')
def index(request):
    """ Appointment app home page

    :param request: The user that is making the request
    :return: The appointment home page
    """
    return render(request, 'healthnet/appointment/appointments.html', )


# @login_required(login_url='/userprofile/login')
class CreateAppointment(View):
    """ Create a new appointment

    :param request: The user who is making the request
    :return: On GET, a new create appointment form. On POST, if the
        from is valid, save the appointment and redirect to the appointment
        app home page. If invalid, re-render the form or display an Http error message.
    """

    template_name = 'healthnet/create.html'

    def get(self, request):
        form = AppointmentForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)

            # make sure to check if time start is greater than time end.
            if appointment.valid_end_time() and appointment.valid_date():

                user = UserFactory.get_user(request)

                appointment.patient_ID = user
                appointment.doctor_ID = user.doctor

                doctor = user.doctor

                # filter appointments that have the appointments doctor and are on the same date
                # if appointment to be created starts within duration of start time, do not create
                try:
                    existing_appointment_list = Appointment.objects.filter(doctor_ID=doctor.id).filter(
                        date=appointment.date)
                    for existing_appointment in existing_appointment_list:
                        if existing_appointment.time <= appointment.time <= existing_appointment.endTime:
                            errormsg = '- Doctor is busy at this time, please try a different time or date.'
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
                return HttpResponseRedirect('/appointments/')

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


# The page the holds the calendar
@login_required(login_url='/userprofile/login')
def calendar(request):
    """ Load the calendar Page

    :param request: The user who is making the request
    :return: Render the Fullcalendar page
    """

    return render(request, 'healthnet/calendar.html')


# Page that holds the feed for calendar
def patient_calendar_feed(request):
    """ A json feed for the Calendar page

    :param request: the user who is making the request.
    :return: A json dictionary
    """

    # Create list of appointments depending on which user is logged in

    appointment_list = []

    user = UserFactory.get_user(request)

    if UserFactory.isNurse(user):
        appointment_list = Appointment.objects.all()
    elif UserFactory.isDoctor(user):
        appointment_list = Appointment.objects.filter(doctor_ID=user.id)
    elif UserFactory.isPatient(user):
        appointment_list = Appointment.objects.filter(patient_ID=user.id)
    else:
        return HttpResponse("You tried accessing an appointment that is not yours")

    json_list = []

    # Format the data from the django models so that they are
    # are compatible with the json format
    for appointment in appointment_list:
        id = appointment.id
        title = appointment.location
        start = appointment.date.strftime("%Y-%m-%dT")
        start += appointment.time.strftime("%H:%M:%S")

        end = appointment.date.strftime("%Y-%m-%dT")
        end += appointment.endTime.strftime("%H:%M:%S")

        url = "/appointments/" + id.__str__()

        allDay = False

        json_entry = {'title': title, 'id': id, 'start': start, 'end': end, 'allDay': allDay, 'url': url}
        json_list.append(json_entry)

    return HttpResponse(json.dumps(json_list), content_type='appliccation/json')
