from collections import defaultdict

from django.db.models.query import QuerySet

from base.models import Outline, Player
from base.models import TargetVertex as Target
from base.models import WeightMaximum


def _return_100():
    return 100


class UpdateOutlineDataError(Exception):
    pass


def generate_morale_dict(outline: Outline) -> defaultdict[tuple[str, str], int]:
    """
    For given outline function returns defaultdict where keys are
    tuples (DEFENDER NICK, ATACKER NICK) and values are morale between 25 and 100
    (for an attacker attacking defender)

    Defaults to 100 morale for example where some players are missing or when
    they have 0 points.
    """
    target_players_queryset: QuerySet["Target"] = (
        Target.objects.filter(outline=outline).order_by("player").distinct("player")
    )
    unique_target_players = [target.player for target in target_players_queryset]
    weight_max_players_queryset: QuerySet["WeightMaximum"] = (
        WeightMaximum.objects.filter(outline=outline)
        .order_by("player")
        .distinct("player")
    )
    print(weight_max_players_queryset)
    unique_weight_max_players = [
        weight.player for weight in weight_max_players_queryset
    ]
    dict_player_to_points: dict[str, int] = {}

    dict_player_tuple_to_morale: defaultdict[tuple[str, str], int] = defaultdict(
        _return_100
    )
    player: Player
    for player in Player.objects.filter(
        name__in=unique_target_players + unique_weight_max_players, world=outline.world
    ):
        dict_player_to_points[player.name] = player.points
    print(dict_player_to_points)
    for target_player in unique_target_players:
        try:
            target_player_points = dict_player_to_points[target_player]
        except KeyError:
            raise UpdateOutlineDataError
        for weight_player in unique_weight_max_players:
            try:
                weight_player_points = dict_player_to_points[weight_player]
            except KeyError:
                raise UpdateOutlineDataError
            if weight_player_points == 0:
                continue
            morale = round(
                ((3 * target_player_points / weight_player_points) + 0.3) * 100
            )
            if morale >= 100:
                continue
            elif morale < 25:
                morale = 25
            dict_player_tuple_to_morale[(target_player, weight_player)] = morale
    return dict_player_tuple_to_morale
