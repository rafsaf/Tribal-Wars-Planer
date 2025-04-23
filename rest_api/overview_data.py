import json

from django.core.cache import cache

from base.models.outline_overview import OutlineOverview
from rest_api import serializers


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

    query = []
    targets = json.loads(outline_overview.targets_json)
    weights = json.loads(outline_overview.weights_json)

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
            "outline": outline_overview.outline_json,
            "world": outline_overview.world_json,
            "targets": query,
        }
    )
    cache.set(cache_key, output, 60 * 60 * 12)  # 12 hours
    return output
