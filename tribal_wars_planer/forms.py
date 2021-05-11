from django_registration.forms import RegistrationForm
from captcha.fields import ReCaptchaField
from captcha import widgets


class RecaptchaRegistrationForm(RegistrationForm):
    recaptcha = ReCaptchaField(
        label="",
        widget=widgets.ReCaptchaV2Checkbox(
            api_params={"hl": "en"},
        ),
    )
