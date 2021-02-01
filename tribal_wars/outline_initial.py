""" File with outline making """
from tribal_wars import input_target
from tribal_wars import target_utils
from tribal_wars import weight_utils
from tribal_wars import write_out_outline
from base import models
from tribal_wars import basic


def make_outline(outline: models.Outline, make_targets=True):
    """ Create only weight max models """
    # Remove instances in case of earlier exception
    if models.WeightMaximum.objects.filter(outline=outline).count() == 0:
        # Weight max model creating
        weight_max_create_list = []

        try:
            for army in weight_utils.OffTroops(outline=outline):

                weight_max_create_list.append(
                    models.WeightMaximum(
                        outline_id=outline.id,
                        player=army.player,
                        start=army.coord,
                        x_coord=int(army.coord[0:3]),
                        y_coord=int(army.coord[4:7]),
                        off_max=army.off,
                        off_left=army.off,
                        nobleman_max=army.nobleman,
                        nobleman_left=army.nobleman,
                        first_line=army.first_line,
                        fake_limit=outline.initial_outline_fake_limit,
                    )
                )
        except weight_utils.VillageOwnerDoesNotExist:
            raise KeyError()
        models.WeightMaximum.objects.bulk_create(weight_max_create_list)

    if make_targets:
        # Make targets 
        # Remove instances in case of earlier exception
        models.TargetVertex.objects.filter(outline=outline).delete()
        user_input = outline.initial_outline_targets.split("---")
        # User input targets
        targets_input = input_target.TargetsGeneralInput(
            outline_targets=user_input[0].strip(),
            world=outline.world,
            fake=False,
            outline=outline,
        )
        targets_input.generate_targets()
        target_list1 = targets_input.targets
        # target creating
        models.TargetVertex.objects.bulk_create(target_list1)

        # User input fake targets
        fake_input = input_target.TargetsGeneralInput(
            outline_targets=user_input[1].strip(),
            world=outline.world,
            fake=True,
            outline=outline,
        )

        fake_input.generate_targets()
        target_list2 = fake_input.targets
        # fakes target creating
        models.TargetVertex.objects.bulk_create(target_list2)

@basic.timing
def complete_outline(outline: models.Outline):
    """Auto write out outline """
    # user_input = outline.initial_outline_targets.split("---")
    #
    # targets_general = target_utils.TargetsGeneral(
    #     outline_targets=user_input[0].strip(), world=outline.world,
    # )
    # fakes_general = target_utils.TargetsGeneral(
    #     outline_targets=user_input[1].strip(), world=outline.world,
    # )

    # Auto writing outline for user
    world: models.World = outline.world
    targets = models.TargetVertex.objects.filter(outline=outline, fake=False).order_by(
        "id"
    )
    fakes = models.TargetVertex.objects.filter(outline=outline, fake=True).order_by(
        "id"
    )
    modes_list = ["closest", "close", "random", "far"]

    leave = False
    for target in fakes:
        if leave:
            break

        if target.required_off == 0:
            if len(target.exact_off) == 4:
                for required_off, mode in zip(
                    target.exact_off, modes_list
                ):  # closest, close, random, far
                    if required_off == 0:
                        continue
                    target.required_off = required_off
                    target.mode_off = mode

                    parsed = write_out_outline.WriteTarget(target, outline, world)
                    parsed.write_ram()
                    if parsed.end_up_offs:
                        leave = True
                        break
            continue

        parsed = write_out_outline.WriteTarget(target, outline, world)
        parsed.write_ram()
        if parsed.end_up_offs:
            break

    for target in targets:
        if target.required_noble == 0:
            if len(target.exact_noble) == 4:
                for required_noble, mode in zip(
                    target.exact_noble, modes_list
                ):  # closest, close, random, far
                    if required_noble == 0:
                        continue
                    target.required_noble = required_noble
                    target.mode_noble = mode

                    parsed = write_out_outline.WriteTarget(target, outline, world)
                    parsed.write_noble()

            continue

        parsed = write_out_outline.WriteTarget(target, outline, world)
        parsed.write_noble()

    leave = False
    for target in targets:
        if leave:
            break

        if target.required_off == 0:
            if len(target.exact_off) == 4:
                for required_off, mode in zip(
                    target.exact_off, modes_list
                ):  # closest, close, random, far
                    if required_off == 0:
                        continue
                    target.required_off = required_off
                    target.mode_off = mode

                    parsed = write_out_outline.WriteTarget(target, outline, world)
                    parsed.write_ram()
                    if parsed.end_up_offs:
                        leave = True
                        break
            continue

        parsed = write_out_outline.WriteTarget(target, outline, world)
        parsed.write_ram()
        if parsed.end_up_offs:
            break

    for target in fakes:

        if target.required_noble == 0:
            if len(target.exact_noble) == 4:
                for required_noble, mode in zip(
                    target.exact_noble, modes_list
                ):  # closest, close, random, far
                    if required_noble == 0:
                        continue
                    target.required_noble = required_noble
                    target.mode_noble = mode

                    parsed = write_out_outline.WriteTarget(target, outline, world)
                    parsed.write_noble()
            continue

        parsed = write_out_outline.WriteTarget(target, outline, world)
        parsed.write_noble()


