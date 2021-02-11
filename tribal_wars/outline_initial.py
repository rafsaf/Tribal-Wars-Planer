""" File with outline making """
from tribal_wars import input_target
from tribal_wars import weight_utils
from tribal_wars import write_out_outline
from base import models
from tribal_wars import basic


def make_outline(outline: models.Outline, target_mode: basic.TargetMode = None):
    """ Create weight max models and/or targets """

    if models.WeightMaximum.objects.filter(outline=outline).count() == 0:
        weight_max_create_list = []

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

        models.WeightMaximum.objects.bulk_create(weight_max_create_list)

    if target_mode is not None:
        # Remove targets
        models.TargetVertex.objects.filter(
            outline=outline, fake=target_mode.fake, ruin=target_mode.ruin
        ).delete()

        # Create targets depend of target mode
        if target_mode.is_real:
            user_input: str = outline.initial_outline_targets.strip()
        elif target_mode.is_fake:
            user_input: str = outline.initial_outline_fakes.strip()
        else:
            user_input: str = outline.initial_outline_ruins.strip()

        targets = input_target.TargetsGeneralInput(
            outline_targets=user_input,
            world=outline.world,
            fake=target_mode.fake,
            ruin=target_mode.ruin,
            outline=outline,
        )

        models.TargetVertex.objects.bulk_create(targets.list(), batch_size=500)




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
