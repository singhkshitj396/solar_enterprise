from django import forms
from django.utils import timezone

from .models import Appointment


class AppointmentForm(forms.ModelForm):
    preferred_visit = forms.DateTimeField(
        input_formats=("%Y-%m-%dT%H:%M",),
        widget=forms.DateTimeInput(
            format="%Y-%m-%dT%H:%M",
            attrs={"type": "datetime-local"},
        ),
    )

    class Meta:
        model = Appointment
        fields = (
            "customer_name",
            "phone",
            "email",
            "city",
            "address",
            "capacity",
            "system_type",
            "preferred_visit",
            "message",
        )
        widgets = {
            "customer_name": forms.TextInput(
                attrs={"autocomplete": "name", "placeholder": "Your full name"}
            ),
            "phone": forms.TelInput(
                attrs={"autocomplete": "tel", "placeholder": "+91 00000 00000"}
            ),
            "email": forms.EmailInput(
                attrs={"autocomplete": "email", "placeholder": "you@example.com"}
            ),
            "city": forms.TextInput(
                attrs={"autocomplete": "address-level2", "placeholder": "Your city"}
            ),
            "address": forms.TextInput(
                attrs={
                    "autocomplete": "street-address",
                    "placeholder": "House / street / landmark",
                }
            ),
            "capacity": forms.Select(
                choices=[
                    ("", "Select if you know"),
                    ("1–3 kW", "1–3 kW"),
                    ("3–5 kW", "3–5 kW"),
                    ("5–10 kW", "5–10 kW"),
                    ("10–25 kW", "10–25 kW"),
                    ("25+ kW", "25+ kW"),
                    ("Not sure", "Not sure"),
                ]
            ),
            "system_type": forms.Select(),
            "message": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Tell us about your property or energy needs",
                }
            ),
        }
        labels = {
            "customer_name": "Full name",
            "phone": "Mobile number",
            "email": "Email address",
            "city": "City",
            "address": "Visit address",
            "capacity": "Required solar capacity",
            "system_type": "Solar system",
            "preferred_visit": "Preferred visit date and time",
            "message": "Message (optional)",
        }

    def clean_preferred_visit(self):
        visit = self.cleaned_data["preferred_visit"]
        if visit <= timezone.now():
            raise forms.ValidationError("Choose a future date and time for your visit.")
        return visit
