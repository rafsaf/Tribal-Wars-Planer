# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from django.conf import settings


def build_tag(request):
    return {"BUILD_TAG": settings.BUILD_TAG, "DEBUG": settings.DEBUG}
