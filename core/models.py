from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    address = models.CharField(max_length=250, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("city", "name")
        verbose_name_plural = "branches"

    def __str__(self):
        return f"{self.name} · {self.city}"


class StaffProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_profile",
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name="staff_profiles",
    )
    job_title = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ("branch__city", "user__last_name", "user__username")

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} · {self.branch}"


class Appointment(models.Model):
    class SystemType(models.TextChoices):
        ON_GRID = "on_grid", "On-Grid"
        OFF_GRID = "off_grid", "Off-Grid"
        HYBRID = "hybrid", "Hybrid"
        NOT_SURE = "not_sure", "Not sure yet"

    class Status(models.TextChoices):
        NEW = "new", "New request"
        CONFIRMED = "confirmed", "Confirmed"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    phone_validator = RegexValidator(
        regex=r"^\+?[\d\s().-]{8,18}$",
        message="Enter a valid phone number.",
    )

    customer_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20, validators=[phone_validator])
    email = models.EmailField()
    city = models.CharField(max_length=120)
    address = models.CharField(max_length=250)
    capacity = models.CharField(max_length=40, blank=True)
    system_type = models.CharField(
        max_length=20,
        choices=SystemType.choices,
        default=SystemType.NOT_SURE,
    )
    preferred_visit = models.DateTimeField()
    message = models.TextField(blank=True)
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        related_name="appointments",
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("preferred_visit", "created_at")
        indexes = [
            models.Index(fields=("status", "preferred_visit")),
            models.Index(fields=("branch", "preferred_visit")),
        ]

    def __str__(self):
        return f"{self.customer_name} · {self.preferred_visit:%d %b %Y %H:%M}"
