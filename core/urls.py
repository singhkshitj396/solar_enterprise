from django.urls import path

from .views import (
    StaffLoginView,
    StaffLogoutView,
    book_appointment,
    home,
    staff_appointments,
    update_appointment_status,
)

urlpatterns = [
    path("", home, name="home"),
    path("appointments/book/", book_appointment, name="book-appointment"),
    path("staff/login/", StaffLoginView.as_view(), name="staff-login"),
    path("staff/logout/", StaffLogoutView.as_view(), name="staff-logout"),
    path("staff/appointments/", staff_appointments, name="staff-appointments"),
    path(
        "staff/appointments/<int:pk>/status/",
        update_appointment_status,
        name="update-appointment-status",
    ),
]
