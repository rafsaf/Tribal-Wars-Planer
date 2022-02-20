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

""" Basic """

from .army import Army, ArmyError, Defence, DefenceError, world_evidence
from .calculate_duplicates import CalcultateDuplicates
from .create_test_world import create_test_world
from .dictionary import coord_to_player, coord_to_player_from_string
from .encode_component import encode_component
from .info_generatation import OutlineInfo, TargetCount
from .mode import Mode, TargetMode
from .morale import generate_morale_dict
from .off_text import (
    DeffException,
    NewDeffText,
    NewOffsText,
    UserDeffInfo,
    VillageDeffInfo,
)
from .outline_stats import Action, action
from .period_utils import FromPeriods
from .queries import TargetWeightQueries
from .sort_detail_view import SortAndPaginRequest
from .table_text import TableText
from .target_line import TargetsData, TargetsOneLine
from .timer import timing
from .troops import Troops
from .village import Unit, Village, VillageError, dist, many_villages
