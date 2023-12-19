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

from functools import cached_property
from typing import Literal

from django.db.models.aggregates import Count
from django.db.models.query import QuerySet

from base.models import Outline
from base.models import TargetVertex as Target
from utils.basic.mode import TargetMode


class CalcultateDuplicates:
    def __init__(self, outline: Outline, target_mode: TargetMode) -> None:
        self.outline: Outline = outline
        self.target_mode: TargetMode = target_mode
        self.all_targets = Target.objects.filter(outline=outline)

    def _real_targets(self):
        return self.all_targets.filter(fake=False, ruin=False)

    def _fake_targets(self):
        return self.all_targets.filter(fake=True, ruin=False)

    def _ruin_targets(self):
        return self.all_targets.filter(fake=False, ruin=True)

    def actual_targets(self):
        if self.target_mode.is_real:
            return self._real_targets().order_by("pk")
        elif self.target_mode.is_fake:
            return self._fake_targets().order_by("pk")
        else:
            return self._ruin_targets().order_by("pk")

    @cached_property
    def len_real(self) -> int:
        return self._real_targets().count()

    @cached_property
    def len_fake(self) -> int:
        return self._fake_targets().count()

    @cached_property
    def len_ruin(self) -> int:
        return self._ruin_targets().count()

    @cached_property
    def actual_len(self):
        if self.target_mode.is_real:
            return self.len_real
        elif self.target_mode.is_fake:
            return self.len_fake
        else:
            return self.len_ruin

    @staticmethod
    def _targets_duplicates(
        queryset: QuerySet[Target],
    ) -> list[dict[Literal["target", "duplicate", "lines"], int | str]]:
        """
        Example result:
        ===============

        [
            {"target": "500|500", duplicate: 2, lines: "2,3"},
            {"target": "500|501", duplicate: 4, lines: "5,6,7..."}
        ]

        """

        targets_context: dict[str, list[str]] = {}
        # example {"500|500": [1, 2, 3]}
        # where 1,2,3 represent line numbers in target input
        result_list: list[dict[Literal["target", "duplicate", "lines"], int | str]] = []

        for i, coord in enumerate(
            queryset.order_by("pk").values_list("target", flat=True)
        ):
            if coord in targets_context:
                if len(targets_context[coord]) < 4:
                    targets_context[coord].append(str(i + 1))
            else:
                targets_context[coord] = [str(i + 1)]

        duplicates = (
            queryset.values("target")
            .annotate(duplicate=Count("target"))
            .filter(duplicate__gt=1)
            .values("target", "duplicate")
        )

        target_dict: dict[str, str]
        for target_dict in duplicates.iterator():
            line_lst: list[str] = targets_context[target_dict["target"]]
            if len(line_lst) <= 3:
                lines: str = ",".join(line_lst)
            else:
                lines = ",".join(line_lst[:3]) + ",..."
            result_list.append(
                {
                    "target": target_dict["target"],
                    "duplicate": target_dict["duplicate"],
                    "lines": lines,
                }
            )

        return result_list

    def real_duplicates(self):
        return self._targets_duplicates(self._real_targets())

    def fake_duplicates(self):
        return self._targets_duplicates(self._fake_targets())

    def ruin_duplicates(self):
        return self._targets_duplicates(self._ruin_targets())
