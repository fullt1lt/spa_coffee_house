from django.contrib import admin
from .models import CafeProduct, Composition, MassageTherapist, Position, Review, Salon, SpaUser, TypeCafeProduct, TypeCategories, SpaСategories, CategoriesSession

admin.site.register(SpaUser)
admin.site.register(Salon)
admin.site.register(MassageTherapist)
admin.site.register(SpaСategories)
admin.site.register(TypeCategories)
admin.site.register(Composition)
admin.site.register(Review)
admin.site.register(Position)
admin.site.register(CategoriesSession)
admin.site.register(CafeProduct)
admin.site.register(TypeCafeProduct)
