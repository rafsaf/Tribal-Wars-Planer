from captcha import widgets
from captcha.fields import ReCaptchaField
from django_registration.forms import RegistrationForm


class RecaptchaRegistrationForm(RegistrationForm):
    recaptcha = ReCaptchaField(
        label="",
        widget=widgets.ReCaptchaV2Checkbox(
            api_params={"hl": "en"},
        ),
    )
