# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from django.conf import settings
from django.http.request import HttpRequest
from django.utils.crypto import constant_time_compare
from rest_framework import permissions


class MetricsExportSecretPermission(permissions.BasePermission):
    """
    Ensure the request's GET token param equals to secret from settings.
    """

    def has_permission(self, request: HttpRequest, view):
        if constant_time_compare(
            request.GET.get("token") or "", settings.METRICS_EXPORT_ENDPOINT_SECRET
        ):
            return True

        return False
