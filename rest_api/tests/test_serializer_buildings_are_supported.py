from base.models import Outline, WeightModel
from rest_api.serializers import BUILDINGS
from utils.basic.ruin import RuinHandle


def test_buildings_from_serializer_match_from_ruin_and_models():
    assert BUILDINGS == set(RuinHandle.BIG_LEVELS.keys())
    assert BUILDINGS == set(RuinHandle.SMALL_LEVELS.keys())
    assert BUILDINGS == set(building[0] for building in WeightModel.BUILDINGS)
    assert BUILDINGS == set(building[0] for building in Outline.BUILDINGS)
