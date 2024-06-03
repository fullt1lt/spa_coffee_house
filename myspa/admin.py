from django.contrib import admin
from .models import MassageTherapist, Salon, SpaUser

admin.site.register(SpaUser)
admin.site.register(Salon)
admin.site.register(MassageTherapist)
