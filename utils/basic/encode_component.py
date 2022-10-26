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

from collections.abc import Callable

from js2py import eval_js

__encode_component_using_javascript: Callable[[str], str] = eval_js(
    "function encode(arg) {return encodeURIComponent(arg);}"
)


def encode_component(string_to_encode: str) -> str:
    return __encode_component_using_javascript(string_to_encode)
