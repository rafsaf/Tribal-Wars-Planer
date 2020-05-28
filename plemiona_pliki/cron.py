from urllib.parse import unquote_plus, unquote

import requests

from data.models import Village, Tribe, Player, World


def cron_schedule_data_update():
    worlds = World.objects.all()
    """Village Model Update"""
    for instance in worlds:
        Village.objects.all().filter(world=instance.world).delete()
        x = [i.split(',') for i in
             requests.get(f"https://pl{instance.world}.plemiona.pl/map/village.txt").text.split('\n')]
        village_list = [
            Village(village_id=unquote(unquote_plus(i[0])), x=i[2], y=i[3], player_id=i[4], points=i[5],
                    world=instance.world) for i in
            x if i != ['']
        ]
        Village.objects.bulk_create(village_list)
    """Tribe Model Update"""
    for instance in worlds:
        Tribe.objects.all().filter(world=instance.world).delete()
        x = [i.split(',') for i in
             requests.get(f"https://pl{instance.world}.plemiona.pl/map/ally.txt").text.split('\n')]
        tribe_list = [
            Tribe(tribe_id=i[0], name=unquote(unquote_plus(i[1])), tag=unquote(unquote_plus(i[2])), members=i[3],
                  villages=i[4], points=i[5], all_points=i[6], rank=i[7], world=instance.world) for i in x if i != ['']
        ]
        Tribe.objects.bulk_create(tribe_list)
    """Player Model update"""
    for instance in worlds:
        Player.objects.all().filter(world=instance.world).delete()
        x = [i.split(',') for i in
             requests.get(f"https://pl{instance.world}.plemiona.pl/map/player.txt").text.split('\n')]
        player_list = [
            Player(player_id=i[0], name=unquote(unquote_plus(i[1])), tribe_id=i[2], villages=i[3], points=i[4],
                   rank=i[5], world=instance.world) for i in x if i != ['']
        ]
        Player.objects.bulk_create(player_list)


def update_Village():
    worlds = World.objects.all()
    for instance in worlds:
        Village.objects.all().filter(world=instance.world).delete()
        x = [i.split(',') for i in
             requests.get(f"https://pl{instance.world}.plemiona.pl/map/village.txt").text.split('\n')]
        village_list = [
            Village(village_id=i[0], x=i[2], y=i[3], player_id=i[4], points=i[5], world=instance.world) for i in
            x if i != ['']
        ]
        Village.objects.bulk_create(village_list)


def update_Player():
    worlds = World.objects.all()
    for instance in worlds:
        Player.objects.all().filter(world=instance.world).delete()
        x = [i.split(',') for i in
             requests.get(f"https://pl{instance.world}.plemiona.pl/map/player.txt").text.split('\n')]
        player_list = [
            Player(player_id=i[0], name=unquote(unquote_plus(i[1])), tribe_id=i[2], villages=i[3], points=i[4],
                   rank=i[5], world=instance.world) for i in x if i != ['']
        ]
        Player.objects.bulk_create(player_list)


def update_Tribe():
    worlds = World.objects.all()
    for instance in worlds:
        Tribe.objects.all().filter(world=instance.world).delete()
        x = [i.split(',') for i in
             requests.get(f"https://pl{instance.world}.plemiona.pl/map/ally.txt").text.split('\n')]
        tribe_list = [
            Tribe(village_id=i[0], name=unquote(unquote_plus(i[1])), tag=unquote(unquote_plus(i[2])), members=i[3],
                  villages=i[4], points=i[5], all_points=i[6], rank=i[7], world=instance.world) for i in x if i != ['']
        ]
        Tribe.objects.bulk_create(tribe_list)
