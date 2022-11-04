from asyncio.windows_events import NULL
from cgitb import text
from distutils.log import info
from email import message
import imp
from multiprocessing import Value, context
from optparse import Values
from unicodedata import name
from urllib import request
from webbrowser import get
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from myapp.forms import PatientRegisterForm, DoctorRegisterForm
from .models import Billing, Doctor_Summary, Ipreg, MCQTest, Opreg, Docinfo, Pathology, Roominfo, Ipbilling, Opbilling, User, Patient, Doctor, Appointment
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, TemplateView
from .forms import MyForm, PatientRegisterForm, DoctorRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from myapp import models
from django.views.generic import ListView
import datetime
from django.contrib.auth import get_user_model
from pip._vendor import requests 
import json
User = get_user_model()

# Create your views here.
def home(request):
    return render(request, 'home.html')


def index(request):
    return render(request, 'index.html')


def register(request):
    return render(request, 'register.html')


# search patient
def search_patient(request):
    context = {}
    qs = Appointment.objects.all()
    name_search_query = request.POST.get('name_search')
    date_min = request.POST.get('date_min')
    date_max = request.POST.get('date_max')
    bill_generated = request.POST.get('bill_generated')


    if name_search_query !='' and name_search_query is not None:
        qs = qs.filter(user__first_name__icontains=name_search_query)

    if date_min != '' and date_min is not None:
        qs = qs.filter(date__gte=date_min)

    if date_max != '' and date_max is not None:
        qs = qs.filter(date__lt=date_max)

    if bill_generated == 'on':
        qs = qs.filter(bill_generated=True)
    
    context['queryset'] = qs
    return render(request, 'search_patient.html', context)

# pdf generator
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
import os

# def render_to_pdf(template_scr, context_dict={}):
#     pass


def render_pdf_view(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if pdf.err:
        return HttpResponse('we had some errors')


    # context = {}
    # # create a django response object and specify content_type as pdf
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'filename="bill.pdf"'
    # # find the template and render it
    # template = get_template(template_path)
    # html = template.render(context)

    # # create a pdf
    # pisa_status = pisa.CreatePDF(html, dest=response)

    # # if error
    # if pisa_status.err:
    #     return HttpResponse('we had some errors')
    return HttpResponse(result.getvalue(), content_type='application/pdf')


def download_bill_pdf(request):
    context = {}
    bid = request.GET['bid']
    billing = Billing.objects.get(user_id=bid)
    context['billing'] = billing
    pdf = render_pdf_view('pdf_view.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


class BillingView(CreateView):
    template_name = 'billing.html'
    model = Billing
    fields = '__all__'

    def get(self, request):
        bid = request.GET['bid']
        request.session['bid'] = bid
        return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bid = self.request.session.get('bid')
        patientAppointmentDetails = Appointment.objects.get(id=bid)
        context.update({'appointment': patientAppointmentDetails})
        userid = patientAppointmentDetails.user_id
        dataP = Patient.objects.get(user_id=userid)
        context.update({'data': dataP})

        return context

    def post(self, request):
        user_id = request.session.get('bid')
        billNo = request.POST['billNo']
        name = request.POST['name']
        contactno = request.POST['contactno']
        location = request.POST['location']
        doa = request.POST['doa']
        consultationFee = request.POST['consultationFee']
        docFee = request.POST['docFee']
        miscCharge = request.POST['miscCharge']
        # total = consultationFee+docFee+miscCharge
        total = request.POST['total']
        new_bill = Billing.objects.create(
            user_id = user_id,
            billNo = billNo, 
            name = name, 
            contactno = contactno, 
            location = location, 
            doa = doa, 
            consultationFee = consultationFee,
            docFee = docFee, 
            miscCharge = miscCharge, 
            total = total
        )
        new_bill.save()
        patient_id = Appointment.objects.get(id=request.session.get('bid'))
        patient_id.bill_generated = True   
        patient_id.save()     
        return HttpResponseRedirect('doctorstatus.html')



def patientprofile(request):
    context = {}
    check = Patient.objects.filter(user__id=request.user.id)
    if len(check) > 0:
        dataP = Patient.objects.get(user__id=request.user.id)
        dataA = Appointment.objects.filter(id=request.user.id)
        context["data"] = dataP
        context["appointment"] = dataA

    if request.method == "POST":
        # type = request.POST["type"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        # email = request.POST["email"]
        # contactno = request.POST["contactno"]
        phone_number = request.POST.get("contactno")
        # print(phone_number)
        location = request.POST["location"]
        # address = request.POST["address"]

        usr = User.objects.get(id=request.user.id)
        usr.first_name = fname
        usr.last_name = lname
        usr.save()

        dataP.location = location
        dataP.phone_number = phone_number
        dataP.save()

        dataA = Appointment.objects.filter(user__id=request.user.id)
        # dataA.type = type
        # dataA.email = email
        dataA.contactno = phone_number
        # dataA.address = address
        for object in dataA:
            object.save()

        context["status"] = "Changes saved successfully!"
    return render(request, 'patientprofile.html', context)

def doctorprofile(request):
    context = {}
    check = Doctor.objects.filter(user__id=request.user.id)
    if len(check) > 0:
        dataP = Doctor.objects.get(user__id=request.user.id)
        context["data"] = dataP

    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        phone_number = request.POST.get("contactno")
        # print(phone_number)
        speciality = request.POST["speciality"]

        usr = User.objects.get(id=request.user.id)
        usr.first_name = fname
        usr.last_name = lname
        usr.save()

        dataP.speciality = speciality
        dataP.phone_number = phone_number
        dataP.save()

        context["status"] = "Changes saved successfully!"
    return render(request, 'doctorprofile.html', context)


def mcq_test(request):
    exam = MCQTest.objects.all()
    context = {'exam': exam}
    if request.method == 'POST':
        # count = 0
        # for i in exam:
        #     selected_answer = request.POST.get(f'selectedAnswer_i.id')
        #     print(selected_answer)
        #     if selected_answer == i.answer:
        #         count = count+1

        # if(count<4):
        #     print(count, 'less than 4')
        # else:
        #     print(count, 'greater than 4')
        count = 0
        answer1 = request.POST.get('answer1')
        # print(answer1)
        test = MCQTest.objects.get(id=1)
        # print(test.answer)
        if answer1 == test.answer:
            count=count+1
            # print(count)
        answer2 = request.POST.get('answer2')
        # print(answer2)
        test = MCQTest.objects.get(id=2)
        # print(test.answer)
        if answer2 == test.answer:
            count=count+1
            # print(count)
        answer3 = request.POST.get('answer3')
        # print(answer3)
        test = MCQTest.objects.get(id=3)
        # print(test.answer)
        if answer3 == test.answer:
            count=count+1
            # print(count)
        answer4 = request.POST.get('answer4')
        # print(answer4)
        test = MCQTest.objects.get(id=4)
        # print(test.answer)
        if answer4 == test.answer:
            count=count+1
            # print(count)
        answer5 = request.POST.get('answer5')
        # print(answer5)
        test = MCQTest.objects.get(id=5)
        # print(test.answer)
        if answer5 == test.answer:
            count=count+1
            # print(count)
        answer6 = request.POST.get('answer6')
        # print(answer6)
        test = MCQTest.objects.get(id=6)
        # print(test.answer)
        if answer6 == test.answer:
            count=count+1
            # print(count)

        # if answer1 == exam.answer:
        #     count = count+1
        #     print(count)

        context = {'count': count}

    return render(request, 'mcq_test.html', context)


import random
# from captcha.fields import CaptchaField

# str_num = 0

def login_homepage(request):
    num = random.randrange(1000, 9999)
    # global str_num
    # str_num = str(num)
    request.session['str_num'] = str(num)
    print('inside login_homepage')
    return render(request, 'login.html', {"captcha": str(num)})

def login_view(request):
    print('inside login_view')
    context = {}
    context['captcha'] = request.session.get('str_num')
    disp = context['captcha']
    print(request.session.get('str_num'))
    print(disp)
    if request.method == 'POST':
        captcha = request.POST.get('captcha')
        str_num = request.session.get('str_num')
        # print(str_num)
        # print(captcha)
        form = AuthenticationForm(data=request.POST)
        # captchaForm = MyForm(request.POST)
        # print(captchaForm)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # print(str_num)
            # print(captcha)
            # if str_num == str(captcha):
            #     pass
            # clientKey = request.POST['g-recaptcha-response']
            # print(clientKey)
            # clientKey = form.cleaned_data.get('g-recaptcha-response')
            # secretKey = '6LcsIvUhAAAAAGr6lwVscIiRFe2pivkQT79gkL6L'

            # captchaData = {
                # 'secret': secretKey,
                # 'response': clientKey
            # }

            # r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchaData)
            # response = json.loads(r.text)
            # verify = response['success']
            # print('Your success is: ', verify)
            # if str_num == str(captcha):
            if str_num == str(captcha):
                print('Recaptcha Success')
                user = authenticate(username=username, password=password)
                if user is not None and user.is_doctor:
                    login(request, user)
                    return redirect('index.html')
                elif user is not None and user.is_patient:
                    login(request, user)
                    return redirect('patienthome.html')
            else:
                print('Recaptcha Failure')
                messages.error(request,
                               "Enter the captcha Correctly!")
            # print(user.is_doctor)
        
        else:
            messages.error(request,
                           "Invalid User Credentials. Please try again!")
    # captchaForm = MyForm()
    # context['captcha'] = captchaForm
    context['form'] = AuthenticationForm()
    return render(request, 'login.html', context)


class patient_register(CreateView):
    model: User
    form_class = PatientRegisterForm
    template_name = '../templates/patient_register.html'
    context_object_name = 'form'

    def form_valid(self, form):  
        # clientKey = self.request.POST['g-recaptcha-response']
        # secretKey = '6LcsIvUhAAAAAGr6lwVscIiRFe2pivkQT79gkL6L'

        # captchaData = {
        #     'secret': secretKey,
        #     'response': clientKey
        # }

        # r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        # response = json.loads(r.text)
        # verify = response['success']
        # print('Your success is: ', verify)
        # if verify:
        # print('Recaptcha Success')
        user = form.save()
        login(self.request, user)
                    # return redirect('/')
        # else:
        # print('Recaptcha failure')
        # messages.error(self.request, "Form is not valid. Fill the captcha correctly")
        messages.success(self.request,'You are Registered Successfully! Please Log-In to continue.')
        return redirect('/')


class doctor_register(CreateView):
    model: User
    form_class = DoctorRegisterForm
    template_name = '../templates/doctor_register.html'

    def form_valid(self, form):

        # clientKey = self.request.POST['g-recaptcha-response']
        # secretKey = '6LcsIvUhAAAAAGr6lwVscIiRFe2pivkQT79gkL6L'

        # captchaData = {
            # 'secret': secretKey,
            # 'response': clientKey
        # }

        # r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        # response = json.loads(r.text)
        # verify = response['success']
        # print('Your success is: ', verify)
        # if verify:
        # print('Recaptcha Success')
        user = form.save()
        login(self.request, user)
            # return redirect('/')
        # else:
            # print('Recaptcha failure')
        messages.success(self.request, "You are Registered Successfully! Please Log-In to continue.")

        return redirect('/')


def logout(request):
    auth.logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('/')


class AppointmentTemplateView(TemplateView):
    template_name = 'appointment.html'
    model: User

    def post(self, request):
        # username = request.POST['username']
        user_id = request.user.id
        type = request.POST['type']
        contactno = request.POST['contactno']
        email = request.POST['email']
        address = request.POST['address']
        date = request.POST['date']
        time = request.POST['time']
        services = request.POST['services']

        new_appointment = Appointment.objects.create(
            # username = username,
            user_id=user_id,
            type=type,
            contactno=contactno,
            email=email,
            address=address,
            date=date,
            time=time,
            services=services,
        )

        new_appointment.save()
        messages.add_message(
            request, messages.SUCCESS,
            f"Thanks for making an appointment. We'll contact you as soon as possible."
        )

        return HttpResponseRedirect(request.path)

    # def get_user(request):
    #     current_user = request.get.user
    #     return current_user

    def get_id(request, appointment_id):
        return models.User.id

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['appoint'] = Appointment.objects.filter(accepted = 1)
    #     return context

    def get(self, request, *args, **kwargs):
        appointment = Appointment.objects.filter(user_id=request.user)
        context = {'appoint': appointment}
        return render(request, 'appointment.html', context=context)


class ManageAppointmentsTemplateView(ListView):
    template_name = 'manage_appointments.html'
    model = Appointment
    conext_object_name = 'appointments'
    login_required = True

    # paginate_by = 3

    def post(self, request):
        date = request.POST.get('datetime')
        appointment_id = request.POST.get('appointment-id')
        appointment = Appointment.objects.get(id=appointment_id)
        # print(appointment_id)
        # print(appointment)
        appointment.accepted = True
        appointment.accepted_date = datetime.datetime.now()
        # for appointments in appointment:
        appointment.save()

        # messages.add_message(request, messages.SUCCESS, f"You accepted the appointment of {appointments.user.first_name} on {date}")
        AppointmentTemplateView.get_id(request, appointment_id)
        return HttpResponseRedirect(request.path)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        appointments = Appointment.objects.all()
        context.update({
            'appointments': appointments,
            'title': 'Manage Appointments'
        })
        return context


class PatientStatus(CreateView):
    model = Appointment
    template_name = 'patientstatus.html'
    context_object_name = 'appointments'
    fields = '__all__'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        appointments = Appointment.objects.filter(user__id=request.user.id)
        context.update({'appointments': appointments})
        return context

    def get(self, request, *args, **kwargs):
        appointment = Appointment.objects.filter(user_id=request.user)
        context = {'appointments': appointment}
        return render(request, 'patientstatus.html', context=context)


class DoctorStatus(CreateView):
    model = Appointment
    template_name = 'doctorstatus.html'
    context_object_name = 'appointments'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointments = Appointment.objects.all()
        context.update({'appointments': appointments})
        return context

    def post(self, request):
        appointment_id = request.POST.get('appointment-id')
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.checkupstatus = True
        appointment.save()
        return super().post(request)


class DoctorSummary(CreateView):
    template_name = 'doctor_summary.html'
    model = Doctor_Summary
    fields = '__all__'

    def get(self, request):
        userid = request.GET['uid']
        request.session['userid'] = userid
        return super().get(request)

    def post(self, request):
        user_id = request.session.get('userid')
        illness = request.POST['illness']
        medication = request.POST['medication']
        dosage = request.POST['dosage']
        vaccination = request.POST['vaccination']
        note = request.POST['note']

        new_summary = Doctor_Summary.objects.create(
            user_id=user_id,
            illness=illness,
            medication=medication,
            dosage=dosage,
            vaccination=vaccination,
            note=note,
        )
        new_summary.save()
        messages.success(request, "Summary Sent Successfully!")
        return HttpResponseRedirect('doctorstatus.html',
                                    f"{request.POST.get('uid')}")


def patientDoctorSummaryView(request):
    appointment = Appointment.objects.all()
    context = {'appointments': appointment}
    
    userid = request.GET['uid']
    # print(userid)

    patientSummary = Doctor_Summary.objects.filter(user_id = userid)
    context = {'patient':patientSummary}
    return render(request, 'patientDoctorSummary.html', context=context)


# no longer in use
def ipreg(request):
    if request.method == 'POST':
        patientID = request.POST['patientID']
        name = request.POST['name']
        age = request.POST['age']
        address = request.POST['address']
        contactNo = request.POST['contactNo']
        regDate = request.POST['regDate']
        roomNo = request.POST['roomNo']
        gender = request.POST['gender']

        new_ipreg = Ipreg(patientID=patientID,
                          name=name,
                          age=age,
                          address=address,
                          contactNo=contactNo,
                          regDate=regDate,
                          roomNo=roomNo,
                          gender=gender)
        new_ipreg.save()

    return render(request, 'ipreg.html', {})


def opreg(request):
    if request.method == 'POST':
        patientID = request.POST['patientID']
        name = request.POST['name']
        age = request.POST['age']
        contactNo = request.POST['contactNo']
        date = request.POST['date']
        department = request.POST['department']
        docName = request.POST['docName']
        gender = request.POST['gender']

        new_opreg = Opreg(patientID=patientID,
                          name=name,
                          age=age,
                          contactNo=contactNo,
                          date=date,
                          department=department,
                          docName=docName,
                          gender=gender)
        new_opreg.save()

    return render(request, 'opreg.html', {})


def docinfo(request):
    if request.method == 'POST':
        docID = request.POST['docID']
        docname = request.POST['docname']
        age = request.POST['age']
        contactNo = request.POST['contactNo']
        department = request.POST['department']
        gender = request.POST['gender']

        new_docinfo = Docinfo(docID=docID,
                              docname=docname,
                              age=age,
                              contactNo=contactNo,
                              department=department,
                              gender=gender)
        new_docinfo.save()

    return render(request, 'docinfo.html', {})


def roominfo(request):
    if request.method == 'POST':
        roomNo = request.POST['roomNo']
        roomType = request.POST['roomType']

        new_roominfo = Roominfo(roomNo=roomNo, roomType=roomType)
        new_roominfo.save()

    return render(request, 'roominfo.html')


def ipbilling(request):
    if request.method == 'POST':
        billNo = request.POST['billNo']
        patientID = request.POST['patientID']
        name = request.POST['name']
        age = request.POST['age']
        doa = request.POST['doa']
        dod = request.POST['dod']
        gender = request.POST['gender']
        roomCharge = request.POST['roomCharge']
        docFees = request.POST['docFees']

        new_ipbilling = Ipbilling(billNo=billNo,
                                  patientID=patientID,
                                  name=name,
                                  age=age,
                                  doa=doa,
                                  dod=dod,
                                  gender=gender,
                                  roomCharge=roomCharge,
                                  docFees=docFees)
        new_ipbilling.save()

    return render(request, 'ipbilling.html', {})


def opbilling(request):
    if request.method == 'POST':
        billNo = request.POST['billNo']
        patientID = request.POST['patientID']
        name = request.POST['name']
        date = request.POST['date']
        docname = request.POST['docname']
        coamt = request.POST['coamt']
        totalamt = request.POST['totalamt']

        new_opbilling = Opbilling(billNo=billNo,
                                  patientID=patientID,
                                  name=name,
                                  date=date,
                                  docname=docname,
                                  coamt=coamt,
                                  totalamt=totalamt)
        new_opbilling.save()

    return render(request, 'opbilling.html', {})


def searchip(request):
    if request.method == 'POST':
        searchip = request.POST['searchip']
        searchip_results = Ipreg.objects.filter(name__icontains=searchip)
        return redirect(request, 'searchip_results.html', {
            'searchip': searchip,
            'searchip_results': searchip_results
        })
    else:
        return render(request, 'searchip.html', {})


def searchip_results(request):
    searchip = request.POST['searchip']
    searchip_results = Ipreg.objects.filter(name__icontains=searchip)
    return render(request, 'searchip_results.html', {
        'searchip': searchip,
        'searchip_results': searchip_results
    })


def searchop(request):
    if request.method == 'POST':
        searchop = request.POST['searchop']
        # searchop_results = Opreg.objects.filter(name__icontains = searchop)
        return redirect('searchop_results.html')
    else:
        return render(request, 'searchop.html', {})


def searchop_results(request):
    searchop = request.POST['searchop']
    searchop_results = Opreg.objects.filter(name__icontains=searchop)
    return render(request, 'searchop_results.html', {
        'searchop': searchop,
        'searchop_results': searchop_results
    })


def pathology(request):
    if request.method == 'POST':
        patientID = request.POST['patientID']
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST['gender']
        testname = request.POST['testname']
        description = request.POST['description']

        new_pathology = Pathology(patientID=patientID,
                                  name=name,
                                  age=age,
                                  gender=gender,
                                  testname=testname,
                                  description=description)
        new_pathology.save()

    return render(request, 'pathology.html', {})


def patienthome(request):
    # appointment = Appointment.objects.all()
    # appoint = Appointment.objects
    # if Appointment.accepted == True:
    #     messages.add_message(request, messages.SUCCESS, f"Your appointment has been accepted on {appointment.user.accepted_date}")
    # else:
    #     print("Not found")
    return render(request, 'patienthome.html')


# def patientstatus(request):
#     return render(request, 'patientstatus.html')
