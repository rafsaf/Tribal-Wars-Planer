import datetime

from django.contrib.auth.models import User

from base import models


def create_initial_data():
    user1 = User.objects.create_user(username="user1", password="user1")
    user2 = User.objects.create_user(username="user2", password="user2")

    outlines = []
    tribes = []
    villages = []
    players = []
    weight_maxs = []
    weights = []
    targets = []




    TEXT = (
        "500|500,0,0,10000,0,0,0,0,0,2,0,0,\r\n"
        "500|501,0,0,190,0,0,0,0,0,0,0,0,\r\n"
        "500|502,0,0,19500,0,0,0,0,0,0,0,0,\r\n"
        "500|503,0,0,20100,0,0,0,0,0,0,0,0,\r\n"
        "500|504,0,0,20000,0,0,0,0,0,2,0,0,\r\n"
        "500|505,0,0,20000,0,0,0,0,0,2,0,0,"
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

    outline1 = models.Outline.objects.create(
        id=1,
        owner=user1,
        date=datetime.date.today(),
        name="name",
        world=world1,
        ally_tribe_tag=["pl1"],
        enemy_tribe_tag=["pl2"],
        initial_outline_targets="500|499:1:4\r\n500|498:1:2---",
        initial_outline_min_off=15000,
        initial_outline_front_dist=3,
        off_troops=TEXT,
    )


    outline2 = models.Outline.objects.create(
        id=2,
        owner=user1,
        date=datetime.date.today(),
        name="name",
        world=world1,
        ally_tribe_tag=["pl1"],
        enemy_tribe_tag=["pl2"],
        initial_outline_targets="500|499:1:4\r\n500|498:1:2---",
        initial_outline_min_off=15000,
        initial_outline_front_dist=3,
        off_troops=TEXT,
    )
    
    outline3 = models.Outline.objects.create(
        id=3,
        owner=user2,
        date=datetime.date.today(),
        name="name",
        world=world1,
        ally_tribe_tag=["pl1"],
        enemy_tribe_tag=["pl2"],
        initial_outline_targets="500|499:1:4\r\n500|498:1:2---",
        initial_outline_min_off=15000,
        initial_outline_front_dist=3,
        off_troops=TEXT,
    )
    
    outline4 = models.Outline.objects.create(
        id=4,
        owner=user2,
        date=datetime.date.today(),
        name="name",
        world=world1,
        ally_tribe_tag=["pl1"],
        enemy_tribe_tag=["pl2"],
        initial_outline_targets="500|499:1:4\r\n500|498:1:2---",
        initial_outline_min_off=15000,
        initial_outline_front_dist=3,
        off_troops=TEXT,
    )

    ally_tribe = models.Tribe(
        tribe_id=0, tag="pl1", world=world1
    )
    enemy_tribe = models.Tribe(
        tribe_id=1, tag="pl2", world=world1
    )
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

    weight_max1 = models.WeightMaximum(
        x_coord=500,
        y_coord=500,
        player="user1",
        outline=outline1,
        start="500|501",
        off_max=10000,
        off_left=10000,
        off_state=0,
        nobleman_max=2,
        nobleman_left=2,
        first_line=True,
        fake_limit=2
    )
    weights.append(weight_max1)
    weight_max2 = models.WeightMaximum(
        x_coord=500,
        y_coord=501,
        player="user1",
        outline=outline1,
        start="500|501",
        off_max=190,
        off_left=190,
        off_state=0,
        nobleman_max=0,
        nobleman_left=0,
        first_line=True,
        fake_limit=2
    )
    weights.append(weight_max2)
    weight_max3 = models.WeightMaximum(
        x_coord=500,
        y_coord=502,
        player="user1",
        outline=outline1,
        start="500|502",
        off_max=190,
        off_left=190,
        off_state=0,
        nobleman_max=0,
        nobleman_left=0,
        first_line=True,
        fake_limit=2
    )
    weights.append(weight_max3)
    weight_max4 = models.WeightMaximum(
        x_coord=500,
        y_coord=503,
        player="user1",
        outline=outline1,
        start="500|503",
        off_max=19500,
        off_left=19500,
        off_state=0,
        nobleman_max=0,
        nobleman_left=0,
        first_line=True,
        fake_limit=2
    )
    weights.append(weight_max4)
    weight_max5 = models.WeightMaximum(
        x_coord=500,
        y_coord=504,
        player="user1",
        outline=outline1,
        start="500|504",
        off_max=20000,
        off_left=0,
        off_state=20000,
        nobleman_max=2,
        nobleman_left=0,
        first_line=True,
        fake_limit=2
    )
    weights.append(weight_max5)
    weight_max6 = models.WeightMaximum(
        x_coord=500,
        y_coord=505,
        player="user1",
        outline=outline1,
        start="500|505",
        off_max=20000,
        off_left=0,
        off_state=20000,
        nobleman_max=2,
        nobleman_left=0,
        first_line=True,
        fake_limit=2
    )
    weights.append(weight_max6)
    models.WeightMaximum.objects.bulk_create(weights)

