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

import datetime
import random
from collections import deque
from math import inf

from base import models
from utils import basic


class FromPeriods:
    def __init__(
        self,
        periods: list[models.PeriodModel],
        world: models.World,
        date: datetime.date,
    ):
        self.date_time: datetime.datetime = datetime.datetime(
            year=date.year, month=date.month, day=date.day
        )
        self.world: models.World = world

        self.nob_period: models.PeriodModel | None = None
        self.ram_period: models.PeriodModel | None = None

        self.nob_periods = deque(
            [period for period in periods if period.unit == "noble"]
        )
        self.ram_periods = deque([period for period in periods if period.unit == "ram"])

        self.attack_numbers_ram = {}
        self.attack_numbers_noble = {}

    def adjust_time(self, weights: list[models.WeightModel]) -> None:
        offs = len(
            [weight for weight in weights if weight.nobleman == 0 and not weight.ruin]
        )
        nobles = len(weights) - offs

        for period in self.ram_periods:
            self.attack_numbers_ram[period] = self.attack_number(period)
        for period in self.nob_periods:
            self.attack_numbers_noble[period] = self.attack_number(period)

        # now change infinity to really whats's left
        left_rams = max(
            offs - sum(n for n in self.attack_numbers_ram.values() if n != inf), 0
        )
        left_nobles = max(
            nobles - sum(n for n in self.attack_numbers_noble.values() if n != inf), 0
        )

        for period in self.ram_periods:
            if self.attack_numbers_ram[period] == inf:
                self.attack_numbers_ram[period] = left_rams
        for period in self.nob_periods:
            if self.attack_numbers_noble[period] == inf:
                self.attack_numbers_noble[period] = left_nobles

    def next(self, weight: models.WeightModel) -> models.WeightModel:
        if weight.nobleman == 0 and not weight.ruin:
            if self.ram_period is None:
                period: models.PeriodModel = self.ram_periods.popleft()
                self.ram_period = period

            result = self.overwrite_weight(self.ram_period, weight)
            self.attack_numbers_ram[self.ram_period] -= 1
            if self.attack_numbers_ram[self.ram_period] <= 0:
                self.ram_period = None

            return result

        if self.nob_period is None:
            period = self.nob_periods.popleft()
            self.nob_period = period
        result = self.overwrite_weight(self.nob_period, weight)

        self.attack_numbers_noble[self.nob_period] -= 1
        if self.attack_numbers_noble[self.nob_period] <= 0:
            self.nob_period = None

        return result

    def attack_number(self, period: models.PeriodModel) -> float:
        n1 = period.from_number
        n2 = period.to_number
        if n2 is None:
            return inf
        if n1 is None:
            return n2
        return random.randint(n1, n2)

    def overwrite_weight(
        self, period: models.PeriodModel, weight: models.WeightModel
    ) -> models.WeightModel:
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
        if weight.ruin:
            desc = "ram"
        elif period.unit == "noble":
            desc = "nobleman"
        else:
            desc = "ram"
        time_distance = datetime.timedelta(
            seconds=village1.time_distance(other=village2, unit=desc, world=self.world)
        )
        t1_shipment = t1 - time_distance
        t2_shipment = t2 - time_distance
        weight.t1 = t1
        weight.t2 = t2
        weight.sh_t1 = t1_shipment
        weight.sh_t2 = t2_shipment
        return weight
