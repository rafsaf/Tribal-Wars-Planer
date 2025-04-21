# Copyright 2021 Rafał Safin (rafsaf). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


from base import models
from utils.basic.cdist_brute import CDistBrute


def calculate_and_update_available_troops(outline: models.Outline):  # noqa: PLR0912
    excluded_coords_text: str = outline.initial_outline_excluded_coords
    excluded_coords = set(
        (int(coord[0:3]), int(coord[4:7])) for coord in excluded_coords_text.split()
    )

    min_radius: float = float(outline.initial_outline_front_dist)
    max_radius: float = float(outline.initial_outline_maximum_off_dist)

    [
        all_noble,
        front_noble,
        back_noble,
        too_far_noble,
        all_off,
        front_off,
        back_off,
        too_far_off,
        all_full_noble_off,
        front_full_noble_off,
        back_full_noble_off,
        too_far_full_noble_off,
        all_noble_near,
        front_noble_near,
        back_noble_near,
        too_far_noble_near,
        all_off_near,
        front_off_near,
        back_off_near,
        too_far_off_near,
        all_catapults,
        front_catapults,
        back_catapults,
        too_far_catapults,
        available_ruins,
    ] = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    ally_villages = models.WeightMaximum.objects.filter(outline=outline).only(
        "pk",
        "x_coord",
        "y_coord",
        "off_left",
        "nobleman_left",
        "catapult_left",
        "first_line",
        "too_far_away",
    )

    ally_villages_coords = [
        (village.x_coord, village.y_coord) for village in ally_villages
    ]

    enemy_villages_coords = (
        models.VillageModel.objects.select_related()
        .filter(player__tribe__tag__in=outline.enemy_tribe_tag, world=outline.world)
        .values_list("x_coord", "y_coord")
    )
    enemy_villages_coords = [
        coord for coord in enemy_villages_coords if coord not in excluded_coords
    ]

    if len(enemy_villages_coords) > 0:
        front_set, away_set = CDistBrute(
            ally_villages=ally_villages_coords,
            enemy_villages=enemy_villages_coords,  # type: ignore[assignment]
            min_radius=min_radius,
            max_radius=max_radius,
        ).double_result()
    else:
        front_set = set()
        away_set = set()

    target_villages_coords = [
        target.coord_tuple()
        for target in models.TargetVertex.objects.filter(outline=outline).only(
            "target",
        )
    ]
    target_villages_coords = [
        coord for coord in target_villages_coords if coord not in excluded_coords
    ]

    target_radius = float(outline.initial_outline_target_dist)
    if len(target_villages_coords) > 0:
        front_set_near, _ = CDistBrute(
            ally_villages=ally_villages_coords,
            enemy_villages=target_villages_coords,
            min_radius=target_radius,
            max_radius=target_radius,
        ).double_result()
    else:
        front_set_near = set()

    front_pk: list[int] = []
    back_pk: list[int] = []
    away_pk: list[int] = []

    for weight_max in ally_villages:
        coords = weight_max.coord_tuple()
        if coords in front_set:
            front_noble += weight_max.nobleman_left
            all_noble += weight_max.nobleman_left
            all_catapults += weight_max.catapult_left
            front_catapults += weight_max.catapult_left
            if (
                weight_max.off_left >= outline.initial_outline_min_off
                and weight_max.off_left <= outline.initial_outline_max_off
            ):
                all_off += 1
                front_off += 1
                if weight_max.nobleman_left >= 1:
                    all_full_noble_off += 1
                    front_full_noble_off += 1

            if not weight_max.first_line:
                front_pk.append(weight_max.pk)

            if coords in front_set_near:
                front_noble_near += weight_max.nobleman_left
                all_noble_near += weight_max.nobleman_left
                if (
                    weight_max.off_left >= outline.initial_outline_min_off
                    and weight_max.off_left <= outline.initial_outline_max_off
                ):
                    all_off_near += 1
                    front_off_near += 1

        elif coords in away_set:
            too_far_noble += weight_max.nobleman_left
            all_noble += weight_max.nobleman_left
            all_catapults += weight_max.catapult_left
            too_far_catapults += weight_max.catapult_left
            if (
                weight_max.off_left >= outline.initial_outline_min_off
                and weight_max.off_left <= outline.initial_outline_max_off
            ):
                all_off += 1
                too_far_off += 1
                if weight_max.nobleman_left >= 1:
                    all_full_noble_off += 1
                    too_far_full_noble_off += 1

            if not weight_max.too_far_away:
                away_pk.append(weight_max.pk)

            if coords in front_set_near:
                too_far_noble_near += weight_max.nobleman_left
                all_noble_near += weight_max.nobleman_left
                if (
                    weight_max.off_left >= outline.initial_outline_min_off
                    and weight_max.off_left <= outline.initial_outline_max_off
                ):
                    all_off_near += 1
                    too_far_off_near += 1

        else:
            back_noble += weight_max.nobleman_left
            all_noble += weight_max.nobleman_left
            all_catapults += weight_max.catapult_left
            back_catapults += weight_max.catapult_left
            if (
                weight_max.off_left >= outline.initial_outline_min_off
                and weight_max.off_left <= outline.initial_outline_max_off
            ):
                all_off += 1
                back_off += 1
                if weight_max.nobleman_left >= 1:
                    all_full_noble_off += 1
                    back_full_noble_off += 1
            if (
                weight_max.off_left >= outline.initial_outline_min_ruin_attack_off
                and weight_max.catapult_left
                >= outline.initial_outline_catapult_min_value
            ):
                available_ruins += weight_max.catapult_left

            if coords in front_set_near:
                back_noble_near += weight_max.nobleman_left
                all_noble_near += weight_max.nobleman_left
                if (
                    weight_max.off_left >= outline.initial_outline_min_off
                    and weight_max.off_left <= outline.initial_outline_max_off
                ):
                    all_off_near += 1
                    back_off_near += 1

            if weight_max.first_line or weight_max.too_far_away:
                back_pk.append(weight_max.pk)

    batch_size = 1000
    for i in range(0, len(front_pk), batch_size):
        batch = front_pk[i : i + batch_size]
        models.WeightMaximum.objects.filter(outline=outline, pk__in=batch).update(
            first_line=True, too_far_away=False
        )
    for i in range(0, len(back_pk), batch_size):
        batch = back_pk[i : i + batch_size]
        models.WeightMaximum.objects.filter(outline=outline, pk__in=batch).update(
            first_line=False, too_far_away=False
        )
    for i in range(0, len(away_pk), batch_size):
        batch = away_pk[i : i + batch_size]
        models.WeightMaximum.objects.filter(outline=outline, pk__in=batch).update(
            first_line=False, too_far_away=True
        )

    outline.available_nobles = [all_noble, front_noble, back_noble, too_far_noble]
    outline.available_offs = [all_off, front_off, back_off, too_far_off]
    outline.available_full_noble_offs = [
        all_full_noble_off,
        front_full_noble_off,
        back_full_noble_off,
        too_far_full_noble_off,
    ]
    outline.available_nobles_near = [
        all_noble_near,
        front_noble_near,
        back_noble_near,
        too_far_noble_near,
    ]
    outline.available_offs_near = [
        all_off_near,
        front_off_near,
        back_off_near,
        too_far_off_near,
    ]
    outline.available_catapults = [
        all_catapults,
        front_catapults,
        back_catapults,
        too_far_catapults,
    ]
    outline.available_ruins = available_ruins
    outline.save(
        update_fields=[
            "available_nobles",
            "available_offs",
            "available_full_noble_offs",
            "available_nobles_near",
            "available_offs_near",
            "available_catapults",
            "available_ruins",
        ]
    )
