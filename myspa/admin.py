from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (BlogAndNews, CafeProduct, Gallery, MassageTherapist, Position, Procedure, Record, Review, Salon, Schedule, SpaUser, TypeBlogAndNews, TypeCafeProduct, TypeCategories, TypeGallery, SpaСategories)


@admin.register(SpaUser)
class SpaUserAdmin(UserAdmin):
    model = SpaUser
    list_display = ("email", "first_name", "last_name", "is_staff")
    ordering = ("email",)
    search_fields = ("email", "first_name", "last_name")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "phone", "profile_image")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )

admin.site.register(Salon)
admin.site.register(MassageTherapist)
admin.site.register(SpaСategories)
admin.site.register(TypeCategories)
admin.site.register(Review)
admin.site.register(Position)
admin.site.register(Procedure)
admin.site.register(CafeProduct)
admin.site.register(TypeCafeProduct)
admin.site.register(BlogAndNews)
admin.site.register(TypeBlogAndNews)
admin.site.register(TypeGallery)
admin.site.register(Gallery)
admin.site.register(Schedule)
admin.site.register(Record)
