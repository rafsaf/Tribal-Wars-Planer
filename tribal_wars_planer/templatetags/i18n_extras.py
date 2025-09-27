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
