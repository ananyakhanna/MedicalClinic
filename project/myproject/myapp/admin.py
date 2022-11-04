from django.contrib import admin
from .models import Docinfo, Doctor_Summary, Ipbilling, Ipreg, MCQTest, Opbilling, Opreg, Pathology, Roominfo, User, Patient, Doctor, Appointment
# Register your models here.

# admin.site.register(Feature)
admin.site.register(Ipreg)
admin.site.register(Opreg)
admin.site.register(Docinfo)
admin.site.register(Roominfo)
admin.site.register(Ipbilling)
admin.site.register(Opbilling)
admin.site.register(Pathology)
admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Doctor_Summary)
admin.site.register(MCQTest)


