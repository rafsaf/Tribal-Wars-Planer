""" File with outline making """
from tribal_wars.basic.ruin import RuinHandle
from django.db.models.query import QuerySet
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
                    outline_id=outline.pk,
                    player=army.player,
                    start=army.coord,
                    x_coord=int(army.coord[0:3]),
                    y_coord=int(army.coord[4:7]),
                    off_max=army.off,
                    off_left=army.off,
                    catapult_max=army.catapult,
                    catapult_left=army.catapult,
                    nobleman_max=army.nobleman,
                    nobleman_left=army.nobleman,
                    first_line=False,
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
            user_input: str = outline.initial_outline_targets
        elif target_mode.is_fake:
            user_input: str = outline.initial_outline_fakes
        else:
            user_input: str = outline.initial_outline_ruins

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
    world: models.World = outline.world
    targets = models.TargetVertex.objects.filter(
        outline=outline, fake=False, ruin=False
    ).order_by("id")
    fakes = models.TargetVertex.objects.filter(
        outline=outline, fake=True, ruin=False
    ).order_by("id")
    ruins = models.TargetVertex.objects.filter(
        outline=outline, fake=False, ruin=True
    ).order_by("id")

    create_weights(fakes, outline, world, noble=False)
    create_weights_ruin(ruins, outline, world)
    create_weights(targets, outline, world, noble=True)
    create_weights(targets, outline, world, noble=False)
    create_weights(ruins, outline, world, noble=False)
    create_weights(fakes, outline, world, noble=True)


def create_weights(
    targets_query: QuerySet,
    outline: models.Outline,
    world: models.World,
    noble=False,
) -> None:
    modes_list = ["closest", "close", "random", "far"]

    target: models.TargetVertex
    for target in targets_query.iterator():

        if noble:
            if target.required_noble == 0:  # extended syntax
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
            else:
                parsed: write_out_outline.WriteTarget = write_out_outline.WriteTarget(
                    target, outline, world
                )
                parsed.write_noble()

        else:
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
                            return
            else:
                parsed = write_out_outline.WriteTarget(target, outline, world)
                parsed.write_ram()
                if parsed.end_up_offs:
                    break


def create_weights_ruin(
    targets_query: QuerySet,
    outline: models.Outline,
    world: models.World,
) -> None:
    modes_list = ["random", "random", "random", "random"]
    target: models.TargetVertex
    for target in targets_query.iterator():
        # here noble numbers becomes offs and we treat it like off
        target.required_off = target.required_noble
        target.exact_off = target.exact_noble
        target.mode_off = "random"

        if target.required_off == 0:
            if len(target.exact_off) == 4:
                for required_off, mode in zip(
                    target.exact_off, modes_list
                ):  # random, random, random, random
                    if required_off == 0:
                        continue
                    target.required_off = required_off
                    target.mode_off = mode

                    parsed = write_out_outline.WriteTarget(
                        target, outline, world, ruin=True
                    )
                    parsed.write_ram()
                    if parsed.end_up_offs:
                        return
        else:
            parsed = write_out_outline.WriteTarget(target, outline, world, ruin=True)
            parsed.write_ram()
            if parsed.end_up_offs:
                break