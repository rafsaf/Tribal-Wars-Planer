from django.conf import settings


def build_tag(request):
    return {"BUILD_TAG": settings.BUILD_TAG}
