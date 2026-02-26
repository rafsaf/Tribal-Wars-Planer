from django.test import SimpleTestCase

from base import forms


class TestSanitizeTroopsHtml(SimpleTestCase):
    def test_sanitize_troops_html_keeps_only_span_grey(self):
        value = (
            '12<span class="grey">.</span>345'
            '<span class="red">.</span>'
            "</script><script>alert('XSS')</script>"
        )

        sanitized = forms.sanitize_troops_html(value)

        assert '<span class="grey">.</span>' in sanitized
        assert '<span class="red">' not in sanitized
        assert "<script>" not in sanitized
        assert "alert('XSS')" in sanitized
