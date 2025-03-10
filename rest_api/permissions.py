# Copyright 2021 Rafał Safin (rafsaf). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

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
