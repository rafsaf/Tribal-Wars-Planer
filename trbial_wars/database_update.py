
from . import basic
from base.models import VillageModel, Tribe, Player, World
from urllib.parse import unquote, unquote_plus
import requests



def cron_schedule_data_update():
    """ Update Tribe, VillageModel, Player instances to database """

    if not World.objects.filter(world=0).exists():
        World.objects.create(title='Świat 0', world=0)
        Tribe.objects.create(id='ALLY::0', tribe_id=0, tag='ALLY', world=0)
        Tribe.objects.create(id='ENEMY::0', tribe_id=1, tag='ENEMY', world=0)
        ally_villages = []
        ally_players = []
        enemy_players = []
        enemy_villages = []

        for i in range(5):
            ally_players.append(Player(id=f'AllyPlayer{i}:0', tribe_id=0, world=0, player_id=i, name=f'AllyPlayer{i}'))
            enemy_players.append(Player(id=f'EnemyPlayer{i}:0', tribe_id=1, world=0, player_id=i+5, name=f'EnemyPlayer{i}'))

        for i in range(50):
            ids = i // 10
            ally_villages.append(
                VillageModel(world=0, id=f'{100+i}{100+i}0', x_coord=100+i, y_coord=100+i, village_id=i, player_id=ids)
            )
            enemy_villages.append(
                VillageModel(world=0, id=f'{200+i}{200+i}0', x_coord=200+i, y_coord=200+i, village_id=i+50, player_id=ids+5)
            )
        Player.objects.bulk_create(enemy_players)
        Player.objects.bulk_create(ally_players)

        VillageModel.objects.bulk_create(enemy_villages)
        VillageModel.objects.bulk_create(ally_villages)

    worlds = World.objects.all().exclude(world=0)
    ## VillageModel Model Update
    for instance in worlds:
    
        context = {}
        create_list = list()
        update_list = list()
        query = VillageModel.objects.filter(world=instance.world)
        
        for village in query.iterator(chunk_size=4000):
            context[f'{village.x_coord}{village.y_coord}{instance.world}'] = village
        
        req = requests.get(f"https://pl{instance.world}.plemiona.pl/map/village.txt").text
        x = [i.split(',') for i in req.split('\n')]
        for line in x:
            if line == ['']:
                continue
            pk = f'{line[2]}{line[3]}{instance.world}'
            if pk not in context:
                village = VillageModel(id=pk, village_id=line[0], x_coord=line[2], y_coord=line[3], player_id=line[4], world=instance.world)
                create_list.append(village)
            else:
                village = context[pk]
                if village.player_id != int(line[4]):
                    village.player_id = int(line[4])
                    update_list.append(village)
                del context[pk]
        VillageModel.objects.bulk_create(create_list)
        VillageModel.objects.bulk_update(update_list, ['player_id'])
        
        if len(context) != 0:
            village_ids = [village.id for village in context.values()]
            VillageModel.objects.filter(pk__in=village_ids).delete()

   
        context = {}
        create_list = list()
        tribe_ids = []
        
        for tribe in Tribe.objects.filter(world=instance.world):
            context[tribe.tribe_id] = tribe
        
        for line in [i.split(',') for i in requests.get(f"https://pl{instance.world}.plemiona.pl/map/ally.txt").text.split('\n')]:
            if line == ['']:
                continue
            tribe_id = int(line[0])
            if tribe_id not in context:
                tag = unquote(unquote_plus(line[2]))

                tribe = Tribe(
                    id=f'{tag}::{instance.world}',
                    tribe_id=line[0],
                    tag=tag,
                    world=instance.world)
                create_list.append(tribe)
            else:
                tribe = context[tribe_id]
                tag = unquote(unquote_plus(line[2]))
                
                if tribe.tag != tag:
                    new_tribe = Tribe(id=f'{tag}::{instance.world}', tribe_id=tribe.tribe_id, tag=tag, world=instance.world)
                    create_list.append(new_tribe)
                    tribe_ids.append(tribe.id)
                    
                del context[tribe_id]
        if len(context) != 0:
            for tribe in context.values():
                tribe_ids.append(tribe.id)
        Tribe.objects.filter(id__in=tribe_ids).delete()
            
        Tribe.objects.bulk_create(create_list)
    

        context = {}
        create_list = list()
        update_list = list()
        
        for player in Player.objects.filter(world=instance.world).iterator():
            context[player.name] = player
        
        for line in [i.split(',') for i in requests.get(f"https://pl{instance.world}.plemiona.pl/map/player.txt").text.split('\n')]:
            if line == ['']:
                continue
            name = unquote(unquote_plus(line[1]))
            if name not in context:
                player = Player(id=f'{name}:{instance.world}', player_id=line[0], name=name, tribe_id=line[2], world=instance.world)
                create_list.append(player)
            else:
                player = context[name]
                if player.tribe_id != int(line[2]):
                    player.tribe_id = int(line[2])
                    update_list.append(player)
                del context[name]
        Player.objects.bulk_create(create_list)
        Player.objects.bulk_update(update_list, ['tribe_id'])
        
        if len(context) != 0:
            player_ids = [player.id for player in context.values()]
            Player.objects.filter(pk__in=player_ids).delete()
