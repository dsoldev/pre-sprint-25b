from django.contrib import admin
from .models import Questions, Scripts, Patients, Answers

# Register your models here.
admin.site.register(Questions)
admin.site.register(Scripts)
admin.site.register(Patients)
admin.site.register(Answers)