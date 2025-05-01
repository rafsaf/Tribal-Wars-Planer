import json
import logging
from collections import defaultdict

from django.core.cache import cache

from base.models.outline_overview import OutlineOverview
from rest_api import serializers

log = logging.getLogger(__name__)


def get_overview_data(
    outline_overview_pk: int,
    show_hidden: bool,
    player: str,
    language: str,
    version: int,
) -> serializers.OverviewSerializer:
    cache_key = f"fn:get_overview_data:{outline_overview_pk}_{show_hidden}_{player}_{language}_{version}"
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return cached_data

    outline_overview = OutlineOverview.objects.defer("outline").get(
        pk=outline_overview_pk
    )

    output = output_data(
        targets=json.loads(outline_overview.targets_json),
        weights=json.loads(outline_overview.weights_json),
        outline=outline_overview.outline_json,
        world=outline_overview.world_json,
        show_hidden=show_hidden,
        player=player,
    )

    cache.set(cache_key, output, 60 * 60 * 12)  # 12 hours
    return output


def get_overview_data_many(
    outline_overview_pk_lst: list[int],
    show_hidden: bool,
    player: str,
    language: str,
    version: int,
) -> serializers.OverviewSerializer:
    cache_key = f"fn:get_overview_data_many:{outline_overview_pk_lst}_{show_hidden}_{player}_{language}_{version}"
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        log.info("cache hit for %s", cache_key)
        return cached_data

    log.debug("calculate response for %s", outline_overview_pk_lst)
    outline_overviews = OutlineOverview.objects.defer("outline").filter(
        pk__in=outline_overview_pk_lst
    )

    if not outline_overviews:
        raise ValueError("empty overview list")

    all_targets = json.loads(outline_overviews[0].targets_json)
    all_weights = defaultdict(list)

    for outline_overview in outline_overviews:
        all_targets |= json.loads(outline_overview.targets_json)

        weights = json.loads(outline_overview.weights_json)

        for target_id, weight_lst in weights.items():
            all_weights[target_id] += weight_lst

    output = output_data(
        targets=all_targets,
        weights=all_weights,
        outline=outline_overview.outline_json,
        world=outline_overview.world_json,
        show_hidden=show_hidden,
        player=player,
    )

    cache.set(cache_key, output, 60 * 60 * 12)  # 12 hours
    return output


def output_data(
    targets: dict,
    weights: dict,
    outline: dict,
    world: dict,
    show_hidden: bool,
    player: str,
) -> serializers.OverviewSerializer:
    query = []

    if show_hidden:
        for target, lst in weights.items():
            for weight in lst:
                if weight["player"] == player:
                    query.append(
                        {
                            "target": targets[target],
                            "my_orders": [
                                weight for weight in lst if weight["player"] == player
                            ],
                            "other_orders": [
                                weight for weight in lst if weight["player"] != player
                            ],
                        }
                    )
                    break

    else:
        for target, lst in weights.items():
            owns = [weight for weight in lst if weight["player"] == player]

            if len(owns) > 0:
                alls = False
                for weight in owns:
                    if weight["nobleman"] > 0 and weight["distance"] < 14:
                        alls = True
                        break
                if alls:
                    others = [weight for weight in lst if weight["player"] != player]
                else:
                    others = []

                query.append(
                    {
                        "target": targets[target],
                        "my_orders": owns,
                        "other_orders": others,
                    }
                )
    output = serializers.OverviewSerializer(
        data={
            "outline": outline,
            "world": world,
            "targets": query,
        }
    )

    return output
