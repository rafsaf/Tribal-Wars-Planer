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

from django.http import HttpRequest
from django.utils import translation

from base.tests.test_utils.mini_setup import MiniSetup


class OverviewTest(MiniSetup):
    def setUp(self):
        self.request = HttpRequest()
        self.request.META["SERVER_NAME"] = "localhost"
        self.request.META["SERVER_PORT"] = 80
        super().setUp()
        translation.activate("pl")

    def test_extend_with_encodeURIComponent(self):
        outline = self.get_outline(add_result=True)
        outline.title_message = "t1\nt2\r[#/]!@]"
        outline.text_message = "t1\nt2\r[#/]!@a;poasd1!\n\t\nbffdb[b]XD[/b]"
        outline.save()

        player = "=hated guy="
        token = "token"
        extended = "[size=12][/size]1. [color=#00a500][b]Wyślij fejk szlachcic[/b][/color] (1 szlachcic) z wioski 138|138 na 215|215\n[b]2021-02-20 [color=#ff0000]15:28:42 - 15:28:42[/color][/b]\n[url=https://plTest.plemiona.pl/game.php?village=38&screen=place&target=65]Wyślij fejk[/url]"
        deputy = "1. [color=#00a500][b]Wyślij fejk szlachcic[/b][/color] (1 szlachcic) z wioski 138|138 na 215|215\n[b]2021-02-20 [color=#ff0000]15:28:42 - 15:28:42[/color][/b]\n[url=https://plTest.plemiona.pl/game.php?village=38&screen=place&target=65&t=3]Wyślij fejk[/url]"
        string = "1. [color=#00a500][b]Wyślij fejk szlachcic[/b][/color] (1 szlachcic)\n[b]2021-02-20 [color=#ff0000]15:28:42 - 15:28:42[/color][/b]\n[url=https://plTest.plemiona.pl/game.php?village=38&screen=place&target=65]Wyślij fejk[/url]"

        overview = self.create_overview(
            outline=outline,
            player=player,
            token=token,
            extended=extended,
            deputy=deputy,
            string=string,
        )

        assert getattr(overview, "to", None) is None
        assert getattr(overview, "message", None) is None

        outline.sending_option = "default"
        outline.save()
        outline.refresh_from_db()
        overview.extend_with_encodeURIComponent(outline, self.request)

        assert getattr(overview, "to", None) == "%3Dhated%20guy%3D"
        print(getattr(overview, "message", None))
        assert (
            getattr(overview, "message", None)
            == "%5Bb%5D%3Dhated%20guy%3D%5B%2Fb%5D%0A%0AUnikalny%20link%20do%20Twoich%20cel%C3%B3w%20na%20plemiona-planer.pl%0A%5Burl%5Dhttp%3A%2F%2Flocalhost%2Fpl%2Foverview%2Ftoken%5B%2Furl%5D%0A%0At1%0At2%0D%5B%23%2F%5D!%40a%3Bpoasd1!%0A%09%0Abffdb%5Bb%5DXD%5B%2Fb%5D"
        )

        outline.sending_option = "string"
        outline.save()
        outline.refresh_from_db()
        overview.extend_with_encodeURIComponent(outline, self.request)

        assert getattr(overview, "to", None) == "%3Dhated%20guy%3D"
        print(getattr(overview, "message", None))
        assert (
            getattr(overview, "message", None)
            == "%5Bb%5D%3Dhated%20guy%3D%5B%2Fb%5D%0A%0AUnikalny%20link%20do%20Twoich%20cel%C3%B3w%20na%20plemiona-planer.pl%0A%5Burl%5Dhttp%3A%2F%2Flocalhost%2Fpl%2Foverview%2Ftoken%5B%2Furl%5D%0A%0At1%0At2%0D%5B%23%2F%5D!%40a%3Bpoasd1!%0A%09%0Abffdb%5Bb%5DXD%5B%2Fb%5D1.%20%5Bcolor%3D%2300a500%5D%5Bb%5DWy%C5%9Blij%20fejk%20szlachcic%5B%2Fb%5D%5B%2Fcolor%5D%20(1%20szlachcic)%0A%5Bb%5D2021-02-20%20%5Bcolor%3D%23ff0000%5D15%3A28%3A42%20-%2015%3A28%3A42%5B%2Fcolor%5D%5B%2Fb%5D%0A%5Burl%3Dhttps%3A%2F%2FplTest.plemiona.pl%2Fgame.php%3Fvillage%3D38%26screen%3Dplace%26target%3D65%5DWy%C5%9Blij%20fejk%5B%2Furl%5D"
        )

        outline.sending_option = "extended"
        outline.save()
        outline.refresh_from_db()
        overview.extend_with_encodeURIComponent(outline, self.request)

        assert getattr(overview, "to", None) == "%3Dhated%20guy%3D"
        print(getattr(overview, "message", None))
        assert (
            getattr(overview, "message", None)
            == "%5Bb%5D%3Dhated%20guy%3D%5B%2Fb%5D%0A%0AUnikalny%20link%20do%20Twoich%20cel%C3%B3w%20na%20plemiona-planer.pl%0A%5Burl%5Dhttp%3A%2F%2Flocalhost%2Fpl%2Foverview%2Ftoken%5B%2Furl%5D%0A%0At1%0At2%0D%5B%23%2F%5D!%40a%3Bpoasd1!%0A%09%0Abffdb%5Bb%5DXD%5B%2Fb%5D1.%20%5Bcolor%3D%2300a500%5D%5Bb%5DWy%C5%9Blij%20fejk%20szlachcic%5B%2Fb%5D%5B%2Fcolor%5D%20(1%20szlachcic)%20z%20wioski%20138%7C138%20na%20215%7C215%0A%5Bb%5D2021-02-20%20%5Bcolor%3D%23ff0000%5D15%3A28%3A42%20-%2015%3A28%3A42%5B%2Fcolor%5D%5B%2Fb%5D%0A%5Burl%3Dhttps%3A%2F%2FplTest.plemiona.pl%2Fgame.php%3Fvillage%3D38%26screen%3Dplace%26target%3D65%5DWy%C5%9Blij%20fejk%5B%2Furl%5D"
        )

        outline.sending_option = "deputy"
        outline.save()
        outline.refresh_from_db()
        overview.extend_with_encodeURIComponent(outline, self.request)

        assert getattr(overview, "to", None) == "%3Dhated%20guy%3D"
        print(getattr(overview, "message", None))
        assert (
            getattr(overview, "message", None)
            == "%5Bb%5D%3Dhated%20guy%3D%5B%2Fb%5D%0A%0AUnikalny%20link%20do%20Twoich%20cel%C3%B3w%20na%20plemiona-planer.pl%0A%5Burl%5Dhttp%3A%2F%2Flocalhost%2Fpl%2Foverview%2Ftoken%5B%2Furl%5D%0A%0At1%0At2%0D%5B%23%2F%5D!%40a%3Bpoasd1!%0A%09%0Abffdb%5Bb%5DXD%5B%2Fb%5D1.%20%5Bcolor%3D%2300a500%5D%5Bb%5DWy%C5%9Blij%20fejk%20szlachcic%5B%2Fb%5D%5B%2Fcolor%5D%20(1%20szlachcic)%20z%20wioski%20138%7C138%20na%20215%7C215%0A%5Bb%5D2021-02-20%20%5Bcolor%3D%23ff0000%5D15%3A28%3A42%20-%2015%3A28%3A42%5B%2Fcolor%5D%5B%2Fb%5D%0A%5Burl%3Dhttps%3A%2F%2FplTest.plemiona.pl%2Fgame.php%3Fvillage%3D38%26screen%3Dplace%26target%3D65%26t%3D3%5DWy%C5%9Blij%20fejk%5B%2Furl%5D"
        )
