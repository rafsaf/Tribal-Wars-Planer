""" File with outline making """
from tribal_wars import input_target
from tribal_wars import target_utils
from tribal_wars import weight_utils
from tribal_wars import write_out_outline
from base import models
from tribal_wars import basic


def make_outline(outline: models.Outline):
    """ Create only weight max models """
    # Remove instances in case of earlier exception
    models.WeightMaximum.objects.filter(outline=outline).delete()

    # Weight max model creating
    weight_max_create_list = []

    deff_troops = weight_utils.DefensiveTroops(outline=outline)
    in_village_troops = deff_troops.in_village_dict()


    try:
        for army in weight_utils.OffTroops(outline=outline):

            if army.coord in in_village_troops:
                in_army = in_village_troops[army.coord]
                in_off = in_army.off
                in_nobleman = in_army.nobleman
            else:
                in_off = None
                in_nobleman = None

            weight_max_create_list.append(
                models.WeightMaximum(
                    outline_id=outline.id,
                    player=army.player,
                    start=army.coord,
                    x_coord=int(army.coord[0:3]),
                    y_coord=int(army.coord[4:7]),
                    off_max=army.off,
                    off_left=army.off,
                    off_in_village=in_off,
                    nobleman_max=army.nobleman,
                    nobleman_left=army.nobleman,
                    nobleman_in_village=in_nobleman,
                    first_line=army.first_line,
                )
            )
    except weight_utils.VillageOwnerDoesNotExist:
        raise KeyError()
    models.WeightMaximum.objects.bulk_create(weight_max_create_list)

    # Make targets
    # Remove instances in case of earlier exception
    models.TargetVertex.objects.filter(outline=outline).delete()

    user_input = outline.initial_outline_targets.split("---")
    # User input targets
    targets_input = input_target.TargetsGeneralInput(
        outline_targets=user_input[0].strip(), world=outline.world, fake=False, outline=outline
    )
    targets_input.generate_targets()
    target_list1 = targets_input.targets
    # target creating
    models.TargetVertex.objects.bulk_create(target_list1)

    # User input fake targets
    fake_input = input_target.TargetsGeneralInput(
        outline_targets=user_input[1].strip(), world=outline.world, fake=True, outline=outline
    )

    fake_input.generate_targets()
    target_list2 = fake_input.targets
    # fakes target creating
    models.TargetVertex.objects.bulk_create(target_list2)


def complete_outline(outline: models.Outline):
    """Auto write out outline """
    user_input = outline.initial_outline_targets.split("---")
    
    targets_general = target_utils.TargetsGeneral(
        outline_targets=user_input[0].strip(), world=outline.world,
    )
    fakes_general = target_utils.TargetsGeneral(
        outline_targets=user_input[1].strip(), world=outline.world,
    )

    # Auto writing outline for user
    targets = list(
        models.TargetVertex.objects.filter(outline=outline, fake=False)
    )
    f_targets = list(
        models.TargetVertex.objects.filter(outline=outline, fake=True)
    )

    # Nobles
    write_out_outline_nobles(targets_general, outline, targets)
    # Nobles fake
    write_out_outline_nobles(fakes_general, outline, f_targets, True)
    # Fake offs
    write_out_outline_offs(fakes_general, outline, f_targets, True)
    # Offs
    write_out_outline_offs(targets_general, outline, targets)


def write_out_outline_nobles(targets_general, outline, targets, fake=False):
    """
    Creates Weights with all User's target nobles if have enough nobles

    Also update Weight Max instances after.

    """
    weight_model_noble_create_list = []
    weight_max_update_list = []

    weights_with_nobles = models.WeightMaximum.objects.filter(
            outline=outline, nobleman_max__gt=0
        )
    if fake:
        weights_with_nobles = list(weights_with_nobles.filter(first_line=False))
    else:
        weights_with_nobles = list(weights_with_nobles.filter(off_max__gt=400))

    for target in targets:
        xxxxxxxxxxxxxxxxxxxx = write_out_outline.WriteTarget(target, outline)
        xxxxxxxxxxxxxxxxxxxx.sorted_weights()
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
            if fake:
                weights_to_add = single_target.parse_fake_noble(
                    nearest_weight, target
                )
            else:
                weights_to_add = single_target.parse_real_noble(
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


def write_out_outline_offs(targets_general, outline, targets, fake=False):
    """
    Creates Weights with all User's target offs if have enough nobles

    Also update Weight Max instances after

    """

    weight_model_off_create_list = []
    weight_max_update_list = []
    if fake:
        min_off = 100
    else:
        min_off = int(outline.initial_outline_min_off)
    weights_max = models.WeightMaximum.objects.filter(
        outline=outline,
        nobleman_left=0,
        off_left__gte=min_off,
        first_line=False,
    )
    if len(weights_max) == 0:
        return

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
        if fake:
            weight_to_add = single_target.parse_fake_off(weight_max, target)
        else:
            weight_to_add = single_target.parse_real_off(weight_max, target)

        weight_model_off_create_list.append(weight_to_add)
        weight_max_update_list.append(weight_max)

    models.WeightModel.objects.bulk_create(weight_model_off_create_list)
    models.WeightMaximum.objects.bulk_update(
        weight_max_update_list,
        ["nobleman_left", "nobleman_state", "off_left", "off_state"],
    )
    if fake:
        if len(targets) > 0:
            return write_out_outline_offs(
                targets_general=targets_general,
                outline=outline,
                targets=targets,
                fake=True,
            )
