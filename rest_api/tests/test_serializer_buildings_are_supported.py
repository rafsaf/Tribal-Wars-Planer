# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from base.models import Outline, WeightModel
from utils.basic.ruin import RuinHandle
from utils.buildings import BUILDING, BUILDINGS_TRANSLATION


def test_buildings_from_serializer_match_from_ruin_and_models():
    assert set(BUILDINGS_TRANSLATION) == set(RuinHandle.BIG_LEVELS.keys())
    assert set(BUILDINGS_TRANSLATION) == set(RuinHandle.SMALL_LEVELS.keys())
    assert set(BUILDINGS_TRANSLATION) == set(
        building[0] for building in WeightModel.BUILDINGS
    )
    assert set(BUILDINGS_TRANSLATION) == set(
        building[0] for building in Outline.BUILDINGS
    )

    for item in BUILDING:
        assert item.value in BUILDINGS_TRANSLATION

    buildings = [item.value for item in BUILDING]
    for item in BUILDINGS_TRANSLATION:
        assert item in buildings
