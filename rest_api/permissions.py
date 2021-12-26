from django.conf import settings
from django.http.request import HttpRequest
from rest_framework import permissions


class StripeWebhookSafeListPermission(permissions.BasePermission):
    """
    Ensure the request's IP address is on the safe list configured in Django settings.
    """

    def has_permission(self, request, view):
        remote_addr: str = request.META["REMOTE_ADDR"]
        for valid_ip in settings.STRIPE_WEBHOOK_SAFE_LIST_IPS:
            if remote_addr == valid_ip or remote_addr.startswith(valid_ip):
                return True

        return False


class MetricsExportSecretPermission(permissions.BasePermission):
    """
    Ensure the request's IP address is on the safe list configured in Django settings.
    """

    def has_permission(self, request: HttpRequest, view):
        if request.GET.get("token") == settings.METRICS_EXPORT_ENDPOINT_SECRET:
            return True

        return False
