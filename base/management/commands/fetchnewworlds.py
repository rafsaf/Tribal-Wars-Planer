# Copyright 2023 Rafał Safin (rafsaf). All Rights Reserved.
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


import logging
from concurrent import futures
from time import sleep
from django.conf import settings

from django.core.management.base import BaseCommand

import metrics
from base.management.commands.utils import job_logs_and_metrics
from base.models import World
from utils.database_update import WorldUpdateHandler


import requests
from bs4 import BeautifulSoup
from base import forms
from base.models import Server, World
import logging

log = logging.getLogger(__name__)


def get_lst_of_available_worlds(tw_server: Server) -> list[str]:
    worlds: list[str] = []
    page_url = f"https://{tw_server.dns}/page/stats"
    res = requests.get(
        page_url,
        allow_redirects=True,
    )
    soup = BeautifulSoup(res.text, features="html.parser")
    worlds_div = soup.find_all("div", attrs={"class": "content-selector"})[1]
    for world_li in worlds_div.ul.find_all("li"):
        world_url: str = world_li.a["href"]
        world_postfix = (
            world_url.removeprefix("https://")
            .split(".")[0]
            .removeprefix(tw_server.prefix)
        )
        worlds.append(world_postfix)
    return worlds


def fetch_and_add_new_worlds() -> None:
    db_worlds = World.objects.all().select_related("server")
    servers = Server.objects.all()
    for server in servers:
        log.info("processing server: %s", server.dns)
        available_worlds_postfixes = get_lst_of_available_worlds(server)
        server_worlds_postfixes = set(
            db_world.postfix for db_world in db_worlds if db_world.server == server
        )
        for world_postfix in available_worlds_postfixes:
            if world_postfix in server_worlds_postfixes:
                continue
            world_form = forms.AddNewWorldForm(
                {"server": server.dns, "postfix": world_postfix}
            )
            if world_form.is_valid():
                log.info("added world %s,%s successfully", server.dns, world_postfix)
                sleep(0.2)
            log.error(
                "adding world %s,%s failed: %s",
                server.dns,
                world_postfix,
                world_form.errors,
            )
        sleep(0.5)


class Command(BaseCommand):
    help = "Fetch new game worlds"

    @job_logs_and_metrics(log)
    def handle(self, *args, **options) -> None:
        fetch_and_add_new_worlds()
