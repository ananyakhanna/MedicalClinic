from unicodedata import name
from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name="home"),
    path('index.html', views.index, name='index'),
    path('ipreg.html', views.ipreg, name='ipreg'),
    path('opreg.html', views.opreg, name='opreg'),
    path('docinfo.html', views.docinfo, name='docinfo'),
    path('roominfo.html', views.roominfo, name='roominfo'),
    path('ipbilling.html', views.ipbilling, name='ipbilling'),
    path('opbilling.html', views.opbilling, name='opbilling'),
    path('searchip.html', views.searchip, name='searchip'),
    path('searchip_results.html', views.searchip_results, name='searchip_results'),
    path('searchop.html', views.searchop, name='searchop'),
    path('searchop_results.html', views.searchop_results, name='searchop_results'),
    path('pathology.html', views.pathology, name='pathology'),
    path('login/', views.login_homepage, name='login_homepage'),
    path('login.html', views.login_view, name='login_view'),
    path('logout', views.logout, name='logout'),
    path('patient_register.html', views.patient_register.as_view(), name='patient_register'),
    path('doctor_register.html', views.doctor_register.as_view(), name='doctor_register'),
    path('register.html', views.register, name='register'),
    path('patienthome.html', views.patienthome, name='patienthome'),
    path('appointment.html', views.AppointmentTemplateView.as_view(), name='appointment'),
    path('manage_appointments.html', views.ManageAppointmentsTemplateView.as_view(), name='manage_appointments'),
    path('patientstatus.html', views.PatientStatus.as_view(), name='patientstatus'),
    path('doctorstatus.html', views.DoctorStatus.as_view(), name='doctorstatus'),
    path('doctor_summary.html', views.DoctorSummary.as_view(), name='doctor_summary'),
    path('patientprofile.html', views.patientprofile, name='patientprofile'),
    path('patientDoctorSummary.html', views.patientDoctorSummaryView, name='patientDoctorSummary'),
    path('doctorprofile.html', views.doctorprofile, name='doctorprofile'),
    path('mcq_test.html', views.mcq_test, name='mcq_test'),
    path('billing.html', views.BillingView.as_view(), name='billing'),
    path('download_bill_pdf', views.download_bill_pdf, name='download_bill_pdf'),
    path('search_patient.html', views.search_patient, name='search_patient'),

    # path('symptoms.html',)
]
    # path('post/<str:pk>', views.post, name='post')