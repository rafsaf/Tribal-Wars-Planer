import secrets
from collections import deque

from tribal_wars import period_utils
from base import models
from tribal_wars import basic


def make_final_outline(outline: models.Outline):
    village_dict = basic.coord_to_player(outline=outline)

    context_with_target_id = {}
    context_with_target_weight = {}
    context_with_target_period = {}
    context_with_time_period = {}

    targets = models.TargetVertex.objects.select_related(
        "outline_time"
    ).filter(outline=outline)

    for target in targets:
        context_with_target_id[target.id] = target
        context_with_target_weight[target.id] = deque()
        context_with_time_period[target.outline_time.id] = deque()

    periods = (
        models.PeriodModel.objects.select_related("outline_time")
        .filter(
            outline_time__in=[target.outline_time.id for target in targets]
        )
        .order_by("from_time", "-unit")
    )

    for period in periods:
        context_with_time_period[period.outline_time.id].append(period)

    for target in targets:
        context_with_target_period[target.id] = context_with_time_period[
            target.outline_time.id
        ]

    weights = models.WeightModel.objects.select_related("target").filter(
        target__in=targets
    )
    villages_id = set()
    for weight in weights:
        villages_id.add(
            f"{weight.target.target[0:3]}"
            f"{weight.target.target[4:7]}{outline.world}"
        )
        villages_id.add(
            f"{weight.start[0:3]}{weight.start[4:7]}{outline.world}"
        )
        context_with_target_weight[weight.target.id].append(weight)
    world_model = models.World.objects.get(world=outline.world)

    village_id = {}
    result_dictionary = {}

    for village in models.VillageModel.objects.filter(id__in=villages_id):
        village_id[f"{village.x_coord}|{village.y_coord}"] = village.village_id

    for target_id, lst in context_with_target_weight.items():
        periods_list = list(context_with_target_period[target_id])
        from_period = period_utils.FromPeriods(
            periods=periods_list, world=world_model, date=outline.date
        )
        for weight in lst:
            if weight.nobleman > 0:
                unit = "noble"
            else:
                unit = "ram"

            weight = from_period.next(weight=weight)
            link = f"https://pl{outline.world}.plemiona.pl/game.php?village={village_id[weight.start]}&screen=place&target={village_id[weight.target.target]}"
            try:
                result_dictionary[
                    village_dict[weight.start]
                ] += f"[*][url={link}]Link[/url][|][coord]{weight.start}[/coord][|][coord]{weight.target.target}[/coord][|]{unit}[|]{weight.off}[|]{weight.nobleman}[|]{weight.sh_t1}[|]{weight.sh_t2}[|]{weight.t1}[|]{weight.t2}"
            except KeyError:
                result_dictionary[
                    village_dict[weight.start]
                ] = f"[*][url={link}]Link[/url][|][coord]{weight.start}[/coord][|][coord]{weight.target.target}[/coord][|]{unit}[|]{weight.off}[|]{weight.nobleman}[|]{weight.sh_t1}[|]{weight.sh_t2}[|]{weight.t1}[|]{weight.t2}"

    prefix = "[table][**]LINK[||]Z WIOSKI[||]CEL[||]PRĘDKOŚĆ[||]OFF[||]SZLACHTA[||]MIN WYSYŁKA[||]MAX WYSYŁKA[||]MIN WEJŚCIE[||]MAX WEJŚCIE[/**]"
    postfix = "[/table]"
    result = ""
    for i, j in result_dictionary.items():
        j = prefix + j + postfix
        result_dictionary[i] = j
        result += "\r\n\r\n" + i + "\r\n" + j
    res = outline.result
    res.results_outline = result
    res.save()
    players_set = set(village_dict.values())

    overviews = []
    for player in players_set:
        token = secrets.token_urlsafe()
        try:
            text = result_dictionary[player]
        except KeyError:
            continue

        overviews.append(
            models.Overview(
                outline=outline, player=player, token=token, text=text,
            )
        )

    models.Overview.objects.bulk_create(overviews)
