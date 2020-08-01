from urllib.parse import unquote_plus, unquote

import requests

from base.models import VillageModel, Tribe, Player, World


def cron_schedule_data_update():
    """ Update Tribe, VillageModel, Player instances to database """

    worlds = World.objects.all()
    # VillageModel Model Update
    for instance in worlds:
        VillageModel.objects.all().filter(world=instance.world).delete()
        x = [
            i.split(',') for i in requests.get(
                f"https://pl{instance.world}.plemiona.pl/map/village.txt").
            text.split('\n')
        ]
        village_list = [
            VillageModel(
                    id=f'{i[2]}{i[3]}{instance.world}',
                    village_id=i[0],
                    x_coord=i[2],
                    y_coord=i[3],
                    player_id=i[4],
                    world=instance.world) for i in x if i != ['']
        ]
        VillageModel.objects.bulk_create(village_list)
    # Tribe Model Update
    for instance in worlds:
        Tribe.objects.all().filter(world=instance.world).delete()
        x = [
            i.split(',') for i in requests.get(
                f"https://pl{instance.world}.plemiona.pl/map/ally.txt").text.
            split('\n')
        ]
        tribe_list = [
            Tribe(id=f'{unquote(unquote_plus(i[2]))}::{instance.world}',
                  tribe_id=i[0],
                  tag=unquote(unquote_plus(i[2])),
                  world=instance.world) for i in x
            if i != [''] and ', ' not in unquote(unquote_plus(i[2]))
        ]
        Tribe.objects.bulk_create(tribe_list)
    # Player Model Update
    for instance in worlds:
        Player.objects.all().filter(world=instance.world).delete()
        x = [
            i.split(',') for i in requests.get(
                f"https://pl{instance.world}.plemiona.pl/map/player.txt").text.
            split('\n')
        ]
        player_list = [
            Player(id=f'{unquote(unquote_plus(i[1]))}:{instance.world}',
                   player_id=i[0],
                   name=unquote(unquote_plus(i[1])),
                   tribe_id=i[2],
                   world=instance.world) for i in x if i != ['']
        ]
        Player.objects.bulk_create(player_list)
