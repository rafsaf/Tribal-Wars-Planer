# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

"""Basic"""

from .army import Army, ArmyError, Defence, DefenceError, world_evidence  # noqa
from .target_calculations import TargetsCalculations  # noqa
from .create_test_world import create_test_world  # noqa
from .dictionary import coord_to_player  # noqa
from .draw_table import draw_table  # noqa
from .encode_component import encode_component  # noqa
from .info_generatation import OutlineInfo, TargetCount  # noqa
from .mode import Mode, TargetMode  # noqa
from .morale import generate_morale_dict  # noqa
from .off_text import (
    DeffException,  # noqa
    NewDeffText,  # noqa
    NewOffsText,  # noqa
    UserDeffInfo,  # noqa
    VillageDeffInfo,  # noqa
)
from .outline_stats import Action, action  # noqa
from .period_utils import FromPeriods  # noqa
from .request_info import is_android_tw_app_webview  # noqa
from .sort_detail_view import SortAndPaginRequest  # noqa
from .table_text import TableText  # noqa
from .target_line import TargetsData, TargetsOneLine  # noqa
from .timer import timing  # noqa
from .troops import Troops  # noqa
from .village import Unit, Village, VillageError, dist, many_villages  # noqa
