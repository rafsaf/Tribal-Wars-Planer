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

    text = basic.TableText(world_num=outline.world)
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
                )
                weight.t1 = weight.t1.time()
                weight.t2 = weight.t2.time()

                update_weights.append(weight)
    
    models.WeightModel.objects.bulk_update(update_weights, ['t1', 't2'])

    result_instance = outline.result
    result_instance.results_outline = text.get_full_result()
    result_instance.save()

    overviews = []
    for player, table, string in text.iterate_over():
        token = secrets.token_urlsafe()

        overviews.append(
            models.Overview(
                outline=outline, player=player, token=token,
                table=table, string=string
            )
        )

    models.Overview.objects.bulk_create(overviews)
