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

import datetime
import json
import zoneinfo

from django.test import TestCase
from django.utils.translation import activate

from base.models import Outline, OutlineOverview, Overview, PeriodModel, WeightModel
from base.models import TargetVertex as Target
from base.tests.test_utils.initial_setup import create_initial_data
from utils.outline_finish import MakeFinalOutline, OutdatedData


class TestMakeFinalOutline(TestCase):
    def setUp(self):
        activate("pl")
        create_initial_data()
        self.maxDiff = None
        self.outline: Outline = Outline.objects.get(id=1)
        self.make_final: MakeFinalOutline = MakeFinalOutline(self.outline)

    def test_add_target_error(self):
        coord = "500|499"
        self.make_final._add_target_error(coord)
        expected = {"Cel 500|499 nie istnieje"}
        self.assertEqual(expected, self.make_final.error_messages_set)

    def test_add_village_player_error(self):
        coord = "500|499"
        self.make_final._add_village_error(coord)
        expected = {"Wioska 500|499 nie istnieje"}
        self.assertEqual(expected, self.make_final.error_messages_set)

    def test_add_player_error(self):
        player = "player"
        self.make_final._add_player_error(player)
        expected = {"Gracz player nie istnieje"}
        self.assertEqual(expected, self.make_final.error_messages_set)

    def test_targets_json_format(self):
        target = Target.objects.get(target="500|499")
        self.make_final.targets = Target.objects.filter(target="500|499")

        assert (
            self.make_final.targets_json_format()
            == f'{{"{target.pk}": {{"id": 1, "target": "500|499", "player": "player1", "fake": false, "ruin": false, "village_id": 0, "player_id": 0}}}}'
        )

    def test_ally_id(self):
        self.make_final._calculate_villages_id_dictionary()
        coord1 = "500|500"
        coord2 = "500|501"
        coord3 = "100|100"
        res1 = self.make_final._ally_id(coord1)
        res2 = self.make_final._ally_id(coord2)

        self.assertEqual(res1, "0")
        self.assertEqual(res2, "1")
        with self.assertRaises(OutdatedData):
            self.make_final._ally_id(coord3)
        expected = {"Wioska 100|100 nie istnieje"}
        self.assertEqual(expected, self.make_final.error_messages_set)

    def test_enemy_id(self):
        self.make_final._calculate_villages_id_dictionary()
        coord1 = "500|500"
        coord2 = "500|501"
        coord3 = "100|100"
        res1 = self.make_final._enemy_id(coord1)
        res2 = self.make_final._enemy_id(coord2)

        self.assertEqual(res1, "0")
        self.assertEqual(res2, "1")
        with self.assertRaises(OutdatedData):
            self.make_final._enemy_id(coord3)
        expected = {"Cel 100|100 nie istnieje"}
        self.assertEqual(expected, self.make_final.error_messages_set)

    def test_player_id(self):
        self.make_final._calculate_player_id_dictionary()
        player1 = "player0"
        player2 = "aaa"

        res1 = self.make_final._player_id(player1)
        self.assertEqual(res1, "0")

        with self.assertRaises(OutdatedData):
            self.make_final._player_id(player2)
        expected = {"Gracz aaa nie istnieje"}
        self.assertEqual(expected, self.make_final.error_messages_set)

    def test_calculate_player_id_dictionary(self):
        self.make_final._calculate_player_id_dictionary()
        expected = {"player0": "0"}
        self.assertEqual(expected, self.make_final.player_id_dictionary)

    def test_calculate_village_id_dictionary(self):
        self.make_final._calculate_villages_id_dictionary()
        expected = {
            "500|502": "2",
            "500|501": "1",
            "500|500": "0",
            "500|499": "6",
        }
        self.assertEqual(expected, self.make_final.village_id_dictionary)

    def test_weights_list(self):
        target = Target.objects.get(target="500|499")
        weight1 = WeightModel.objects.get(start="500|500")
        weight2 = WeightModel.objects.get(start="500|501")
        weight3 = WeightModel.objects.get(start="500|502")
        res = list(self.make_final._weights_list(target))
        self.assertEqual([weight1, weight2, weight3], res)

    def test_json_weight(self):
        self.make_final._calculate_period_dictionary()
        target = Target.objects.get(target="500|499")
        weight1 = WeightModel.objects.get(start="500|500")
        time_periods = self.make_final._time_periods(target)
        time_periods.adjust_time([weight1])
        new_weight = time_periods.next(weight1)
        res = self.make_final._json_weight(new_weight, target.village_id)
        expected = {
            "id": 1,
            "start": "500|500",
            "player": "player0",
            "off": 5000,
            "nobleman": 1,
            "catapult": 0,
            "ruin": False,
            "distance": 1.0,
            "time_seconds": 84300,
            "t1": datetime.datetime(2021, 3, 3, 9, 0),
            "t2": datetime.datetime(2021, 3, 3, 10, 0),
            "delivery_t1": datetime.datetime(
                2021, 3, 3, 9, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Warsaw")
            ),
            "delivery_t2": datetime.datetime(
                2021, 3, 3, 10, 0, tzinfo=zoneinfo.ZoneInfo(key="Europe/Warsaw")
            ),
            "shipment_t1": datetime.datetime(
                2021, 3, 3, 8, 25, tzinfo=zoneinfo.ZoneInfo(key="Europe/Warsaw")
            ),
            "shipment_t2": datetime.datetime(
                2021, 3, 3, 9, 25, tzinfo=zoneinfo.ZoneInfo(key="Europe/Warsaw")
            ),
            "village_id": 0,
            "player_id": 0,
            "send_url": "https://te1.testserver/game.php?village=0&screen=place&target=0",
        }
        self.assertEqual(expected, res)

    def test_calculate_period_dict(self):
        self.make_final._calculate_period_dictionary()
        target = Target.objects.get(target="500|499")
        period1 = PeriodModel.objects.get(unit="ram")
        period2 = PeriodModel.objects.get(unit="noble")
        expected = {target: [period1, period2]}
        self.assertEqual(expected, self.make_final.target_period_dict)

    def test_call_main_method_works_as_expected(self):
        outline = Outline.objects.get(id=1)
        error_msg = self.make_final()
        self.assertEqual(error_msg, set())
        outline_overview: OutlineOverview = OutlineOverview.objects.get(outline=outline)
        overview: Overview = Overview.objects.get(outline=outline)
        self.assertEqual(overview.player, "player0")
        table = (
            "\r\n\r\n[table][**][||]WYŚLIJ[||]OFF[||]GRUBE[||]WYSYŁKA[||]WEJŚCIE[||]Z WIOSKI[||]CEL[/**][*]1[|][url=https://te1.testserver/game.php?village=2&screen=place&target=6]Wyślij OFF[/url][|]19000[|]0[|]2021-03-03"
            "\n[b][color=#0e5e5e]05:30:00[/color][/b]-[b][color=#ff0000]07:30:00[/color][/b][|]2021-03-03"
            "\n[b][color=#0e5e5e]07:00:00[/color][/b]-[b][color=#ff0000]09:00:00[/color][/b][|][coord]500|502[/coord][|][coord]500|499[/coord][*]2[|][url=https://te1.testserver/game.php?village=1&screen=place&target=6]Wyślij OFF[/url][|]100[|]0[|]2021-03-03"
            "\n[b][color=#0e5e5e]06:00:00[/color][/b]-[b][color=#ff0000]08:00:00[/color][/b][|]2021-03-03"
            "\n[b][color=#0e5e5e]07:00:00[/color][/b]-[b][color=#ff0000]09:00:00[/color][/b][|][coord]500|501[/coord][|][coord]500|499[/coord][*]3[|][url=https://te1.testserver/game.php?village=0&screen=place&target=6]Wyślij OFF[/url][|]5000[|]1[|]2021-03-03"
            "\n[b][color=#0e5e5e]08:25:00[/color][/b]-[b][color=#ff0000]09:25:00[/color][/b][|]2021-03-03"
            "\n[b][color=#0e5e5e]09:00:00[/color][/b]-[b][color=#ff0000]10:00:00[/color][/b][|][coord]500|500[/coord][|][coord]500|499[/coord][/table]"
        )
        self.assertEqual(overview.table, table)
        extended = (
            "\r\n\r\n1. [size=12][b]OFF[/b][/size] (Off-19000) z wioski 500|502 na 500|499\r\n"
            "[b]2021-03-03 [color=#ff0000]05:30:00 - 07:30:00[/color][/b]\n"
            "[url=https://te1.testserver/game.php?village=2&screen=place&target=6]Wyślij OFF[/url]\r\n"
            "\r\n"
            "2. [size=12][b]OFF[/b][/size] (Off-100) z wioski 500|501 na 500|499\r\n"
            "[b]2021-03-03 [color=#ff0000]06:00:00 - 08:00:00[/color][/b]\n"
            "[url=https://te1.testserver/game.php?village=1&screen=place&target=6]Wyślij OFF[/url]\r\n"
            "\r\n"
            "3. [color=#a500a5][size=12][b]SZLACHCIC[/b][/size][/color] (Off-5000, Szlachcice-1)  z wioski 500|500 na 500|499\r\n"
            "[b]2021-03-03 [color=#ff0000]08:25:00 - 09:25:00[/color][/b]\n"
            "[url=https://te1.testserver/game.php?village=0&screen=place&target=6]Wyślij OFF[/url]\r\n\r\n"
        )

        self.assertEqual(overview.extended, extended)
        new_extended = (
            "\r\n\r\n[b]----------------2021-03-03 (Środa)----------------[/b]\r\n"
            "1. [b][color=#a50000]Wyślij OFF[19000 off][/color] (1 z 1)[/b]\n"
            "\r\n"
            "[b]2021-03-03 [color=#ff0000]05:30:00 - 07:30:00[/color][/b]\n"
            "500|502 [b]->[/b] 500|499\n"
            "[url=https://te1.testserver/game.php?village=2&screen=place&target=6]Wyślij OFF[/url]\r\n"
            "\r\n"
            "2. [b][color=#a50000]Wyślij OFF[100 off][/color] (1 z 1)[/b]\n"
            "\r\n"
            "[b]2021-03-03 [color=#ff0000]06:00:00 - 08:00:00[/color][/b]\n"
            "500|501 [b]->[/b] 500|499\n"
            "[url=https://te1.testserver/game.php?village=1&screen=place&target=6]Wyślij OFF[/url]\r\n"
            "\r\n"
            "3. [b][color=#a500a5]Wyślij SZLACHCIC[5000 off + 1 szlachcic][/color] (1 z 1)[/b]\n"
            "\r\n"
            "[b]2021-03-03 [color=#ff0000]08:25:00 - 09:25:00[/color][/b]\n"
            "500|500 [b]->[/b] 500|499\n"
            "[url=https://te1.testserver/game.php?village=0&screen=place&target=6]Wyślij SZLACHCIC[/url]\r\n\r\n"
        )

        self.assertEqual(overview.new_extended, new_extended)

        string = (
            "\r\n\r\n1. [size=12][b]OFF[/b][/size] (Off-19000)\r\n"
            "[b]2021-03-03 [color=#ff0000]05:30:00 - 07:30:00[/color][/b]\n"
            "[url=https://te1.testserver/game.php?village=2&screen=place&target=6]Wyślij OFF[/url]\r\n"
            "\r\n"
            "2. [size=12][b]OFF[/b][/size] (Off-100)\r\n"
            "[b]2021-03-03 [color=#ff0000]06:00:00 - 08:00:00[/color][/b]\n"
            "[url=https://te1.testserver/game.php?village=1&screen=place&target=6]Wyślij OFF[/url]\r\n"
            "\r\n"
            "3. [color=#a500a5][size=12][b]SZLACHCIC[/b][/size][/color] (Off-5000, Szlachcice-1) \r\n"
            "[b]2021-03-03 [color=#ff0000]08:25:00 - 09:25:00[/color][/b]\n"
            "[url=https://te1.testserver/game.php?village=0&screen=place&target=6]Wyślij OFF[/url]\r\n\r\n"
        )
        self.assertEqual(overview.string, string)

        deputy = (
            "\r\n\r\n[b]----------------2021-03-03 (Środa)----------------[/b]\r\n"
            "1. [b][color=#a50000]Wyślij OFF[19000 off][/color] (1 z 1)[/b]\n"
            "\r\n"
            "[b]2021-03-03 [color=#ff0000]05:30:00 - 07:30:00[/color][/b]\n"
            "500|502 [b]->[/b] 500|499\n"
            "[url=https://te1.testserver/game.php?village=2&screen=place&target=6&t=0]Wyślij OFF[/url]\r\n"
            "\r\n"
            "2. [b][color=#a50000]Wyślij OFF[100 off][/color] (1 z 1)[/b]\n"
            "\r\n"
            "[b]2021-03-03 [color=#ff0000]06:00:00 - 08:00:00[/color][/b]\n"
            "500|501 [b]->[/b] 500|499\n"
            "[url=https://te1.testserver/game.php?village=1&screen=place&target=6&t=0]Wyślij OFF[/url]\r\n"
            "\r\n"
            "3. [b][color=#a500a5]Wyślij SZLACHCIC[5000 off + 1 szlachcic][/color] (1 z 1)[/b]\n"
            "\r\n"
            "[b]2021-03-03 [color=#ff0000]08:25:00 - 09:25:00[/color][/b]\n"
            "500|500 [b]->[/b] 500|499\n"
            "[url=https://te1.testserver/game.php?village=0&screen=place&target=6&t=0]Wyślij SZLACHCIC[/url]\r\n\r\n"
        )
        self.assertEqual(overview.deputy, deputy)
        self.assertEqual(overview.show_hidden, False)
        self.assertEqual(overview.outline_overview, outline_overview)
        target = Target.objects.get(target="500|499")
        print("weights_json")
        print(outline_overview.weights_json)
        print("targets_json")
        print(outline_overview.targets_json)
        print("world_json")
        print(outline_overview.world_json)
        print("outline_json")
        print(outline_overview.outline_json)

        self.assertEqual(
            json.loads(outline_overview.weights_json),
            {
                f"{target.pk}": [
                    {
                        "id": WeightModel.objects.get(
                            state__outline=outline, off=100
                        ).pk,
                        "start": "500|501",
                        "player": "player0",
                        "off": 100,
                        "nobleman": 0,
                        "catapult": 0,
                        "ruin": False,
                        "distance": 2.0,
                        "time_seconds": 82800,
                        "t1": "2021-03-03T07:00:00",
                        "t2": "2021-03-03T09:00:00",
                        "delivery_t1": "2021-03-03T07:00:00+01:00",
                        "delivery_t2": "2021-03-03T09:00:00+01:00",
                        "shipment_t1": "2021-03-03T06:00:00+01:00",
                        "shipment_t2": "2021-03-03T08:00:00+01:00",
                        "village_id": 0,
                        "player_id": 0,
                        "send_url": "https://te1.testserver/game.php?village=0&screen=place&target=0",
                    },
                    {
                        "id": WeightModel.objects.get(
                            state__outline=outline, off=19000
                        ).pk,
                        "start": "500|502",
                        "player": "player0",
                        "off": 19000,
                        "nobleman": 0,
                        "catapult": 0,
                        "ruin": False,
                        "distance": 3.0,
                        "time_seconds": 81000,
                        "t1": "2021-03-03T07:00:00",
                        "t2": "2021-03-03T09:00:00",
                        "delivery_t1": "2021-03-03T07:00:00+01:00",
                        "delivery_t2": "2021-03-03T09:00:00+01:00",
                        "shipment_t1": "2021-03-03T05:30:00+01:00",
                        "shipment_t2": "2021-03-03T07:30:00+01:00",
                        "village_id": 0,
                        "player_id": 0,
                        "send_url": "https://te1.testserver/game.php?village=0&screen=place&target=0",
                    },
                    {
                        "id": WeightModel.objects.get(
                            state__outline=outline, off=5000
                        ).pk,
                        "start": "500|500",
                        "player": "player0",
                        "off": 5000,
                        "nobleman": 1,
                        "catapult": 0,
                        "ruin": False,
                        "distance": 1.0,
                        "time_seconds": 84300,
                        "t1": "2021-03-03T09:00:00",
                        "t2": "2021-03-03T10:00:00",
                        "delivery_t1": "2021-03-03T09:00:00+01:00",
                        "delivery_t2": "2021-03-03T10:00:00+01:00",
                        "shipment_t1": "2021-03-03T08:25:00+01:00",
                        "shipment_t2": "2021-03-03T09:25:00+01:00",
                        "village_id": 0,
                        "player_id": 0,
                        "send_url": "https://te1.testserver/game.php?village=0&screen=place&target=0",
                    },
                ]
            },
        )

        self.assertEqual(
            json.loads(outline_overview.targets_json),
            {
                f"{target.pk}": {
                    "id": target.pk,
                    "target": "500|499",
                    "player": "player1",
                    "fake": False,
                    "ruin": False,
                    "village_id": 0,
                    "player_id": 0,
                }
            },
        )

        self.assertEqual(
            outline_overview.world_json,
            {
                "id": outline.world.pk,
                "name": "te1",
                "server": "testserver",
                "speed_units": 1.0,
                "speed_world": 1.0,
                "full_game_name": "",
            },
        )

        self.assertEqual(
            outline_overview.outline_json,
            {"id": outline.pk, "date": "2021-03-03"},
        )
