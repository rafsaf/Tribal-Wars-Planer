""" File with outline making and getting stuff """

from base import models
from . import basic
from .basic import timing
import random

def make_outline(outline: models.Outline):
    """ Make empty outline """
    village_dict = basic.coord_to_player(outline=outline)
    evidence = basic.world_evidence(outline.world)
    target_info_dict = {}
    for target_info in outline.initial_outline_targets.split("\r\n"):
        target_info = target_info.split(":")
        target_info_dict[target_info[0]] = {
            "off": int(target_info[1]),
            "nob": int(target_info[2]),
        }
    
    target_vertex_list = []
    off_troops = outline.off_troops.split("\r\n")
    # Target creating
    target_village_dict = basic.coord_to_player_from_string(
        village_coord_list=" ".join(target_info_dict), world=outline.world,
    )
    for target in target_village_dict:
        target_vertex_list.append(
            models.TargetVertex(
                outline_id=outline.id,
                target=target,
                player=target_village_dict[target],
            )
        )

    query1 = models.TargetVertex.objects.filter(outline=outline)
    query2 = models.WeightModel.objects.filter(target__in=query1)
    query2._raw_delete(query2.db)
    query1._raw_delete(query1.db)
    models.TargetVertex.objects.bulk_create(target_vertex_list)
    # Weight max creating
    weight_max_list = []
    for line in off_troops:
        army = basic.Army(text_army=line, evidence=evidence)
        try:
            player = village_dict[army.coord]
        except KeyError:
            raise KeyError()
        if army.off < 500 and army.nobleman == 0:
            continue
        if army.deff > 5000 and army.nobleman == 0:
            continue
        weight_max_list.append(
            models.WeightMaximum(
                outline_id=outline.id,
                player=player,
                start=army.coord,
                off_max=army.off,
                off_left=army.off,
                nobleman_max=army.nobleman,
                nobleman_left=army.nobleman,
            )
        )

    query3 = models.WeightMaximum.objects.filter(outline=outline)
    query3._raw_delete(query3.db)
    models.WeightMaximum.objects.bulk_create(weight_max_list)
    return make_outline_next(target_info_dict, outline)


@timing
def make_outline_next(target_info_dict: dict, outline: models.Outline):
    weight_max_list = list(models.WeightMaximum.objects.filter(outline=outline))
    targets = list(models.TargetVertex.objects.filter(outline=outline))
    weight_create_list = []
    weight_max_update = []
    context_off = {}
    context_nob = {}

    for target in targets:
        context_nob[target] = target_info_dict[target.target]['nob']
        context_off[target] = target_info_dict[target.target]['off']
        

    for target in targets:
        weight_max_list.sort(key=lambda weight: basic.dist(weight.start, target.target))

        for weight_max in weight_max_list:
            required = context_nob[target]
            if required == 0:
                break

            if weight_max.nobleman_max == 0:
                continue
            
            if weight_max.nobleman_max > required:
                nob = required

            else:
                nob = weight_max.nobleman_max

            army = weight_max.off_max // nob
            for i in range(100, 100 + nob):
                weight_create_list.append(
                    models.WeightModel(
                        target=target,
                        player=weight_max.player,
                        start=weight_max.start,
                        state=weight_max,
                        off=army,
                        distance=basic.dist(weight_max.start, target.target),
                        nobleman=1,
                        order=i
                    )
                )
            context_nob[target] -= nob
            weight_max.nobleman_left = weight_max.nobleman_max - nob
            weight_max.nobleman_state = nob
            weight_max.off_state = weight_max.off_max
            weight_max.off_left = 0
            weight_max_update.append(weight_max)
    random.shuffle(weight_max_list)
    for weight in weight_max_list:
        if weight.off_max < 19000 and weight.nobleman_max == 0:
            continue

        off = weight.off_max
        if off > 19000 and len(context_off) != 0:
            min_off_target = min(
                context_off,
                key=lambda target: basic.dist(weight.start, target.target)
            )
            required = context_off[min_off_target]
            army = weight.off_max
            weight_create_list.append(
                models.WeightModel(
                target=min_off_target,
                player=weight.player,
                start=weight.start,
                state=weight,
                off=army,
                distance=basic.dist(weight.start, min_off_target.target),
                nobleman=0,
                order=required
                )
            )
            context_off[min_off_target] -= 1
            if context_off[min_off_target] == 0:
                del context_off[min_off_target]
            weight.off_state = weight.off_max
            weight.off_left = 0
            weight_max_update.append(weight)
            continue
        continue

    models.WeightModel.objects.bulk_create(weight_create_list)
    models.WeightMaximum.objects.bulk_update(weight_max_update, ['nobleman_left','nobleman_state', 'off_left', 'off_state'])