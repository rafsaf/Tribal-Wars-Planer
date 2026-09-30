# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

"""functions to generate coord-to-player dictionaries"""

from base.models import Outline, Player, VillageModel


def coord_to_player(outline: Outline) -> dict[str, Player]:
    """Dictionary coord : player name for tribes in outline"""
    ally_villages = VillageModel.objects.select_related("player").filter(
        player__tribe__tag__in=outline.ally_tribe_tag, world=outline.world
    )
    village_dictionary: dict[str, Player] = {}
    for village in ally_villages.iterator(chunk_size=10000):
        assert village.player
        village_dictionary[village.coord] = village.player

    return village_dictionary
