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
from time import sleep

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from requests.adapters import HTTPAdapter, Retry

from base import forms
from base.management.commands.utils import job_logs_and_metrics
from base.models import Server, World

log = logging.getLogger(__name__)
retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])


def get_lst_of_available_worlds(tw_server: Server) -> dict[str, str]:
    worlds: dict[str, str] = {}
    page_url = f"https://{tw_server.dns}/page/stats"
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retries))
    res = session.get(
        page_url,
        allow_redirects=True,
        timeout=5,
        headers={
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "*/*",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        },
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
        worlds[world_postfix] = world_li.a.text.strip()
    return worlds


def fetch_and_add_new_worlds() -> None:
    db_worlds = World.objects.all().select_related("server")
    servers = Server.objects.all()
    for server in servers:
        log.info("processing server: %s", server.dns)
        try:
            available_worlds_postfixes = get_lst_of_available_worlds(server)
        except Exception as err:
            log.error(
                "failed to get list of worlds from server: %s: %s",
                server.dns,
                err,
                exc_info=True,
            )
            sleep(1)
            continue
        server_worlds_postfixes = {
            db_world.postfix: db_world
            for db_world in db_worlds
            if db_world.server == server
        }
        for world_postfix in available_worlds_postfixes:
            if world_postfix in server_worlds_postfixes:
                log.info("world %s:%s already here", server.dns, world_postfix)
                world = server_worlds_postfixes[world_postfix]
                if world.full_game_name != available_worlds_postfixes[world_postfix]:
                    world.full_game_name = available_worlds_postfixes[world_postfix]
                    world.save()
                continue
            log.info("adding world %s:%s", server.dns, world_postfix)
            try:
                world_form = forms.AddNewWorldForm(
                    {"server": server.dns, "postfix": world_postfix}
                )
                if world_form.is_valid():
                    log.info(
                        "added world %s,%s successfully", server.dns, world_postfix
                    )
                    World.objects.filter(
                        server=server,
                        postfix=world_postfix,
                    ).update(full_game_name=available_worlds_postfixes[world_postfix])

                    sleep(1)
                    continue
                log.error(
                    "adding world %s,%s failed: %s",
                    server.dns,
                    world_postfix,
                    world_form.errors,
                )
            except Exception as err:
                log.error(
                    "adding world %s,%s failed: %s",
                    server.dns,
                    world_postfix,
                    err,
                    exc_info=True,
                )
                sleep(1)
        sleep(1)


class Command(BaseCommand):
    help = "Fetch new game worlds"

    @job_logs_and_metrics(log)
    def handle(self, *args, **options) -> None:
        fetch_and_add_new_worlds()
