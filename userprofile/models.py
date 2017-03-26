from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

# Add a third option who do not identify
GENDERS = (('M', 'Male'),
           ('F', 'Female'))


class Hospital(models.Model):
    name = models.CharField(max_length=50, default='Hospital')
    address = models.CharField(validators=[RegexValidator(regex='^\d+\s[a-zA-z]+\s[a-zA-z\s]+',
                                                          message='Address should be formatted as [Number][Street name]')],
                                                          max_length=30, default='')

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, default=2)

    def __str__(self):
        return self.user.username



class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, default=2)


    def __str__(self):
        return self.user.username


class Patient(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=1)
    date_of_birth = models.DateField(("Birthday"), default=timezone.now()) #Because django's user does not have birthday field
    phone_number = models.CharField(validators=[RegexValidator(regex='^[0-9]+$',
                                                               message='Phone number can only contain numbers')],
                                                               max_length=10, default='')
    address = models.CharField(validators=[RegexValidator(regex='^\d+\s[a-zA-z]+\s[a-zA-z\s]+',
                                                          message='Address should be formatted as [Number][Street name]')],
                                                          max_length=30, default='')
    city = models.CharField(validators=[RegexValidator(regex='[a-zA-Z\'-]',
                            message='City name can only contain letters, apostrophes, and/or dashes')],
                            max_length=20 , default='') #[a-zA-Z]
    gender = models.CharField(max_length=1, choices=GENDERS, default='Male')
    height = models.CharField(validators=
                            [RegexValidator(regex='(^[1-8]\'\s?([0-9]|1[0-1])(\'\'|\"))$|(^[0]\'\s?([1-9]|1[0-1])(\'\'|\"))$',
                                            message='Height needs to be in the form FEET\'INCHES\" and needs to be at least 0\'0\"')],
                                            max_length=6, default='')
    weight = models.CharField(validators=[RegexValidator(regex='^[1-9][0-9]*$',
                                              message='Weight must be greater than 0 lbs')],
                                              verbose_name= 'Weight(lb)',
                                              max_length=3,
                                              default='')
    emergency_contact = models.CharField(validators=[RegexValidator(regex='[a-zA-Z\'-.]',
                                         message='Emergency contact should only contain letters, apostrophes, dashes, and/or periods')],
                                         max_length=30, default='') #[a-zA-Z]
    emergency_number = models.CharField(validators=[RegexValidator(regex='^[0-9]+$',
                                                                   message='Emergency number can only contain numbers')],
                                                                   max_length=10, default='')
    insurance_provider = models.CharField(max_length=50, default='')
    insurance_number = models.CharField(max_length=20, default='')

    #Hospital represents which hospital they are in.
    #Null represents not checked in to any hospital
    hospital = models.ForeignKey(Hospital, default=1)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    def getInfo(self):
        info = [self.__str__(), self.doctor, self.date_of_birth, self.phone_number, self.address, self.city,
                self.insurance_provider, self.insurance_number, self.height, self.weight, self.gender, self.hospital,
                self.emergency_contact, self.emergency_number]
        return info

