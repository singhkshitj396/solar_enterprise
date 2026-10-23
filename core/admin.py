from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Appointment, Branch, StaffProfile

User = get_user_model()
admin.site.unregister(User)


class StaffProfileInline(admin.StackedInline):
    model = StaffProfile
    extra = 0
    can_delete = True


@admin.register(User)
class BranchStaffUserAdmin(UserAdmin):
    inlines = (StaffProfileInline,)
    list_display = ("username", "email", "first_name", "last_name", "is_staff")


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "phone", "is_active")
    list_filter = ("is_active", "city")
    search_fields = ("name", "city", "address")
    ordering = ("city", "name")


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "branch", "job_title")
    list_filter = ("branch",)
    search_fields = ("user__username", "user__first_name", "user__last_name")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "customer_name",
        "city",
        "phone",
        "preferred_visit",
        "branch",
        "status",
    )
    list_filter = ("status", "system_type", "branch", "preferred_visit")
    search_fields = ("customer_name", "phone", "email", "city", "address")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "preferred_visit"
    ordering = ("preferred_visit",)
