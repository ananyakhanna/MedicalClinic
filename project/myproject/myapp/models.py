from asyncio.windows_events import NULL
from tkinter import CASCADE
from django.urls import reverse
from pickle import TRUE
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # is_admin = models.BooleanField('Is Admin', default = False)
    is_patient = models.BooleanField('Is Patient', default = False)
    is_doctor = models.BooleanField('Is Doctor', default = False)

    def __str__(self):
        return self.username

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=TRUE)
    phone_number = models.CharField(max_length=10)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('login_view') 

class Doctor(models.Model):

    Dermatology = 'Dermatology'
    Cardiology = 'Cardiology'
    Gastroenterology = 'Gastroenterology'
    Neurology = 'Neurology'
    Obsterics_Gynecology = 'Obsterics/Gynecology'
    Pediatrics = 'Pediatrics'
    Ophthalmology = 'Ophthalmology'
    Psychiatry = 'Psychiatry'
    Urology = 'Urology'
    Emergency_medicine = 'Emergency medicine'

    TYPE_SPECIALITY = [
        (Dermatology, 'Dermatology'),
        (Cardiology, 'Cardiology'),
        (Gastroenterology, 'Gastroenterology'),
        (Neurology, 'Neurology'),
        (Obsterics_Gynecology, 'Obsterics/Gynecology'),
        (Pediatrics, 'Pediatrics'),
        (Ophthalmology, 'Ophthalmology'),
        (Psychiatry, 'Psychiatry'),
        (Urology, 'Urology'),
        (Emergency_medicine, 'Emergency medicine')

    ]


    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=TRUE)
    phone_number = models.CharField(max_length=10)
    speciality = models.CharField(max_length=50, choices=TYPE_SPECIALITY)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('login_view')




class Appointment(models.Model):
    INPATIENT = 'Inpatient'
    OUTPATIENT = 'Outpatient'

    TYPE = [
        (INPATIENT, 'Inpatient'),
        (OUTPATIENT, 'Outpatient')
    ]


    Dermatology = 'Dermatology'
    Cardiology = 'Cardiology'
    Gastroenterology = 'Gastroenterology'
    Neurology = 'Neurology'
    Obsterics_Gynecology = 'Obsterics/Gynecology'
    Pediatrics = 'Pediatrics'
    Ophthalmology = 'Ophthalmology'
    Psychiatry = 'Psychiatry'
    Urology = 'Urology'
    Emergency_medicine = 'Emergency medicine'

    TYPE_SPECIALITY = [
        (Dermatology, 'Dermatology'),
        (Gastroenterology, 'Gastroenterology'),
        (Cardiology, 'Cardiology'),
        (Neurology, 'Neurology'),
        (Obsterics_Gynecology, 'Obsterics/Gynecology'),
        (Pediatrics, 'Pediatrics'),
        (Ophthalmology, 'Ophthalmology'),
        (Psychiatry, 'Psychiatry'),
        (Urology, 'Urology'),
        (Emergency_medicine, 'Emergency medicine')

    ]


    # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=TRUE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # username = models.CharField(max_length=100, unique=True, error_messages={"unique": _("A user with that username already exists."),},)
    contactno = models.BigIntegerField()
    type = models.CharField(max_length=50, choices=TYPE)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=200)
    date = models.DateField(default=datetime.now, blank=True)
    time = models.TimeField(default=datetime.now, blank=True)
    services = models.CharField(max_length=100, choices=TYPE_SPECIALITY)
    sent_date = models.DateField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    accepted_date = models.DateField(auto_now_add=False, null=True, blank=True)
    checkupstatus = models.BooleanField(default= False)
    bill_generated = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-sent_date'] 
        
# class PatientStatus(models.Model):
#     user = models.ForeignKey(Appointment, on_delete=None)
#     # doctor_summery
#     # checkup_status
    
    
class Billing(models.Model):
    user = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True)
    billNo = models.BigIntegerField(null=True, blank=True,)
    name = models.CharField(max_length=100, null=True, blank=True)
    contactno = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    doa = models.CharField(max_length=100, null=True, blank=True)
    consultationFee = models.FloatField(null=True, blank=True)
    docFee = models.FloatField(null=True, blank=True)
    miscCharge = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class Doctor_Summary(models.Model):
    user = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    illness = models.CharField(max_length=100)
    medication = models.CharField(max_length=1000)    
    dosage = models.CharField(max_length=500)    
    vaccination = models.CharField(max_length=500)    
    note = models.CharField(max_length=1000)  


class MCQTest(models.Model):
    question = models.CharField(max_length=200)
    option1 = models.CharField(max_length=10)
    option2 = models.CharField(max_length=10)
    answer = models.CharField(max_length=10) 


class Ipreg(models.Model):
    patientID = models.BigIntegerField()
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.CharField(max_length=500)
    contactNo = models.BigIntegerField()
    regDate = models.DateField(default=datetime.now, blank=True)
    roomNo = models.IntegerField()
    gender = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Opreg(models.Model):
    patientID = models.BigIntegerField()
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    contactNo = models.BigIntegerField()
    date = models.DateField(default=datetime.now, blank=True)
    department = models.CharField(max_length=100)
    docName = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Docinfo(models.Model):
    docID = models.BigIntegerField()
    docname = models.CharField(max_length=100)
    age = models.IntegerField()
    contactNo = models.BigIntegerField()
    department = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)

    def __str__(self):
        return self.docname

class Roominfo(models.Model):
    roomNo = models.IntegerField()
    roomType = models.CharField(max_length=100)

class Ipbilling(models.Model):
    billNo = models.BigIntegerField()
    patientID = models.BigIntegerField()
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    doa = models.DateField(default=datetime.now, blank=True)
    dod = models.DateField(default=datetime.now, blank=True)
    gender = models.CharField(max_length=100)
    roomCharge = models.FloatField()
    docFees = models.FloatField()

    def __str__(self):
        return self.name

class Opbilling(models.Model):
    billNo = models.BigIntegerField()
    patientID = models.BigIntegerField()
    name = models.CharField(max_length=100)
    date = models.DateField(default=datetime.now, blank=True)
    docname = models.CharField(max_length=100)
    coamt = models.FloatField()
    totalamt = models.FloatField()

    def __str__(self):
        return self.name

class Pathology(models.Model):
    patientID = models.BigIntegerField()
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=100)
    testname = models.CharField(max_length=500)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name

