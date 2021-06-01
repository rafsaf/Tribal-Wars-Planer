from functools import cached_property
from typing import Dict, List

from django.db.models.aggregates import Count
from django.db.models.query import QuerySet

from base.models import Outline
from base.models import TargetVertex as Target

from utils.basic.mode import TargetMode


class CalcultateDuplicates:
    def __init__(self, outline: Outline, target_mode: TargetMode) -> None:
        self.outline: Outline = outline
        self.target_mode: TargetMode = target_mode
        self.all_targets: "QuerySet[Target]" = Target.objects.filter(outline=outline)

    def _real_targets(self) -> "QuerySet[Target]":
        return self.all_targets.filter(fake=False, ruin=False)

    def _fake_targets(self) -> "QuerySet[Target]":
        return self.all_targets.filter(fake=True, ruin=False)

    def _ruin_targets(self) -> "QuerySet[Target]":
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
    def _targets_duplicates(queryset: "QuerySet[Target]"):
        targets_context: Dict[str, List[str]] = {}

        for i, target in enumerate(queryset.order_by("pk").values("target").iterator()):
            if target["target"] in targets_context:
                targets_context[target["target"]].append(str(i + 1))
            else:
                targets_context[target["target"]] = [str(i + 1)]

        duplicates = (
            queryset.values("target")
            .annotate(duplicate=Count("target"))
            .filter(duplicate__gt=1)
            .values("target", "duplicate")
        )

        target_dict: Dict[str, str]
        for target_dict in duplicates:
            line_lst: List[str] = targets_context[target_dict["target"]]
            if len(line_lst) <= 3:
                target_dict["lines"] = ",".join(line_lst)
            else:
                target_dict["lines"] = ",".join(line_lst[:3]) + ",..."

        return duplicates

    def real_duplicates(self):
        return self._targets_duplicates(self._real_targets())

    def fake_duplicates(self):
        return self._targets_duplicates(self._fake_targets())

    def ruin_duplicates(self):
        return self._targets_duplicates(self._ruin_targets())
