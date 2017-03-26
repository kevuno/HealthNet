from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import MedicalRecordModelForm, TestResultModelForm
from .models import MedicalRecord, Prescription, TestResult
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from userprofile.factory import UserFactory
from userprofile.decorators import user_is_employee
from log.models import Entry


# Doctors viewing a list of prescriptions
@login_required(login_url='/userprofile/login')
@user_is_employee
def doctor_view_prescriptions(request):
    user = UserFactory.get_user(request)
    prescription_list = Prescription.objects.all()
    context = {
        'prescription_list': prescription_list
    }
    return render(request, 'healthnet/medrecord/doctor_view_prescriptions.html', context)


# Doctors view the details of prescriptions
@login_required(login_url='/userprofile/login')
@user_is_employee
def doctor_prescription_detail(request, prescription_id):
    prescription = Prescription.objects.get(pk=prescription_id)
    if request.method == "GET":
        return render(request, 'healthnet/medrecord/doctor_prescription_detail.html', {'prescription': prescription})


class UploadFile(View):
    """
        Doctors can Upload files that are saved in the media folder
    """
    template_name = 'healthnet/medrecord/upload.html'

    def get(self, request):
        form = MedicalRecordModelForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = MedicalRecordModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            logEntry = Entry()
            logEntry.user = request.user.username
            logEntry.trigger = "appointment.views.create"
            logEntry.activity = "Created Appointment"
            logEntry.save()
            return HttpResponseRedirect('/medrecord/view/uploads')

        return render(request, self.template_name, {'form': form})


# Employee view files that they have uploaded
@login_required(login_url='/userprofile/login')
@user_is_employee
def view_uploads(request):
    upload_list = MedicalRecord.objects.all()

    context = {
        'upload_list': upload_list
    }
    return render(request, 'healthnet/medrecord/view_uploads.html', context)


# Doctors view a list of tests they have made
@login_required(login_url='/userprofile/login')
@user_is_employee
def view_tests(request):
    test_list = TestResult.objects.all()

    context = {
        'test_list': test_list
    }
    return render(request, 'healthnet/medrecord/view_tests.html', context)


# Patients view a list of their prescriptions
@login_required(login_url='/userprofile/login')
def patient_view_prescriptions(request):
    user = UserFactory.get_user(request)
    prescription_list = Prescription.objects.filter(patient=user)
    context = {
        'prescription_list': prescription_list
    }
    return render(request, 'healthnet/view_prescriptions.html', context)


# Patients view their prescription details
@login_required(login_url='/userprofile/login')
def prescription_detail(request, prescription_id):
    prescription = Prescription.objects.get(pk=prescription_id)
    if request.method == "GET":
        return render(request, 'healthnet/prescription_detail.html', {'prescription': prescription})


# Lets patients view the tests that have been released
# By the doctor
@login_required(login_url='/userprofile/login')
def patient_view_tests(request):
    patient = UserFactory.get_user(request)

    test_list = TestResult.objects.filter(patient_ID=patient).filter(released=True)

    context = {
        'test_list': test_list
    }
    return render(request, 'healthnet/medrecord/patient_view_tests.html', context)


# Allows patients to view their test details
@login_required(login_url='/userprofile/login')
def patient_view_tests_details(request, test_id):
    test = TestResult.objects.get(pk=test_id)

    context = {
        'test': test
    }
    return render(request, 'healthnet/medrecord/patient_view_test_details.html', context)


# Doctors can view tests and release them
# If the doctors click the POST button it will change
# the release status of the test
@login_required(login_url='/userprofile/login')
@user_is_employee
def doctor_test_details(request, test_id):
    test = TestResult.objects.get(pk=test_id)
    if request.method == "GET":
        return render(request, 'healthnet/medrecord/doctor_view_test_details.html', {'test': test})

    if request.method == "POST":
        if test.released == True:
            test.released = False
            test.save()
        else:
            test.released = True
            test.save()
        return HttpResponseRedirect('/medrecord/view/tests')