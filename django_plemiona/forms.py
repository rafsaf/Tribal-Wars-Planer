from django_registration.forms import RegistrationForm
from captcha.fields import ReCaptchaField
from django import forms


class RecaptchaRegistrationForm(RegistrationForm):
    recaptcha = ReCaptchaField(label="")
