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
import random
import secrets
import string
from random import randint
from typing import Literal

from django.contrib.auth.models import User
from django.test import TestCase, TransactionTestCase
from django.urls import reverse

from base.models import (
    Outline,
    OutlineOverview,
    OutlineTime,
    Overview,
    Payment,
    Profile,
    Result,
    Server,
    TargetVertex,
    Tribe,
    WeightMaximum,
    WeightModel,
    World,
)
from base.models.period_model import PeriodModel
from base.tests.test_utils.create_user import create_user


class MiniSetup(TestCase):
    TEST_WORLD_DATA = (
        "100|100,55,100,100,7000,0,100,2800,0,0,350,100,0,0,0,0,0,\r\n"
        "101|101,55,100,100,7001,0,100,2801,0,0,350,100,0,0,0,0,0,\r\n"
        "102|102,55,100,100,7002,0,100,2802,0,0,350,100,0,0,0,0,0,\r\n"
        "103|103,55,100,100,7003,0,100,2803,0,0,350,100,0,0,0,0,0,\r\n"
        "104|104,55,100,100,7004,0,100,2804,0,0,350,100,0,0,0,0,0,\r\n"
        "105|105,55,100,100,7005,0,100,2805,0,0,350,100,0,0,0,0,0,\r\n"
        "106|106,55,100,100,7006,0,100,2806,0,0,350,100,0,0,0,0,0,\r\n"
        "107|107,55,100,100,7007,0,100,2807,0,0,350,100,0,0,0,0,0,\r\n"
        "108|108,55,100,100,7008,0,100,2808,0,0,350,100,0,0,0,0,0,\r\n"
        "109|109,55,100,100,7009,0,100,2809,0,0,350,100,0,0,0,0,0,\r\n"
        "110|110,55,100,100,7010,0,100,2810,0,0,350,100,0,0,0,0,0,\r\n"
        "111|111,55,100,100,7011,0,100,2811,0,0,350,100,0,0,0,0,0,\r\n"
        "112|112,55,100,100,7012,0,100,2812,0,0,350,100,0,0,0,0,0,\r\n"
        "113|113,55,100,100,7013,0,100,2813,0,0,350,100,0,0,0,0,0,\r\n"
        "114|114,55,100,100,7014,0,100,2814,0,0,350,100,0,0,0,0,0,\r\n"
        "115|115,55,100,100,7015,0,100,2815,0,0,350,100,0,0,0,0,0,\r\n"
        "116|116,55,100,100,7016,0,100,2816,0,0,350,100,0,0,0,0,0,\r\n"
        "117|117,55,100,100,7017,0,100,2817,0,0,350,100,0,0,0,0,0,\r\n"
        "118|118,55,100,100,7018,0,100,2818,0,0,350,100,0,0,0,0,0,\r\n"
        "119|119,55,100,100,7019,0,100,2819,0,0,350,100,0,0,0,0,0,\r\n"
        "120|120,55,100,100,7020,0,100,2820,0,0,350,100,0,0,0,0,0,\r\n"
        "121|121,55,100,100,7021,0,100,2821,0,0,350,100,0,0,0,0,0,\r\n"
        "122|122,55,100,100,7022,0,100,2822,0,0,350,100,0,0,0,0,0,\r\n"
        "123|123,55,100,100,7023,0,100,2823,0,0,350,100,0,0,0,0,0,\r\n"
        "124|124,55,100,100,7024,0,100,2824,0,0,350,100,0,0,0,0,0,\r\n"
        "125|125,55,100,100,7025,0,100,2825,0,0,350,100,0,0,0,0,0,\r\n"
        "126|126,55,100,100,7026,0,100,2826,0,0,350,100,0,0,0,0,0,\r\n"
        "127|127,55,100,100,7027,0,100,2827,0,0,350,100,0,0,0,0,0,\r\n"
        "128|128,55,100,100,7028,0,100,2828,0,0,350,100,0,0,0,0,0,\r\n"
        "129|129,55,100,100,7029,0,100,2829,0,0,350,100,0,0,0,0,0,\r\n"
        "130|130,55,100,100,7030,0,100,2830,0,0,350,100,0,2,0,0,0,\r\n"
        "131|131,55,100,100,7031,0,100,2831,0,0,350,100,0,2,0,0,0,\r\n"
        "132|132,55,100,100,7032,0,100,2832,0,0,350,100,0,2,0,0,0,\r\n"
        "133|133,55,100,100,7033,0,100,2833,0,0,350,100,0,2,0,0,0,\r\n"
        "134|134,55,100,100,7034,0,100,2834,0,0,350,100,0,2,0,0,0,\r\n"
        "135|135,55,100,100,7035,0,100,2835,0,0,350,100,0,2,0,0,0,\r\n"
        "136|136,55,100,100,7036,0,100,2836,0,0,350,100,0,2,0,0,0,\r\n"
        "137|137,55,100,100,7037,0,100,2837,0,0,350,100,0,2,0,0,0,\r\n"
        "138|138,55,100,100,7038,0,100,2838,0,0,350,100,0,2,0,0,0,\r\n"
        "139|139,55,100,100,7039,0,100,2839,0,0,350,100,0,2,0,0,0,\r\n"
        "140|140,55,100,100,7040,0,100,2840,0,0,350,100,0,4,0,0,0,\r\n"
        "141|141,55,100,100,7041,0,100,2841,0,0,350,100,0,4,0,0,0,\r\n"
        "142|142,55,100,100,7042,0,100,2842,0,0,350,100,0,4,0,0,0,\r\n"
        "143|143,55,100,100,7043,0,100,2843,0,0,350,100,0,4,0,0,0,\r\n"
        "144|144,55,100,100,7044,0,100,2844,0,0,350,100,0,4,0,0,0,\r\n"
        "145|145,55,100,100,7045,0,100,2845,0,0,350,100,0,4,0,0,0,\r\n"
        "146|146,55,100,100,7046,0,100,2846,0,0,350,100,0,4,0,0,0,\r\n"
        "147|147,55,100,100,7047,0,100,2847,0,0,350,100,0,4,0,0,0,\r\n"
        "148|148,55,100,100,7048,0,100,2848,0,0,350,100,0,4,0,0,0,\r\n"
        "149|149,55,100,100,7049,0,100,2849,0,0,350,100,0,4,0,0,0,"
    )

    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)

    def setUp(self):
        self.username: str = self.random_lower_string()
        self.password: str = self.random_lower_string()
        self.username_foreign: str = self.random_lower_string()
        self.password_foreign: str = self.random_lower_string()
        self.user_me: User | None = None
        self.user_foreign: User | None = None
        self.session = self.client.session

    def login_me(self) -> None:
        self.me()
        login = self.client.login(username=self.username, password=self.password)
        if login is False:
            raise ValueError("Loging is not possible")

    def me(self) -> User:
        if self.user_me is None:
            user = create_user(self.username, self.password)
            self.user_me = user
            return user

        return self.user_me

    def foreign_user(self) -> User:
        if self.user_foreign is None:
            user = create_user(self.username_foreign, self.password_foreign)
            self.user_foreign = user
            return user
        return self.user_foreign

    def login_foreign_user(self) -> None:
        self.foreign_user()
        login = self.client.login(
            username=self.username_foreign, password=self.password_foreign
        )
        if login is False:
            raise ValueError("Foreign loging is not possible")

    def login_page_path(self, next: str | None) -> str:
        main_path = reverse("two_factor:login")
        if next is not None:
            return main_path + f"?next={next}"
        return main_path

    def random_lower_string(self, length=20) -> str:
        return "".join(random.choices(string.ascii_lowercase, k=length))

    def random_integer(self, minimum: int = 0, maximum: int = 50) -> int:
        return random.randint(minimum, maximum)

    def get_world(self, test_world: bool = False, save: bool = True) -> World:
        try:
            if test_world:
                return World.objects.get(postfix="Test")
            else:
                return World.objects.get(postfix="1")
        except World.DoesNotExist:
            if test_world:
                server = Server.objects.create(
                    dns="testserver",
                    prefix="te",
                )
                world1 = World.objects.get(postfix="Test")
            else:
                server_in = Server(
                    dns="nottestserver",
                    prefix="nt",
                )
                Server.objects.bulk_create([server_in])
                server = Server.objects.get(dns="nottestserver")
                world1 = World(
                    server=server,
                    postfix="1",
                    paladin="inactive",
                    archer="inactive",
                    militia="inactive",
                )
            me = self.me()
            my_profile: Profile = Profile.objects.get(user=me)
            my_profile.server = server
            my_profile.save()
            if save:
                world1.save()
                world1.refresh_from_db()
            return world1

    def get_outline(
        self,
        test_world: bool = False,
        name: str = "name",
        editable: Literal["active", "inactive"] = "active",
        written: Literal["active", "inactive"] = "inactive",
        add_result: bool = False,
    ) -> Outline:
        world = self.get_world(test_world=test_world)
        try:
            return Outline.objects.get(name=name)
        except Outline.DoesNotExist:
            outline: Outline = Outline.objects.create(
                name=name,
                date=datetime.date.today(),
                world=world,
                owner=self.me(),
                editable=editable,
                written=written,
            )
            if test_world:
                outline.ally_tribe_tag = ["ALLY"]
                outline.enemy_tribe_tag = ["ENEMY"]
                outline.save()
                outline.refresh_from_db()
            if add_result:
                Result.objects.create(outline=outline)
            return outline

    def create_foreign_outline(
        self,
        test_world=False,
        editable: Literal["active", "inactive"] = "active",
        written: Literal["active", "inactive"] = "inactive",
    ) -> Outline:
        world = self.get_world(test_world=test_world)
        try:
            return Outline.objects.get(name="other_name")
        except Outline.DoesNotExist:
            outline: Outline = Outline.objects.create(
                name="other_name",
                date=datetime.date.today(),
                world=world,
                owner=self.foreign_user(),
                editable=editable,
                written=written,
            )
            return outline

    def create_tribe(self, tag: str) -> Tribe:
        world = self.get_world()
        tribe: Tribe = Tribe.objects.create(
            tribe_id=123,
            tag=tag,
            world=world,
        )
        return tribe

    def create_target_on_test_world(
        self,
        outline: Outline,
        coord: str = "200|200",
        fake: bool = False,
        ruin: bool = False,
        player: str = "AllyPlayer3",
        off: int = 0,
        noble: int = 0,
        many: int = 1,
    ) -> None:
        target: TargetVertex = TargetVertex(
            outline=outline,
            target=coord,
            player=player,
            fake=fake,
            ruin=ruin,
            required_off=off,
            required_noble=noble,
        )
        if many > 1:
            TargetVertex.objects.bulk_create([target for _ in range(many)])
        else:
            target.save()

    def create_outline_time(self, outline: Outline) -> OutlineTime:
        return OutlineTime.objects.create(outline=outline)

    def create_period_model(self, outline: Outline) -> PeriodModel:
        return PeriodModel.objects.create(
            status="all", unit="ram", outline_time=self.create_outline_time(outline)
        )

    def create_period_model_from_time(self, outline_time: OutlineTime) -> PeriodModel:
        return PeriodModel.objects.create(
            status="all", unit="ram", outline_time=outline_time
        )

    def create_overview(
        self,
        outline: Outline,
        player: str | None = None,
        token: str | None = None,
        table: str | None = None,
        string: str | None = None,
        deputy: str | None = None,
        extended: str | None = None,
    ) -> Overview:
        outline_overview = OutlineOverview.objects.create(outline=outline)
        return Overview.objects.create(
            outline_overview=outline_overview,
            outline=outline,
            player=player if player else self.random_lower_string(),
            token=token if token else self.random_lower_string(),
            table=table if table else self.random_lower_string(),
            string=string if string else self.random_lower_string(),
            deputy=deputy if deputy else self.random_lower_string(),
            extended=extended if extended else self.random_lower_string(),
            removed=False,
        )

    def create_weight_maximum(self, outline: Outline, start="110|110") -> WeightMaximum:
        return WeightMaximum.objects.create(
            outline=outline,
            start=start,
            player="player",
            off_max=15000,
            off_left=1500,
            nobleman_max=5,
            nobleman_left=5,
        )

    def create_weight(
        self, target: TargetVertex, weight_max: WeightMaximum, start="500|500"
    ) -> WeightModel:
        return WeightModel.objects.create(
            target=target,
            state=weight_max,
            start=start,
            off=self.random_integer(),
            distance=self.random_integer(),
            nobleman=self.random_integer(),
            order=1,
        )

    def create_random_payment(self) -> Payment:
        stripe = randint(0, 1)
        random_months = randint(1, 3)
        random_month = randint(1, 12)
        random_day = randint(10, 25)
        map1 = {1: 30, 2: 55, 3: 70}

        return Payment.objects.create(
            from_stripe=stripe,
            amount=map1[random_months],
            user=self.me(),
            payment_date=f"2021-{random_month}-{random_day}",
            months=random_months,
            event_id=secrets.token_urlsafe(),
        )


class MiniSetupTransactional(MiniSetup, TransactionTestCase):
    pass
