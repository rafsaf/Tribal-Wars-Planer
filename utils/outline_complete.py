from typing import Generator, List, Tuple
from django.db.models.query import QuerySet
from base import models
from utils.write_ram_target import WriteRamTarget
from utils.write_noble_target import WriteNobleTarget
from base.models import TargetVertex as Target, Outline, WeightModel


def complete_outline_write(outline: models.Outline):
    """
    Auto write out given outline
    1. Fake Rams
    2. Ruins
    3. Nobles
    4. Offs & Ruin offs
    5. Fake Nobles

    For every queryset, forLoop over its targets and
    in each step writting the step's target
    """

    targets = models.TargetVertex.objects.filter(
        outline=outline, fake=False, ruin=False
    ).order_by("id")
    fakes = models.TargetVertex.objects.filter(
        outline=outline, fake=True, ruin=False
    ).order_by("id")
    ruins = models.TargetVertex.objects.filter(
        outline=outline, fake=False, ruin=True
    ).order_by("id")

    create_fakes = CreateWeights(fakes, outline, noble=False, ruin=False)
    create_fakes()

    create_ruins = CreateWeights(ruins, outline, noble=False, ruin=True)
    create_ruins()

    create_nobles = CreateWeights(targets, outline, noble=True, ruin=False)
    create_nobles()

    create_offs = CreateWeights(targets, outline, noble=False, ruin=False)
    create_offs()

    create_ruin_offs = CreateWeights(ruins, outline, noble=False, ruin=False)
    create_ruin_offs()

    create_fake_nobles = CreateWeights(fakes, outline, noble=True, ruin=False)
    create_fake_nobles()


class CreateWeights:
    def __init__(
        self,
        targets: "QuerySet[Target]",
        outline: Outline,
        noble: bool = False,
        ruin: bool = False,
    ) -> None:
        self.targets: "QuerySet[Target]" = targets
        self.outline: Outline = outline
        self.noble: bool = noble
        self.ruin: bool = ruin
        self.modes_list = ["closest", "close", "random", "far"]
        self.weight_create_lst: List[WeightModel] = []

    @staticmethod
    def _is_syntax_extended(target: Target, noble_or_ruin: bool = False) -> bool:
        if noble_or_ruin:
            if len(target.exact_noble) == 4:
                return True
            return False
        if len(target.exact_off) == 4:
            return True
        return False

    def _extended_syntax(
        self, target: Target, noble_or_ruin: bool = False
    ) -> Generator[Tuple[int, str], None, None]:
        # closest, close, random, far

        if noble_or_ruin:
            iterator = zip(target.exact_noble, self.modes_list)
        else:
            iterator = zip(target.exact_off, self.modes_list)
        required: int
        for required, mode in iterator:
            yield (required, mode)

    def _create_weights_or_pass(self, weight_lst: List[WeightModel]) -> None:
        # note that we hit database only when have a lot of data

        weight: WeightModel
        for weight in weight_lst:
            self.weight_create_lst.append(weight)

        if len(self.weight_create_lst) >= 500:
            WeightModel.objects.bulk_create(self.weight_create_lst)
            self.weight_create_lst = []

    def _noble_write(self, target: Target) -> None:
        if self._is_syntax_extended(target, noble_or_ruin=True):
            for (required, mode) in self._extended_syntax(target, noble_or_ruin=True):
                if required == 0:
                    continue
                target.required_noble = required
                target.mode_noble = mode
                weight_noble: WriteNobleTarget = WriteNobleTarget(
                    target=target,
                    outline=self.outline,
                )
                self._create_weights_or_pass(weight_noble.weight_create_list())

        else:
            if target.required_noble > 0:
                weight_noble: WriteNobleTarget = WriteNobleTarget(
                    target=target,
                    outline=self.outline,
                )
                self._create_weights_or_pass(weight_noble.weight_create_list())

    def _ruin_write(self, target: Target) -> None:
        if self._is_syntax_extended(target, noble_or_ruin=True):
            for (required, mode) in self._extended_syntax(target, noble_or_ruin=True):
                if required == 0:
                    continue
                target.required_off = required
                target.mode_off = mode
                weight_ram: WriteRamTarget = WriteRamTarget(
                    target=target,
                    outline=self.outline,
                    ruin=True,
                )
                self._create_weights_or_pass(weight_ram.weight_create_list())

        else:
            target.required_off = target.required_noble
            if target.required_off > 0:
                weight_ram: WriteRamTarget = WriteRamTarget(
                    target=target,
                    outline=self.outline,
                    ruin=True,
                )
                self._create_weights_or_pass(weight_ram.weight_create_list())

    def _ram_write(self, target: Target) -> None:
        if self._is_syntax_extended(target, noble_or_ruin=False):
            for (required, mode) in self._extended_syntax(target, noble_or_ruin=False):
                if required == 0:
                    continue
                target.required_off = required
                target.mode_off = mode
                weight_ram: WriteRamTarget = WriteRamTarget(
                    target=target,
                    outline=self.outline,
                    ruin=False,
                )
                self._create_weights_or_pass(weight_ram.weight_create_list())

        else:
            if target.required_off > 0:
                weight_ram: WriteRamTarget = WriteRamTarget(
                    target=target,
                    outline=self.outline,
                    ruin=False,
                )
                self._create_weights_or_pass(weight_ram.weight_create_list())

    def __call__(self) -> None:
        # note that .iterator() prevents from caching querysets
        # which can possibly cause overwriting some targets attributes

        target: Target
        for target in self.targets.iterator():
            if self.noble:
                self._noble_write(target)
            elif self.ruin:
                self._ruin_write(target)
            else:
                self._ram_write(target)
        WeightModel.objects.bulk_create(self.weight_create_lst)
