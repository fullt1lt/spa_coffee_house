from django.contrib import admin
from .models import Composition, MassageTherapist, Salon, SpaUser, TypeCategories, SpaСategories

admin.site.register(SpaUser)
admin.site.register(Salon)
admin.site.register(MassageTherapist)
admin.site.register(SpaСategories)
admin.site.register(TypeCategories)
admin.site.register(Composition)
