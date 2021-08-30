from django.test import TestCase
from utils.basic import encode_component


class TestEncodeComponent(TestCase):
    """Test for basic encode_component"""

    def test_strings_are_encoded_properly_with_js2py(self):
        cases_dict = {
            "test": "test",
            "https://www.w3schools.com/js/tryit.asp?filename=tryjs_editor": "https%3A%2F%2Fwww.w3schools.com%2Fjs%2Ftryit.asp%3Ffilename%3Dtryjs_editor",
            "1. [color=#0e0eff][b]Burzak[/b][/color] (Katapulty-100 [b]Zagroda[/b])": "1.%20%5Bcolor%3D%230e0eff%5D%5Bb%5DBurzak%5B%2Fb%5D%5B%2Fcolor%5D%20(Katapulty-100%20%5Bb%5DZagroda%5B%2Fb%5D)",
            "3. [color=#0e0eff][b]Burzak[/b][/color] (Katapulty-50 [b]Tartak[/b])\n\r\n\t[b]2021-02-20 [color=#ff0000]08:39:12 - 08:39:12[/color][/b]": "3.%20%5Bcolor%3D%230e0eff%5D%5Bb%5DBurzak%5B%2Fb%5D%5B%2Fcolor%5D%20(Katapulty-50%20%5Bb%5DTartak%5B%2Fb%5D)%0A%0D%0A%09%5Bb%5D2021-02-20%20%5Bcolor%3D%23ff0000%5D08%3A39%3A12%20-%2008%3A39%3A12%5B%2Fcolor%5D%5B%2Fb%5D",
        }

        for test_case_name in cases_dict:
            case_after_encoding = encode_component(test_case_name)
            self.assertEqual(cases_dict[test_case_name], case_after_encoding)
