from django.conf import settings
from django.http import HttpRequest


def is_android_tw_app_webview(request: HttpRequest):
    requested_with = request.META.get("HTTP_X_REQUESTED_WITH")
    if requested_with is not None:
        if requested_with == settings.TRIBALWARS_ANDROID_APP_NAME:
            return True
    return False
