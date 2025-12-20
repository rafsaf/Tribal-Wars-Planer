# Copyright 2025 Rafał Safin (rafsaf). All Rights Reserved.
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

from django import template
from django.utils import translation

register = template.Library()


@register.filter
def lang_path_next(full_path):
    """
    Slices the full path to remove the /<lang_code>/ prefix based on the
    current active language.
    """
    # 1. Get the current active language code (e.g., 'en', 'pt-br')
    lang_code = translation.get_language()

    # 2. Calculate the length of the prefix to remove:
    #    1 (leading slash) + len(lang_code) = prefix_length
    prefix_length = len(lang_code) + 1

    # 3. Slice the path, starting after the language prefix.
    #    E.g., for '/pt-br/page/', prefix_length is 7. We slice from index 7 (the 'p').
    #    If the path is just '/pt-br/', this returns '/'
    return full_path[prefix_length:]
