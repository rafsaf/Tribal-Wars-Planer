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

import json

from django.urls import reverse

from base.tests.test_utils.mini_setup import MiniSetup


class UpdateOutlineOffTroopsTest(MiniSetup):
    def test_outline_update_off_troops___403_not_auth(self):
        outline = self.get_outline(test_world=True)
        outline.off_troops = self.TEST_WORLD_DATA
        outline.get_or_set_off_troops_hash()

        PATH = reverse("rest_api:update_outline_off_troops")

        response = self.client.post(
            PATH,
            data=json.dumps(
                {
                    "outline_id": outline.pk,
                    "old_line": "100|100,100,100,7000,0,100,2800,0,0,350,100,0,0,0,0,0,",
                    "new_line": "100|100,100,100,8000,0,100,2800,0,0,350,100,0,0,0,0,0,",
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 403

    def test_outline_update_off_troops___404_foreign_user_has_no_access(self):
        outline = self.get_outline(test_world=True)
        outline.off_troops = self.TEST_WORLD_DATA
        outline.get_or_set_off_troops_hash()

        PATH = reverse("rest_api:update_outline_off_troops")

        self.login_foreign_user()
        response = self.client.post(
            PATH,
            data=json.dumps(
                {
                    "outline_id": outline.pk,
                    "old_line": "100|100,100,100,7000,0,100,2800,0,0,350,100,0,0,0,0,0,",
                    "new_line": "100|100,100,100,8000,0,100,2800,0,0,350,100,0,0,0,0,0,",
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 404

    def test_outline_update_off_troops___400_invalid_payload_type(self):
        outline = self.get_outline(test_world=True)
        outline.off_troops = self.TEST_WORLD_DATA
        outline.get_or_set_off_troops_hash()

        PATH = reverse("rest_api:update_outline_off_troops")

        self.login_me()
        # invalid village
        response = self.client.post(
            PATH,
            data=json.dumps(
                {
                    "outline_id": outline.pk,
                    "old_line": "xxxxxx,100,100,7000,0,100,2800,0,0,350,100,0,0,0,0,0,",
                    "new_line": "100|100,100,100,8000,0,100,2800,0,0,350,100,0,0,0,0,0,",
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 400
        # invalid troops
        response = self.client.post(
            PATH,
            data=json.dumps(
                {
                    "outline_id": outline.pk,
                    "old_line": "100|100,100,100,7000,0,",
                    "new_line": "100|100,100,100,8000,0,100,2800,0,0,350,100,0,0,0,0,0,",
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_outline_update_off_troops___404_line_not_exists_in_off_troops(self):
        outline = self.get_outline(test_world=True)
        outline.off_troops = self.TEST_WORLD_DATA
        outline.get_or_set_off_troops_hash()

        PATH = reverse("rest_api:update_outline_off_troops")

        self.login_me()
        # old_line valid but not in off_troops
        response = self.client.post(
            PATH,
            data=json.dumps(
                {
                    "outline_id": outline.pk,
                    "old_line": "100|100,100,100,700,0,100,2800,0,0,350,100,0,0,0,0,0,",
                    "new_line": "100|100,100,100,8000,0,100,2800,0,0,350,100,0,0,0,0,0,",
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 404

    def test_outline_update_off_troops___204_valid_replace_troops_old_line_to_new(self):
        outline = self.get_outline(test_world=True)
        outline.off_troops = self.TEST_WORLD_DATA
        outline.get_or_set_off_troops_hash()

        PATH = reverse("rest_api:update_outline_off_troops")

        self.login_me()
        # old_line valid but not in off_troops
        response = self.client.post(
            PATH,
            data=json.dumps(
                {
                    "outline_id": outline.pk,
                    "old_line": "100|100,100,100,7000,0,100,2800,0,0,350,100,0,0,0,0,0,",
                    "new_line": "100|100,100,100,8000,0,100,1400,0,0,350,100,0,0,0,0,0,",
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 204
        outline.refresh_from_db()
        assert outline.off_troops == (
            "100|100,100,100,8000,0,100,1400,0,0,350,100,0,0,0,0,0,\r\n"
            "101|101,100,100,7001,0,100,2801,0,0,350,100,0,0,0,0,0,\r\n"
            "102|102,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,\r\n"
            "103|103,100,100,7003,0,100,2803,0,0,350,100,0,0,0,0,0,\r\n"
            "104|104,100,100,7004,0,100,2804,0,0,350,100,0,0,0,0,0,\r\n"
            "105|105,100,100,7005,0,100,2805,0,0,350,100,0,0,0,0,0,\r\n"
            "106|106,100,100,7006,0,100,2806,0,0,350,100,0,0,0,0,0,\r\n"
            "107|107,100,100,7007,0,100,2807,0,0,350,100,0,0,0,0,0,\r\n"
            "108|108,100,100,7008,0,100,2808,0,0,350,100,0,0,0,0,0,\r\n"
            "109|109,100,100,7009,0,100,2809,0,0,350,100,0,0,0,0,0,\r\n"
            "110|110,100,100,7010,0,100,2810,0,0,350,100,0,0,0,0,0,\r\n"
            "111|111,100,100,7011,0,100,2811,0,0,350,100,0,0,0,0,0,\r\n"
            "112|112,100,100,7012,0,100,2812,0,0,350,100,0,0,0,0,0,\r\n"
            "113|113,100,100,7013,0,100,2813,0,0,350,100,0,0,0,0,0,\r\n"
            "114|114,100,100,7014,0,100,2814,0,0,350,100,0,0,0,0,0,\r\n"
            "115|115,100,100,7015,0,100,2815,0,0,350,100,0,0,0,0,0,\r\n"
            "116|116,100,100,7016,0,100,2816,0,0,350,100,0,0,0,0,0,\r\n"
            "117|117,100,100,7017,0,100,2817,0,0,350,100,0,0,0,0,0,\r\n"
            "118|118,100,100,7018,0,100,2818,0,0,350,100,0,0,0,0,0,\r\n"
            "119|119,100,100,7019,0,100,2819,0,0,350,100,0,0,0,0,0,\r\n"
            "120|120,100,100,7020,0,100,2820,0,0,350,100,0,0,0,0,0,\r\n"
            "121|121,100,100,7021,0,100,2821,0,0,350,100,0,0,0,0,0,\r\n"
            "122|122,100,100,7022,0,100,2822,0,0,350,100,0,0,0,0,0,\r\n"
            "123|123,100,100,7023,0,100,2823,0,0,350,100,0,0,0,0,0,\r\n"
            "124|124,100,100,7024,0,100,2824,0,0,350,100,0,0,0,0,0,\r\n"
            "125|125,100,100,7025,0,100,2825,0,0,350,100,0,0,0,0,0,\r\n"
            "126|126,100,100,7026,0,100,2826,0,0,350,100,0,0,0,0,0,\r\n"
            "127|127,100,100,7027,0,100,2827,0,0,350,100,0,0,0,0,0,\r\n"
            "128|128,100,100,7028,0,100,2828,0,0,350,100,0,0,0,0,0,\r\n"
            "129|129,100,100,7029,0,100,2829,0,0,350,100,0,0,0,0,0,\r\n"
            "130|130,100,100,7030,0,100,2830,0,0,350,100,0,2,0,0,0,\r\n"
            "131|131,100,100,7031,0,100,2831,0,0,350,100,0,2,0,0,0,\r\n"
            "132|132,100,100,7032,0,100,2832,0,0,350,100,0,2,0,0,0,\r\n"
            "133|133,100,100,7033,0,100,2833,0,0,350,100,0,2,0,0,0,\r\n"
            "134|134,100,100,7034,0,100,2834,0,0,350,100,0,2,0,0,0,\r\n"
            "135|135,100,100,7035,0,100,2835,0,0,350,100,0,2,0,0,0,\r\n"
            "136|136,100,100,7036,0,100,2836,0,0,350,100,0,2,0,0,0,\r\n"
            "137|137,100,100,7037,0,100,2837,0,0,350,100,0,2,0,0,0,\r\n"
            "138|138,100,100,7038,0,100,2838,0,0,350,100,0,2,0,0,0,\r\n"
            "139|139,100,100,7039,0,100,2839,0,0,350,100,0,2,0,0,0,\r\n"
            "140|140,100,100,7040,0,100,2840,0,0,350,100,0,4,0,0,0,\r\n"
            "141|141,100,100,7041,0,100,2841,0,0,350,100,0,4,0,0,0,\r\n"
            "142|142,100,100,7042,0,100,2842,0,0,350,100,0,4,0,0,0,\r\n"
            "143|143,100,100,7043,0,100,2843,0,0,350,100,0,4,0,0,0,\r\n"
            "144|144,100,100,7044,0,100,2844,0,0,350,100,0,4,0,0,0,\r\n"
            "145|145,100,100,7045,0,100,2845,0,0,350,100,0,4,0,0,0,\r\n"
            "146|146,100,100,7046,0,100,2846,0,0,350,100,0,4,0,0,0,\r\n"
            "147|147,100,100,7047,0,100,2847,0,0,350,100,0,4,0,0,0,\r\n"
            "148|148,100,100,7048,0,100,2848,0,0,350,100,0,4,0,0,0,\r\n"
            "149|149,100,100,7049,0,100,2849,0,0,350,100,0,4,0,0,0,"
        )
