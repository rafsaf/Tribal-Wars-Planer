
from . import basic
from .basic.timer import t
from base.models import VillageModel, Tribe, Player, World
from time import time
from urllib.parse import unquote, unquote_plus
import requests
import json



#@basic.timing
#def cron_schedule_data_update():
 #   """ Update Tribe, VillageModel, Player instances to database """
 #   worlds = World.objects.all()
 #   url = 'https://api.tribalwarshelp.com/graphql'
 #   for instance in worlds:
 #       world = instance.world
 #       query1 = f'query{{villages(server:"pl{world}"){{items{{id x y player{{id name tribe{{id tag}}}}}}}}}}'
 #       query2 = f'query{{players(server:"pl{world}"){{items{{id name tribe{{id tag}}}}}}}}'
 #       query3 = f'query{{tribes(server:"pl{world}"){{items{{id tag}}}}}}'
#
#
 #       context1 = {}
 #       create_list1 = []
 #       update_list1 = []
 #       for village in VillageModel.objects.filter(world=world).iterator():
 #           context1[f'{village.x_coord}{village.y_coord}{world}'] = village
 #       data = json.loads(requests.post(url, json={'query': query1}).text)['data']['villages']['items']
 #       for line1 in data:
 #           pk = f"{line1['x']}{line1['y']}{world}"
 #           if pk not in context1:
 #               if line1['player'] is None:
 #                   player_id = 0   
 #                   player_name = ""
 #                   tribe_id = 0
 #                   tribe_tag = ""    
 #               else:
 #                   player_id = line1['player']['id']
 #                   player_name = line1['player']['name']
 #                   if line1['player']['tribe'] is None:
 #                       tribe_id = 0
 #                       tribe_tag = ""
 #                   else:
 #                       tribe_id = line1['player']['tribe']['id']
 #                       tribe_tag = line1['player']['tribe']['tag']
#
 #               village = VillageModel(
 #                   id=pk, 
 #                   village_id=line1['id'],
 #                   x_coord=line1['x'],
 #                   y_coord=line1['y'],
 #                   player_id=player_id, 
 #                   player_name=player_name, 
 #                   tribe_id=tribe_id, 
 #                   tribe_tag=tribe_tag, 
 #                   world=world)
 #               create_list1.append(village)
 #           else:
 #               village = context1[pk]
 #               if line1['player'] is None:
 #                   player_id = 0   
 #                   player_name = ""
 #                   tribe_id = 0
 #                   tribe_tag = "" 
 #               else:
 #                   player_id = line1['player']['id']
 #                   player_name = line1['player']['name']
 #                   if line1['player']['tribe'] is None:
 #                       tribe_id = 0
 #                       tribe_tag = ""
 #                   else:
 #                       tribe_id = line1['player']['tribe']['id']
 #                       tribe_tag = line1['player']['tribe']['tag']
#
 #               if village.player_id != player_id or village.tribe_id != tribe_id:
 #                   village.player_id = player_id
 #                   village.player_name = player_name
 #                   village.tribe_id = tribe_id
 #                   village.tribe_name = tribe_tag
 #                   update_list1.append(village)
 #               del context1[pk]
 #       VillageModel.objects.bulk_create(create_list1)
 #       VillageModel.objects.bulk_update(update_list1, ['player_id', 'tribe_id', 'player_name', 'tribe_tag'])
 #       
 #       if len(context1) != 0:
 #           village_ids = [village.id for village in context1.values()]
 #           VillageModel.objects.filter(pk__in=village_ids).delete()



@basic.timing
def cron_schedule_data_update():
    """ Update Tribe, VillageModel, Player instances to database """

    worlds = World.objects.all()
    ## VillageModel Model Update
    for instance in worlds:
    #    q1 = VillageModel.objects.all().filter(world=instance.world)
    #    q1._raw_delete(q1.db)
    #    x = [
    #        i.split(',') for i in requests.get(
    #            f"https://pl{instance.world}.plemiona.pl/map/village.txt").
    #        text.split('\n')
    #    ]
    #    village_list = [
    #        VillageModel(
    #                id=f'{i[2]}{i[3]}{instance.world}',
    #                village_id=i[0],
    #                x_coord=i[2],
    #                y_coord=i[3],
    #                player_id=i[4],
    #                world=instance.world) for i in x if i != ['']
    #    ]
    #    VillageModel.objects.bulk_create(village_list)
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

    # Tribe Model Update
    
        #q2 = Tribe.objects.all().filter(world=instance.world)
        #q2._raw_delete(q2.db)
        #x = [
        #    i.split(',') for i in requests.get(
        #        f"https://pl{instance.world}.plemiona.pl/map/ally.txt").text.
        #    split('\n')
        #]
        #tribe_list = [
        #    Tribe(id=f'{unquote(unquote_plus(i[2]))}::{instance.world}',
        #            tribe_id=i[0],
        #            tag=unquote(unquote_plus(i[2])),
        #            world=instance.world) for i in x
        #    if i != [''] and ', ' not in unquote(unquote_plus(i[2]))
        #]
        #Tribe.objects.bulk_create(tribe_list)
        context = {}
        create_list = list()
        update_list = list()
        
        for tribe in Tribe.objects.filter(world=instance.world).iterator():
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
                    tribe.tag = tag
                    tribe.id = f'{tag}::{instance.world}'
                del context[tribe_id]
        Tribe.objects.bulk_create(create_list)
        Tribe.objects.bulk_update(update_list, ['tribe_id'])
        
        if len(context) != 0:
            tribe_ids = [tribe.id for tribe in context.values()]
            Tribe.objects.filter(pk__in=tribe_ids).delete()
        
    # Player Model Update
        #q3 = Player.objects.all().filter(world=instance.world)
        #q3._raw_delete(q3.db)
        #x = [
        #    i.split(',') for i in requests.get(
        #        f"https://pl{instance.world}.plemiona.pl/map/player.txt").text.
        #    split('\n')
        #]
        #player_list = [
        #    Player(id=f'{unquote(unquote_plus(i[1]))}:{instance.world}',
        #            player_id=i[0],
        #            name=unquote(unquote_plus(i[1])),
        #            tribe_id=i[2],
        #            world=instance.world) for i in x if i != ['']
        #]
        #Player.objects.bulk_create(player_list)


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
