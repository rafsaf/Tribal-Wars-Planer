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

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from base import models

"""
### Users ###
user1 username "user1" password "user1"
user1 username "user2" password "user2"

### Server ###
server dns "testserver" prefix "te"

### World ###
world1 postfix "1"

### Outline ###
outline1 id "1"
outline2 id "2"

### Tribes ###
ally_tribe tag "pl1"
enemy_tribe tag "pl2"

### Players ###
player0 name "player0" tribe "ally_tribe"
player1 name "player1" tribe "enemy_tribe"

### Village ###
ally_village1 coord "500|500" id "0"
ally_village2 coord "500|501" id "1"
ally_village3 coord "500|502" id "2"
ally_village4 coord "500|503" id "3"
ally_village5 coord "500|504" id "4"
ally_village6 coord "500|505" id "5"
enemy_village1 coord "500|499" id "6"
enemy_village2 coord "500|498" id "7"
enemy_village3 coord "500|497" id "8"

### WeightMaximum ###
weight_max1 start "500|500" off_max "10000" player "player0"
weight_max2 start "500|501" off_max "190" player "player0"
weight_max3 start "500|502" off_max "19500" player "player0"
weight_max4 start "500|503" off_max "21000" player "player0"
weight_max5 start "500|504" off_max "20000" player "player0"
weight_max6 start "500|505" off_max "20000" player "player0"

### Targets ###
target1 target "500|499" player "player1" required_off "1" required_noble "1"
target2 target "500|497" player "player1" required_off "[1, 0, 0, 1]" required_noble "[2, 0, 0, 2]"
target3 target "500|498" player "player1" required_off "1" required_noble "2"

### Weights ###
weight1 start "500|500" target "500|499" off 5000 noble 1
weight2 start "500|501" target "500|499" off 100 noble 0
weight3 start "500|502" target "500|499" off 19000 noble 0
"""


def create_initial_data():
    User.objects.bulk_create(
        [
            User(
                username="user1",
                email="user1@email.com",
                password=make_password("user1"),
                is_active=True,
            ),
            User(
                username="user2",
                email="user2@email.com",
                password=make_password("user2"),
                is_active=True,
            ),
        ]
    )
    user1 = User.objects.get(username="user1")
    models.Profile.objects.create(user=user1)
    user2 = User.objects.get(username="user2")
    models.Profile.objects.create(user=user2)

    tribes = []
    villages = []
    players = []

    TEXT = (
        "500|500,0,0,8400,0,0,0,0,200,2,0,0,\r\n"
        "500|501,0,0,190,0,0,0,0,0,0,0,0,\r\n"
        "500|502,0,0,19500,0,0,0,0,0,0,0,0,\r\n"
        "500|503,0,0,20100,0,0,0,0,0,0,0,0,\r\n"
        "500|504,0,0,20000,0,0,0,0,0,2,0,0,\r\n"
        "500|505,0,0,20000,0,0,0,0,0,2,0,0,"
    )

    server_in = models.Server(
        dns="testserver",
        prefix="te",
    )
    models.Server.objects.bulk_create([server_in])
    server = models.Server.objects.get(dns="testserver")
    world1 = models.World.objects.create(
        server=server,
        postfix="1",
        paladin="inactive",
        archer="inactive",
        militia="active",
    )

    outline1 = models.Outline.objects.create(
        id=1,
        owner=user1,
        date=datetime.date(year=2021, day=3, month=3),
        name="name",
        world=world1,
        ally_tribe_tag=["pl1"],
        enemy_tribe_tag=["pl2"],
        initial_outline_targets="500|499:1:1\r\n500|497:1|0|0|1:2|0|0|2\r\n---\r\n500|498:1:2",
        initial_outline_min_off=15000,
        initial_outline_front_dist=3,
        off_troops=TEXT,
    )

    models.Result.objects.create(outline=outline1)

    models.Outline.objects.create(
        id=2,
        owner=user1,
        date=datetime.date(year=2021, day=3, month=3),
        name="name",
        world=world1,
        ally_tribe_tag=["pl1"],
        enemy_tribe_tag=["pl2"],
        initial_outline_targets="500|499:1:4\r\n500|498:1:2---",
        initial_outline_min_off=15000,
        initial_outline_front_dist=3,
        off_troops=TEXT,
    )

    ally_tribe = models.Tribe(tribe_id=0, tag="pl1", world=world1)
    enemy_tribe = models.Tribe(tribe_id=1, tag="pl2", world=world1)
    tribes.append(ally_tribe)
    tribes.append(enemy_tribe)
    models.Tribe.objects.bulk_create(tribes)

    ally_player = models.Player(
        player_id=0,
        name="player0",
        tribe=ally_tribe,
        world=world1,
    )
    enemy_player = models.Player(
        player_id=1, name="player1", tribe=enemy_tribe, world=world1
    )
    players.append(ally_player)
    players.append(enemy_player)
    models.Player.objects.bulk_create(players)

    ally_village1 = models.VillageModel(
        coord="500|500",
        village_id=0,
        x_coord=500,
        y_coord=500,
        player=ally_player,
        world=world1,
    )
    villages.append(ally_village1)
    # front
    ally_village2 = models.VillageModel(
        coord="500|501",
        village_id=1,
        x_coord=500,
        y_coord=501,
        player=ally_player,
        world=world1,
    )
    # front
    villages.append(ally_village2)
    ally_village3 = models.VillageModel(
        coord="500|502",
        village_id=2,
        x_coord=500,
        y_coord=502,
        player=ally_player,
        world=world1,
    )

    villages.append(ally_village3)
    ally_village4 = models.VillageModel(
        coord="500|503",
        village_id=3,
        x_coord=500,
        y_coord=503,
        player=ally_player,
        world=world1,
    )

    villages.append(ally_village4)
    ally_village5 = models.VillageModel(
        coord="500|504",
        village_id=4,
        x_coord=500,
        y_coord=504,
        player=ally_player,
        world=world1,
    )

    villages.append(ally_village5)
    ally_village6 = models.VillageModel(
        coord="500|505",
        village_id=5,
        x_coord=500,
        y_coord=505,
        player=ally_player,
        world=world1,
    )
    villages.append(ally_village6)
    enemy_village1 = models.VillageModel(
        coord="500|499",
        village_id=6,
        x_coord=500,
        y_coord=499,
        player=enemy_player,
        world=world1,
    )
    villages.append(enemy_village1)
    enemy_village2 = models.VillageModel(
        coord="500|498",
        village_id=7,
        x_coord=500,
        y_coord=498,
        player=enemy_player,
        world=world1,
    )
    villages.append(enemy_village2)
    enemy_village3 = models.VillageModel(
        coord="500|497",
        village_id=8,
        x_coord=500,
        y_coord=497,
        player=enemy_player,
        world=world1,
    )
    villages.append(enemy_village3)
    models.VillageModel.objects.bulk_create(villages)

    weight_max1: models.WeightMaximum = models.WeightMaximum.objects.create(
        x_coord=500,
        y_coord=500,
        player="player0",
        outline=outline1,
        start="500|500",
        off_max=10000,
        catapult_max=200,
        catapult_left=200,
        off_left=5000,
        off_state=5000,
        nobleman_max=2,
        nobleman_left=1,
        nobleman_state=1,
        first_line=True,
        ram_max=100,
        ram_left=100,
        ram_state=0,
    )

    weight_max2 = models.WeightMaximum.objects.create(
        x_coord=500,
        y_coord=501,
        player="player0",
        outline=outline1,
        start="500|501",
        off_max=190,
        off_left=90,
        off_state=100,
        nobleman_max=0,
        nobleman_left=0,
        first_line=True,
        ram_max=100,
        ram_left=100,
        ram_state=0,
    )

    weight_max3 = models.WeightMaximum.objects.create(
        x_coord=500,
        y_coord=502,
        player="player0",
        outline=outline1,
        start="500|502",
        off_max=19500,
        off_left=500,
        off_state=19000,
        nobleman_max=0,
        nobleman_left=0,
        first_line=True,
        ram_max=100,
        ram_left=100,
        ram_state=0,
    )

    models.WeightMaximum.objects.create(
        x_coord=500,
        y_coord=503,
        player="player0",
        outline=outline1,
        start="500|503",
        off_max=20100,
        off_left=20100,
        off_state=0,
        nobleman_max=0,
        nobleman_left=0,
        first_line=True,
        ram_max=100,
        ram_left=100,
        ram_state=0,
    )

    models.WeightMaximum.objects.create(
        x_coord=500,
        y_coord=504,
        player="player0",
        outline=outline1,
        start="500|504",
        off_max=20000,
        off_left=0,
        off_state=20000,
        nobleman_max=2,
        nobleman_left=0,
        first_line=True,
        ram_max=100,
        ram_left=100,
        ram_state=0,
    )

    models.WeightMaximum.objects.create(
        x_coord=500,
        y_coord=505,
        player="player0",
        outline=outline1,
        start="500|505",
        off_max=20000,
        off_left=0,
        off_state=20000,
        nobleman_max=2,
        nobleman_left=0,
        first_line=True,
        ram_max=100,
        ram_left=100,
        ram_state=0,
    )

    outlinetime1 = models.OutlineTime.objects.create(outline=outline1)

    time1 = models.PeriodModel(
        outline_time=outlinetime1,
        status="all",
        unit="ram",
        from_time=datetime.time(hour=7),
        to_time=datetime.time(hour=9),
    )
    time2 = models.PeriodModel(
        outline_time=outlinetime1,
        status="all",
        unit="noble",
        from_time=datetime.time(hour=9),
        to_time=datetime.time(hour=10),
    )
    time1.save()
    time2.save()

    target1 = models.TargetVertex(
        target="500|499",
        player="player1",
        required_off=1,
        required_noble=1,
        outline=outline1,
        outline_time=outlinetime1,
    )
    target2 = models.TargetVertex(
        target="500|497",
        player="player1",
        exact_off=[1, 0, 0, 1],
        exact_noble=[2, 0, 0, 2],
        required_off=1,
        required_noble=1,
        outline=outline1,
        outline_time=outlinetime1,
    )
    target3 = models.TargetVertex(
        target="500|498",
        player="player1",
        required_off=1,
        required_noble=2,
        fake=True,
        outline=outline1,
        outline_time=outlinetime1,
    )
    target1.save()
    target2.save()
    target3.save()

    weight1 = models.WeightModel(
        player="player0",
        start="500|500",
        first_line=True,
        order=0,
        target=target1,
        state=weight_max1,
        distance=1,
        off=5000,
        nobleman=0,
        village_id=0,
        catapult=0,
        ruin=False,
        player_id=0,
    )

    weight2 = models.WeightModel(
        player="player0",
        start="500|501",
        first_line=True,
        order=1,
        target=target1,
        state=weight_max2,
        distance=2,
        off=100,
        nobleman=0,
        village_id=0,
        catapult=0,
        ruin=False,
        player_id=0,
    )
    weight3 = models.WeightModel(
        player="player0",
        start="500|502",
        first_line=True,
        order=2,
        target=target1,
        state=weight_max3,
        distance=3,
        off=19000,
        nobleman=1,
        village_id=0,
        catapult=0,
        ruin=False,
        player_id=0,
    )

    weight1.save()
    weight2.save()
    weight3.save()


def create_initial_data_write_outline():
    user1 = User.objects.create_user(username="user1", password="user1")  # type: ignore

    tribes = []
    villages = []
    players = []

    TEXT = (
        "500|500,5<span class='grey'>.</span>803,0,0,10000,0,0,0,0,100,2,0,0,\r\n"
        "500|501,5<span class='grey'>.</span>803,0,0,190,0,0,0,0,100,0,0,0,\r\n"
        "500|502,5<span class='grey'>.</span>803,0,0,19500,0,0,0,0,100,0,0,0,\r\n"
        "500|503,5<span class='grey'>.</span>803,0,0,20100,0,0,0,0,100,0,0,0,\r\n"
        "500|504,5<span class='grey'>.</span>803,0,0,20000,0,0,0,0,100,4,0,0,\r\n"
        "500|505,5<span class='grey'>.</span>803,0,0,20000,0,0,0,0,100,2,0,0,"
    )
    TEXT_DEFF = (
        "500|500,111111111111,w wiosce,0,0,10000,0,0,0,0,100,2,0,0,\r\n"
        "500|501,111111111111,w wiosce,0,0,190,0,0,0,0,100,0,0,0,\r\n"
        "500|502,111111111111,w wiosce,0,0,19500,0,0,0,0,100,0,0,0,\r\n"
        "500|503,111111111111,w wiosce,0,0,20100,0,0,0,0,100,0,0,0,\r\n"
        "500|504,111111111111,w wiosce,0,0,20000,0,0,0,0,100,4,0,0,\r\n"
        "500|505,111111111111,w wiosce,0,0,20000,0,0,0,0,100,2,0,0,"
    )

    server = models.Server.objects.create(
        dns="testserver",
        prefix="te",
    )
    world1 = models.World.objects.create(
        server=server,
        postfix="1",
        paladin="inactive",
        archer="inactive",
        militia="active",
    )

    models.Outline.objects.create(
        id=1,
        owner=user1,
        date=datetime.date(year=2021, day=3, month=3),
        name="name",
        world=world1,
        ally_tribe_tag=["pl1"],
        enemy_tribe_tag=["pl2"],
        initial_outline_min_off=15000,
        initial_outline_front_dist=3,
        off_troops=TEXT,
        deff_troops=TEXT_DEFF,
    )

    ally_tribe = models.Tribe(tribe_id=0, tag="pl1", world=world1)
    enemy_tribe = models.Tribe(tribe_id=1, tag="pl2", world=world1)
    tribes.append(ally_tribe)
    tribes.append(enemy_tribe)
    models.Tribe.objects.bulk_create(tribes)

    ally_player = models.Player(
        player_id=0,
        name="player0",
        tribe=ally_tribe,
        world=world1,
    )
    enemy_player = models.Player(
        player_id=1, name="player1", tribe=enemy_tribe, world=world1
    )
    players.append(ally_player)
    players.append(enemy_player)
    models.Player.objects.bulk_create(players)

    ally_village1 = models.VillageModel(
        coord="500|500",
        village_id=0,
        x_coord=500,
        y_coord=500,
        player=ally_player,
        world=world1,
    )
    villages.append(ally_village1)
    # front
    ally_village2 = models.VillageModel(
        coord="500|501",
        village_id=1,
        x_coord=500,
        y_coord=501,
        player=ally_player,
        world=world1,
    )
    # front
    villages.append(ally_village2)
    ally_village3 = models.VillageModel(
        coord="500|502",
        village_id=2,
        x_coord=500,
        y_coord=502,
        player=ally_player,
        world=world1,
    )

    villages.append(ally_village3)
    ally_village4 = models.VillageModel(
        coord="500|503",
        village_id=3,
        x_coord=500,
        y_coord=503,
        player=ally_player,
        world=world1,
    )

    villages.append(ally_village4)
    ally_village5 = models.VillageModel(
        coord="500|504",
        village_id=4,
        x_coord=500,
        y_coord=504,
        player=ally_player,
        world=world1,
    )

    villages.append(ally_village5)
    ally_village6 = models.VillageModel(
        coord="500|505",
        village_id=5,
        x_coord=500,
        y_coord=505,
        player=ally_player,
        world=world1,
    )
    villages.append(ally_village6)
    enemy_village1 = models.VillageModel(
        coord="500|499",
        village_id=6,
        x_coord=500,
        y_coord=499,
        player=enemy_player,
        world=world1,
    )
    villages.append(enemy_village1)
    enemy_village2 = models.VillageModel(
        coord="500|498",
        village_id=7,
        x_coord=500,
        y_coord=498,
        player=enemy_player,
        world=world1,
    )
    villages.append(enemy_village2)
    enemy_village3 = models.VillageModel(
        coord="500|497",
        village_id=8,
        x_coord=500,
        y_coord=497,
        player=enemy_player,
        world=world1,
    )
    villages.append(enemy_village3)
    models.VillageModel.objects.bulk_create(villages)
