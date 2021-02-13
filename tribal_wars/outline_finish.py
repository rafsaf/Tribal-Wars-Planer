import secrets
import json
from tribal_wars import period_utils
from base import models
from tribal_wars import basic
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder


def make_final_outline(outline: models.Outline):
    distinct_player_names = list(
        models.WeightMaximum.objects.filter(outline=outline)
        .distinct("player")
        .values_list("player", flat=True)
    )
    # coord - player_id
    player_id = {}
    players = models.Player.objects.filter(
        name__in=distinct_player_names, world=outline.world
    ).values("name", "player_id")
    for player in players:
        player_id[player["name"]] = player["player_id"]

    queries = basic.TargetWeightQueries(outline=outline, every=True, only_with_weights=True)

    distinct_weight_coords = list(
        models.WeightModel.objects.filter(target__in=queries.targets)
        .distinct("start")
        .values_list("start", flat=True)
    ) + [target.target for target in queries.targets]
    # coord - village_id
    village_id = {}
    villages = models.VillageModel.objects.filter(
        coord__in=distinct_weight_coords, world=outline.world
    ).values("coord", "village_id")
    for village in villages.iterator():
        village_id[village["coord"]] = village["village_id"]

    # target - lst[period1, period2, ...]
    target_period_dict = queries.target_period_dictionary()
    # target - lst[weight1, weight2, ...]
    weights_dict = queries.target_dict_with_weights_extended()
    json_weights = {}

    text = basic.TableText(world=outline.world)
    with text:

        for target, lst in weights_dict.items():

            json_weights[target.target] = list()

            periods_list = target_period_dict[target]
            from_period = period_utils.FromPeriods(
                periods=periods_list, world=outline.world, date=outline.date
            )
            for weight in lst:
                weight = from_period.next(weight=weight)

                text.add_weight(
                    weight=weight,
                    ally_id=village_id[weight.start],
                    enemy_id=village_id[weight.target.target],
                    fake=target.fake,
                    deputy=player_id[weight.player],
                )

                weight.t1 = weight.t1.time()
                weight.t2 = weight.t2.time()

                json_weights[target.target].append(
                    model_to_dict(
                        weight,
                        fields=[
                            "start",
                            "player",
                            "off",
                            "nobleman",
                            "distance",
                            "t1",
                            "t2",
                        ],
                    )
                )
    
    outline_info = basic.OutlineInfo(outline=outline)
    outline_info.generate_nicks()

    result_instance = outline.result
    result_instance.results_outline = text.get_full_result()
    result_instance.results_players = outline_info.players
    result_instance.results_sum_up = outline_info.show_sum_up()
    result_instance.results_export = outline_info.show_export_troops()

    result_instance.save()
    json_weight_dict = json.dumps(json_weights, cls=DjangoJSONEncoder)
    json_targets = queries.targets_json_format()

    outline_overview = models.OutlineOverview.objects.create(
        outline=outline, weights_json=json_weight_dict, targets_json=json_targets
    )
    overviews = []

    for player, table, string, deputy in text.iterate_over():
        token = secrets.token_urlsafe()

        overviews.append(
            models.Overview(
                outline=outline,
                player=player,
                token=token,
                outline_overview=outline_overview,
                table=table,
                string=string,
                deputy=deputy,
                show_hidden=outline.default_show_hidden,
            )
        )
    models.Overview.objects.bulk_create(overviews)
