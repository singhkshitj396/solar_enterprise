from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import AppointmentForm
from .models import Appointment, Branch


def home(request):
    form = AppointmentForm()
    return render(request, "core/home.html", {"form": form})


def book_appointment(request):
    if request.method != "POST":
        return redirect("home")

    form = AppointmentForm(request.POST)
    if form.is_valid():
        appointment = form.save(commit=False)
        appointment.branch = Branch.objects.filter(
            is_active=True,
            city__iexact=appointment.city,
        ).first()
        appointment.save()
        messages.success(
            request,
            "Your visit request is in. Our team will contact you to confirm the details.",
        )
        return redirect(f"{reverse('home')}?submitted=1#contact")

    return render(
        request,
        "core/home.html",
        {"form": form, "show_form_errors": True},
        status=422,
    )


class StaffLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True


class StaffLogoutView(LogoutView):
    http_method_names = ["post", "options"]


@login_required
def staff_appointments(request):
    if not request.user.is_staff:
        raise PermissionDenied("Staff access is required.")

    appointments = Appointment.objects.select_related("branch")
    if not request.user.is_superuser:
        profile = getattr(request.user, "staff_profile", None)
        appointments = (
            appointments.filter(branch=profile.branch)
            if profile
            else appointments.none()
        )

    return render(
        request,
        "core/staff_appointments.html",
        {"appointments": appointments, "status_choices": Appointment.Status.choices},
    )


@login_required
@require_POST
def update_appointment_status(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied("Staff access is required.")

    appointment = get_object_or_404(Appointment, pk=pk)
    if not request.user.is_superuser:
        profile = getattr(request.user, "staff_profile", None)
        if not profile or appointment.branch_id != profile.branch_id:
            raise PermissionDenied("This appointment belongs to another branch.")

    status = request.POST.get("status")
    valid_statuses = {choice[0] for choice in Appointment.Status.choices}
    if status not in valid_statuses:
        messages.error(request, "Choose a valid appointment status.")
    else:
        appointment.status = status
        appointment.save(update_fields=("status", "updated_at"))
        messages.success(request, "Appointment status updated.")
    return redirect("staff-appointments")
