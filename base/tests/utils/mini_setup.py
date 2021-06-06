import datetime
import random
import string
from typing import Literal, Optional

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from base.models import (
    Outline,
    OutlineOverview,
    OutlineTime,
    Overview,
    Profile,
    Result,
    Server,
    TargetVertex,
    Tribe,
    World,
)
from base.tests.utils.create_user import create_user


class MiniSetup(TestCase):
    TEST_WORLD_DATA = (
        "100|100,100,100,7000,0,100,2800,0,0,350,100,0,0,0,0,0,\r\n"
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

    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)

    def setUp(self):
        self.username: str = self.random_lower_string()
        self.password: str = self.random_lower_string()
        self.username_foreign: str = self.random_lower_string()
        self.password_foreign: str = self.random_lower_string()
        create_user(self.username, self.password)
        self.session = self.client.session

    def login_me(self) -> None:
        login = self.client.login(username=self.username, password=self.password)
        if login is False:
            raise ValueError("Loging is not possible")

    def me(self) -> User:
        return User.objects.get(username=self.username)

    def foreign_user(self) -> User:
        try:
            return User.objects.get(username=self.username_foreign)
        except User.DoesNotExist:
            create_user(self.username_foreign, self.password_foreign)
            return User.objects.get(username=self.username_foreign)

    def login_foreign_user(self) -> None:
        login = self.client.login(
            username=self.username_foreign, password=self.password_foreign
        )
        if login is False:
            create_user(self.username_foreign, self.password_foreign)
            self.client.login(
                username=self.username_foreign, password=self.password_foreign
            )

    def login_page_path(self, next: Optional[str]) -> str:
        main_path = reverse("login")
        if next is not None:
            return main_path + f"?next={next}"
        return main_path

    def random_lower_string(self, length=20) -> str:
        return "".join(random.choices(string.ascii_lowercase, k=length))

    def random_integer(self, minimum: int = 0, maximum: int = 50) -> int:
        return random.randint(minimum, maximum)

    def get_world(self, test_world=False) -> World:
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
                    dns="testserver",
                    prefix="te",
                )
                Server.objects.bulk_create([server_in])
                server = Server.objects.get(dns="testserver")
                world1: World = World.objects.create(
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
            return world1

    def get_outline(
        self,
        test_world=False,
        editable: Literal["active", "inactive"] = "active",
        written: Literal["active", "inactive"] = "inactive",
        add_result: bool = False,
    ) -> Outline:
        world = self.get_world(test_world=test_world)
        try:
            return Outline.objects.get(name="name")
        except Outline.DoesNotExist:
            outline: Outline = Outline.objects.create(
                name="name",
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

    def create_overview(self, outline: Outline) -> Overview:
        outline_overview = OutlineOverview.objects.create(outline=outline)
        return Overview.objects.create(
            outline_overview=outline_overview,
            outline=outline,
            player=self.random_lower_string(),
            token=self.random_lower_string(),
            table=self.random_lower_string(),
            string=self.random_lower_string(),
            removed=False,
        )
