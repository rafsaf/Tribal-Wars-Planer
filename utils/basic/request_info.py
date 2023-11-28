# Copyright 2023 Rafał Safin (rafsaf). All Rights Reserved.
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
from django.http import HttpRequest


def is_android_tw_app_webview(request: HttpRequest):
    requested_with = request.META.get("HTTP_X_REQUESTED_WITH")
    if requested_with is not None:
        if requested_with == settings.TRIBALWARS_ANDROID_APP_NAME:
            return True
    return False
