from django.conf import settings


def test_testing_is_true():
    assert settings.TESTING
