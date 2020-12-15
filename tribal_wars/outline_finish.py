import secrets

from tribal_wars import period_utils
from base import models
from tribal_wars import basic


def make_final_outline(outline: models.Outline):

    queries = basic.TargetWeightQueries(outline=outline, every=True)

    # target - lst[period1, period2, ...]
    target_period_dict = queries.target_period_dictionary()
    target_weight_ext_dict = queries.target_dict_with_weights_extended()

    # target - lst[weight1, weight2, ...]
    weights_dict = target_weight_ext_dict["weights"]

    # coord - village_id
    village_id = target_weight_ext_dict["village_ids"]
    player_id = target_weight_ext_dict["player_ids"]

    text = basic.TableText(world=outline.world)
    update_weights = []

    with text:

        for target, lst in weights_dict.items():
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
                    deputy=player_id[weight.start]
                )
                weight.t1 = weight.t1.time()
                weight.t2 = weight.t2.time()

                update_weights.append(weight)
  
    models.WeightModel.objects.bulk_update(update_weights, ['t1', 't2'])
  
    outline_info = basic.OutlineInfo(outline=outline)
    outline_info.generate_nicks()

    result_instance = outline.result
    result_instance.results_outline = text.get_full_result()
    result_instance.results_players = outline_info.players
    result_instance.results_sum_up = outline_info.show_sum_up()

    result_instance.save()

    outline_overview = models.OutlineOverview.objects.create(outline=outline)
    overviews = []
    for player, table, string, deputy in text.iterate_over():
        token = secrets.token_urlsafe()

        overviews.append(
            models.Overview(
                outline=outline, player=player, token=token, outline_overview=outline_overview,
                table=table, string=string, deputy=deputy, show_hidden=outline.default_show_hidden
            )
        )
    models.Overview.objects.bulk_create(overviews)

    targets_overwiews = []
    weight_overwiews = []
    for target in models.TargetVertex.objects.filter(outline=outline):
        targets_overwiews.append(
            models.TargetVertexOverview(
                player=target.player,
                target=target.target,
                fake=target.fake,
                outline_overview=outline_overview,
                target_vertex=target,
            )
        )
    models.TargetVertexOverview.objects.bulk_create(targets_overwiews)
    target_context = {}
    for targets_overwiew in models.TargetVertexOverview.objects.filter(outline_overview=outline_overview):
        target_context[targets_overwiew.target_vertex] = targets_overwiew

    for weight in models.WeightModel.objects.select_related("target", "target__outline").filter(target__outline=outline):
        weight_overwiews.append(
            models.WeightModelOverview(
                player=weight.player,
                start=weight.start,
                order=weight.order,
                target=target_context[weight.target],
                distance=weight.distance,
                off=weight.off,
                nobleman=weight.nobleman,
                t1=weight.t1,
                t2=weight.t2,
            )
        )
    models.WeightModelOverview.objects.bulk_create(weight_overwiews)
    