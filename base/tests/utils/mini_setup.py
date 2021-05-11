import datetime
from base.models import Outline, Profile, Server, Tribe, World
import string
import random
from typing import Optional, Literal
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from base.tests.utils.create_user import create_user


class MiniSetup(TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)

    def setUp(self):
        self.username: str = self.random_lower_string()
        self.password: str = self.random_lower_string()
        self.username_foreign: str = self.random_lower_string()
        self.password_foreign: str = self.random_lower_string()
        create_user(self.username, self.password)

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
        self, test_world=False, editable: Literal["active", "inactive"] = "active"
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
            )
            if test_world:
                outline.ally_tribe_tag = ["ALLY"]
                outline.save()
                outline.refresh_from_db()
            return outline

    def create_foreign_outline(
        self, test_world=False, editable: Literal["active", "inactive"] = "active"
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
