""" File with outline making """
from trbial_wars import target_utils
from trbial_wars import weight_utils
from base import models
from trbial_wars import basic


def make_outline(outline: models.Outline):
    """ Make empty outline, then auto write out it """
    # Remove instances in case of earlier exception
    models.WeightMaximum.objects.filter(outline=outline).delete()
    models.TargetVertex.objects.filter(outline=outline).delete()

    # User input targets
    targets_general = target_utils.TargetsGeneral(
        outline_targets=outline.initial_outline_targets, world=outline.world,
    )

    # Target model creating
    target_model_create_list = []

    for coord in targets_general:
        target_model_create_list.append(
            models.TargetVertex(
                outline_id=outline.id,
                target=coord,
                player=targets_general.player(coord),
            )
        )

    models.TargetVertex.objects.bulk_create(target_model_create_list)

    # Weight max model creating
    weight_max_create_list = []

    try:
        for army in weight_utils.OffTroops(outline=outline):
            if not army.is_enough_off_units():
                continue
            else:
                weight_max_create_list.append(
                    models.WeightMaximum(
                        outline_id=outline.id,
                        player=army.player,
                        start=army.coord,
                        off_max=army.off,
                        off_left=army.off,
                        nobleman_max=army.nobleman,
                        nobleman_left=army.nobleman,
                        first_line=army.first_line,
                    )
                )
    except weight_utils.VillageOwnerDoesNotExist:
        raise KeyError()

    models.WeightMaximum.objects.bulk_create(weight_max_create_list)

    # Auto writing outline for user
    targets = list(models.TargetVertex.objects.filter(outline=outline))

    # Nobles
    write_out_outline_nobles(targets_general, outline, targets)
    # Offs
    write_out_outline_offs(targets_general, outline, targets)


def write_out_outline_nobles(targets_general, outline, targets):
    """
    Creates Weights with all User's target nobles if have enough nobles

    Also update Weight Max instances after.

    """
    weight_model_noble_create_list = []
    weight_max_update_list = []

    weights_with_nobles = list(
        models.WeightMaximum.objects.filter(
            outline=outline, nobleman_max__gt=0, off_max__gt=400
        )
    )

    for target in targets:
        index_error = False
        single_target: target_utils.SingleTarget = targets_general.single(
            target.target
        )
        if single_target.are_nobles_not_required():
            continue
        weights_with_nobles.sort(
            key=lambda weight: basic.dist(weight.start, target.target),
            reverse=True,
        )
        while single_target.are_nobles_to_write_out():
            try:
                nearest_weight = weights_with_nobles.pop()
            except IndexError:
                index_error = True
                break  # after all nobles are used, move to finish func

            weights_to_add = single_target.parse_nearest(
                nearest_weight, target
            )
            for weight_model in weights_to_add:
                weight_model_noble_create_list.append(weight_model)
            weight_max_update_list.append(nearest_weight)

        if index_error:
            break

    models.WeightModel.objects.bulk_create(weight_model_noble_create_list)
    models.WeightMaximum.objects.bulk_update(
        weight_max_update_list,
        ["nobleman_left", "nobleman_state", "off_left", "off_state"],
    )


def write_out_outline_offs(targets_general, outline, targets):
    """
    Creates Weights with all User's target offs if have enough nobles

    Also update Weight Max instances after

    """

    weight_model_off_create_list = []
    weight_max_update_list = []
    
    weights_max = models.WeightMaximum.objects.filter(
        outline=outline,
        nobleman_left=0,
        off_left__gte=int(outline.initial_outline_min_off),
        first_line=False
    )

    for weight_max in weights_max:
        targets.sort(
            key=lambda target: basic.dist(weight_max.start, target.target),
            reverse=True,
        )
        try:
            target = targets[-1]
        except IndexError:
            break
        single_target = targets_general.single(target.target)
        if not single_target.are_offs_to_write_out():
            targets.pop()
            continue

        weight_to_add = single_target.parse_off(weight_max, target)
        weight_model_off_create_list.append(weight_to_add)
        weight_max_update_list.append(weight_max)

    models.WeightModel.objects.bulk_create(weight_model_off_create_list)
    models.WeightMaximum.objects.bulk_update(
        weight_max_update_list,
        ["nobleman_left", "nobleman_state", "off_left", "off_state"],
    )
