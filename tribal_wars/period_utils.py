import datetime
import random
from collections import deque
from math import inf

from django.utils.translation import gettext

from base import models
from tribal_wars import basic


class FromPeriods:
    def __init__(
        self, periods: list(), world: int, date: datetime.date
    ):
        self.date_time = datetime.datetime(
            year=date.year, month=date.month, day=date.day
        )
        self.world = world
        self.periods = periods
        self.nob_periods = deque(
            [period for period in periods if period.unit == "noble"]
        )
        self.ram_periods = deque(
            [period for period in periods if period.unit == "ram"]
        )
        self.nob_period = None
        self.ram_period = None

    def next(self, weight: models.WeightModel):
        if weight.nobleman == 0 and not weight.ruin:
            if self.ram_period is None:
                period = self.ram_periods.popleft()
                period.attack_number = self.attack_number(period)
                self.ram_period = period

            result = self.overwrite_weight(self.ram_period, weight)
            self.ram_period.attack_number -= 1
            if self.ram_period.attack_number <= 0:
                self.ram_period = None

            return result

        if self.nob_period is None:
            period = self.nob_periods.popleft()
            period.attack_number = self.attack_number(period)
            self.nob_period = period
        result = self.overwrite_weight(self.nob_period, weight)

        self.nob_period.attack_number -= 1
        if self.nob_period.attack_number <= 0:
            self.nob_period = None

        return result

    def attack_number(self, period: models.PeriodModel):
        n1 = period.from_number
        n2 = period.to_number
        if n2 is None:
            return inf
        if n1 is None:
            return n2
        return random.randint(n1, n2)

    def overwrite_weight(
        self, period: models.PeriodModel, weight: models.WeightModel
    ):

        t1 = period.from_time
        t2 = period.to_time
        time_d1 = datetime.timedelta(
            hours=t1.hour, minutes=t1.minute, seconds=t1.second
        )
        time_d2 = datetime.timedelta(
            hours=t2.hour, minutes=t2.minute, seconds=t2.second
        )
        t1 = self.date_time + time_d1
        t2 = self.date_time + time_d2

        village1 = basic.Village(weight.start)
        village2 = basic.Village(weight.target.target)
        if period.unit == "noble":
            unit = gettext("nobleman")
            desc = "nobleman"
        else:
            unit = gettext("ram")
            desc = "ram"
        time_distance = datetime.timedelta(
            seconds=village1.time_distance(
                other=village2, unit=desc, world=self.world
            )
        )
        t1_shipment = t1 - time_distance
        t2_shipment = t2 - time_distance
        weight.t1 = t1
        weight.t2 = t2
        weight.sh_t1 = t1_shipment
        weight.sh_t2 = t2_shipment
        return weight