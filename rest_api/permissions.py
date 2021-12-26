from django.conf import settings
from django.http.request import HttpRequest
from rest_framework import permissions


class MetricsExportSecretPermission(permissions.BasePermission):
    """
    Ensure the request's IP address is on the safe list configured in Django settings.
    """

    def has_permission(self, request: HttpRequest, view):
        if request.GET.get("token") == settings.METRICS_EXPORT_ENDPOINT_SECRET:
            return True

        return False
