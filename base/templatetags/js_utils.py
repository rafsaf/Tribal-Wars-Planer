# base/templatetags/js_utils.py
import json

from django import template

register = template.Library()


@register.filter
def js_string(value):
    return json.dumps(value or "")
