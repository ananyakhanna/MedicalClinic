from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Patient, User, Doctor
from django.db import transaction
from captcha.fields import CaptchaField

class PatientRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, max_length=100)
    last_name = forms.CharField(required=False,max_length=100)
    phone_number = forms.IntegerField(required=True, min_value=1000000000, max_value=9999999999)
    location = forms.CharField(required=True, max_length=100)
    captcha = CaptchaField()

    class Meta(UserCreationForm.Meta):
        model = User
        # widgets={
        #     'username': forms.TextInput(attrs={'class':'form-control'}),
        #     'password1': forms.PasswordInput(attrs={'class':'form-control'}),
        #     'password2': forms.PasswordInput(attrs={'class':'form-control'}),
        #     'first_name': forms.TextInput(attrs={'class':'form-control'}),
        #     'last_name': forms.TextInput(attrs={'class':'form-control'}),
        #     'phone_number': forms.NumberInput(attrs={'class':'form-control'}),
        #     'location': forms.TextInput(attrs={'class':'form-control'}),
        # }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_patient = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        patient = Patient.objects.create(user = user)
        patient.phone_number = self.cleaned_data.get('phone_number')
        patient.location = self.cleaned_data.get('location')
        patient.save()
        return user

class DoctorRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)
    phone_number = forms.IntegerField(required=True, min_value=1000000000, max_value=9999999999)
    speciality = forms.ChoiceField(required=True, choices=Doctor.TYPE_SPECIALITY)
    captcha = CaptchaField()

    class Meta(UserCreationForm.Meta):
        model = User
        # widgets={
        #     'username': forms.TextInput(attrs={'class':'form-control'}),
        #     'password1': forms.PasswordInput(attrs={'class':'form-control'}),
        #     'password2': forms.PasswordInput(attrs={'class':'form-control'}),
        #     'first_name': forms.TextInput(attrs={'class':'form-control'}),
        #     'last_name': forms.TextInput(attrs={'class':'form-control'}),
        #     'phone_number': forms.NumberInput(attrs={'class':'form-control'}),
        #     'speciality': forms.TextInput(attrs={'class':'form-control'}),
        # }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_doctor = True
        user.is_staff = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        doctor = Doctor.objects.create(user = user)
        doctor.phone_number = self.cleaned_data.get('phone_number')
        doctor.speciality = self.cleaned_data.get('speciality')
        doctor.save()
        return user


# class AppointmentForm(forms.ModelForm):
#     pass

class MyForm(forms.Form):
    captcha = CaptchaField()