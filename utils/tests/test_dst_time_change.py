# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import datetime
import zoneinfo
from types import SimpleNamespace

import pytest

from utils.basic.period_utils import FromPeriods
from utils.basic.table_text import TableText
from utils.outline_finish import MakeFinalOutline

WARSAW = zoneinfo.ZoneInfo("Europe/Warsaw")
LONDON = zoneinfo.ZoneInfo("Europe/London")
UTC = datetime.UTC

# ram: 30 min per field, world and unit speed 1
RAM_SECONDS_PER_FIELD = 30 * 60


def make_world(tz: zoneinfo.ZoneInfo) -> SimpleNamespace:
    return SimpleNamespace(
        server=SimpleNamespace(tz=tz), speed_world=1.0, speed_units=1.0
    )


def make_weight(fields: int, start: str = "500|500") -> SimpleNamespace:
    x, y = start.split("|")
    return SimpleNamespace(
        start=start,
        target=SimpleNamespace(target=f"{x}|{int(y) + fields}"),
        ruin=False,
        nobleman=0,
        order=0,
    )


def write_times(
    tz: zoneinfo.ZoneInfo,
    date: datetime.date,
    from_time: datetime.time,
    to_time: datetime.time,
    fields: int,
) -> SimpleNamespace:
    period = SimpleNamespace(from_time=from_time, to_time=to_time, unit="ram")
    from_periods = FromPeriods(periods=[], world=make_world(tz), date=date)  # type: ignore
    return from_periods.overwrite_weight(period, make_weight(fields))  # type: ignore


@pytest.mark.parametrize(
    "tz,date,arrival,fields,expected_shipment",
    [
        # normal winter day
        (
            WARSAW,
            datetime.date(2026, 1, 15),
            datetime.time(4, 0),
            6,
            datetime.datetime(2026, 1, 15, 1, 0, tzinfo=WARSAW),
        ),
        # winter -> summer (02:00 CET jumps to 03:00 CEST), 3h travel over the gap
        (
            WARSAW,
            datetime.date(2026, 3, 29),
            datetime.time(4, 0),
            6,
            datetime.datetime(2026, 3, 29, 0, 0, tzinfo=WARSAW),
        ),
        # winter -> summer, shipment day before the change
        (
            WARSAW,
            datetime.date(2026, 3, 29),
            datetime.time(8, 0),
            20,
            datetime.datetime(2026, 3, 28, 21, 0, tzinfo=WARSAW),
        ),
        # summer -> winter (03:00 CEST goes back to 02:00 CET), 3h travel over the change
        (
            WARSAW,
            datetime.date(2026, 10, 25),
            datetime.time(4, 0),
            6,
            datetime.datetime(2026, 10, 25, 2, 0, tzinfo=WARSAW),
        ),
        # summer -> winter, shipment lands in second (CET) occurrence of 02:xx
        (
            WARSAW,
            datetime.date(2026, 10, 25),
            datetime.time(3, 30),
            2,
            datetime.datetime(2026, 10, 25, 2, 30, fold=1, tzinfo=WARSAW),
        ),
        # summer -> winter, shipment lands in first (CEST) occurrence of 02:xx
        (
            WARSAW,
            datetime.date(2026, 10, 25),
            datetime.time(3, 30),
            4,
            datetime.datetime(2026, 10, 25, 2, 30, fold=0, tzinfo=WARSAW),
        ),
        # other server timezone, UK change at 01:00 GMT
        (
            LONDON,
            datetime.date(2026, 3, 29),
            datetime.time(3, 0),
            6,
            datetime.datetime(2026, 3, 28, 23, 0, tzinfo=LONDON),
        ),
        (
            LONDON,
            datetime.date(2026, 10, 25),
            datetime.time(3, 0),
            6,
            datetime.datetime(2026, 10, 25, 1, 0, fold=0, tzinfo=LONDON),
        ),
    ],
)
def test_shipment_time_respects_dst_change(
    tz: zoneinfo.ZoneInfo,
    date: datetime.date,
    arrival: datetime.time,
    fields: int,
    expected_shipment: datetime.datetime,
):
    weight = write_times(tz, date, arrival, arrival, fields)
    travel = fields * RAM_SECONDS_PER_FIELD

    assert weight.t1 == datetime.datetime.combine(date, arrival, tzinfo=tz)
    assert weight.t1.timestamp() - weight.sh_t1.timestamp() == travel
    assert weight.sh_t1.astimezone(UTC) == expected_shipment.astimezone(UTC)
    # wall clock (what is shown to players) and fold must match too
    assert weight.sh_t1.replace(tzinfo=None) == expected_shipment.replace(tzinfo=None)
    assert weight.sh_t1.fold == expected_shipment.fold
    assert weight.sh_t1.utcoffset() == expected_shipment.utcoffset()


def test_shipment_window_keeps_length_when_crossing_dst():
    # arrival 03:30-05:00 CEST on change day, 2h travel -> window crosses the gap
    weight = write_times(
        WARSAW,
        datetime.date(2026, 3, 29),
        datetime.time(3, 30),
        datetime.time(5, 0),
        4,
    )
    assert weight.sh_t2.timestamp() - weight.sh_t1.timestamp() == 90 * 60
    assert weight.sh_t1 == datetime.datetime(2026, 3, 29, 0, 30, tzinfo=WARSAW)
    assert weight.sh_t2 == datetime.datetime(2026, 3, 29, 3, 0, tzinfo=WARSAW)


@pytest.mark.parametrize(
    "date,arrival,fields",
    [
        (datetime.date(2026, 1, 15), datetime.time(4, 0), 6),
        (datetime.date(2026, 3, 29), datetime.time(4, 0), 6),
        (datetime.date(2026, 10, 25), datetime.time(4, 0), 6),
        (datetime.date(2026, 10, 25), datetime.time(3, 30), 2),
        (datetime.date(2026, 3, 29), datetime.time(8, 0), 100),
    ],
)
def test_json_time_seconds_is_real_travel_time(
    date: datetime.date, arrival: datetime.time, fields: int
):
    weight = write_times(WARSAW, date, arrival, arrival, fields)
    weight.pk = 1
    weight.player = "player"
    weight.off = 100
    weight.catapult = 0
    weight.distance = float(fields)
    weight.building = None
    weight.village_id = 1
    weight.player_id = 1

    make_final = MakeFinalOutline.__new__(MakeFinalOutline)
    make_final.game_url = "https://example.test"
    target = SimpleNamespace(fake=False, village_id=2, player_id=2)

    result = make_final._json_weight(weight, target)  # type: ignore

    assert result["time_seconds"] == fields * RAM_SECONDS_PER_FIELD


def test_table_text_sorts_by_real_shipment_time_in_repeated_hour():
    # 02:40 CEST happens before 02:10 CET on 2026-10-25
    first = SimpleNamespace(
        start="500|500",
        sh_t1=datetime.datetime(2026, 10, 25, 2, 40, fold=0, tzinfo=WARSAW),
        nobleman=0,
        order=1,
        target=SimpleNamespace(target="500|510"),
    )
    second = SimpleNamespace(
        start="500|500",
        sh_t1=datetime.datetime(2026, 10, 25, 2, 10, fold=1, tzinfo=WARSAW),
        nobleman=0,
        order=0,
        target=SimpleNamespace(target="500|511"),
    )
    assert first.sh_t1.timestamp() < second.sh_t1.timestamp()

    text = TableText(outline=SimpleNamespace(world=None))  # type: ignore
    text.create_weights([second, first])  # type: ignore

    assert text.weights["500|500"] == [first, second]
