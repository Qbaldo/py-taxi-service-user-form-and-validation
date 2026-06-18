import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset
from .models import Driver, Car


def validate_license_number(license_number):
    if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
        raise ValidationError("License must be 3 uppercase letters + 5 digits")


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(validators=[validate_license_number])

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",
                                                 "first_name",
                                                 "last_name")


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(validators=[validate_license_number])

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "",
                "model",
                "manufacturer",
                "drivers"
            )
        )
        self.fields["drivers"].widget.attrs["class"] = "checkbox"

    class Meta:
        model = Car
        fields = "__all__"
