from typing import Callable

from js2py import eval_js

__encode_component_using_javascript: Callable[[str], str] = eval_js(
    "function encode(arg) {return encodeURIComponent(arg);}"
)


def encode_component(string_to_encode: str) -> str:
    return __encode_component_using_javascript(string_to_encode)
