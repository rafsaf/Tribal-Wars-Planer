import string
import random

from django.test import TestCase


class HomeViewSetup(TestCase):
    def random_lower_string(self, length=20) -> str:
        return "".join(random.choices(string.ascii_lowercase, k=length))
