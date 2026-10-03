# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from secrets import SystemRandom

from django.db.models import ExpressionWrapper, F, FloatField
from django.test import TestCase
from django.utils.translation import activate

from base.models import Outline, WeightMaximum
from base.models import TargetVertex as Target
from base.models.target_vertex import TargetVertex
from base.tests.test_utils.initial_setup import create_initial_data_write_outline
from base.tests.test_utils.mini_setup import MiniSetup
from utils.basic.ruin import RuinHandle
from utils.buildings import BUILDING
from utils.fast_weight_maximum import FastWeightMaximum
from utils.outline_initial import MakeOutline
from utils.write_ram_target import WriteRamTarget


class TestWriteRamTargetNew(MiniSetup):
    def test_regular_off_prefers_catapult_sources_for_ruin_target(self):
        random = SystemRandom("test_write_ram")
        outline = self.get_outline(test_world=True)
        outline.initial_outline_min_off = 1000
        outline.initial_outline_max_off = 2000
        outline.initial_outline_maximum_off_dist = 100
        self.create_target_on_test_world(outline=outline)
        target = Target.objects.get(target="200|200")
        target.ruin = True
        target.required_off = 2
        target.mode_off = "closest"
        target.save()

        weight_max_list = []
        for index, (start, catapults, distance) in enumerate(
            [("110|110", 0, 1), ("111|111", 55, 10), ("112|112", 500, 20)]
        ):
            real_weight_max = self.create_weight_maximum(outline=outline, start=start)
            weight_max = FastWeightMaximum(real_weight_max, index, outline)
            weight_max.off_left = 1500
            weight_max.catapult_left = catapults
            weight_max.distance = distance
            weight_max_list.append(weight_max)

        write_ram = WriteRamTarget(
            target=target,
            outline=outline,
            weight_max_list=weight_max_list,
            random=random,
        )

        created = write_ram.weight_create_list()

        assert [weight.start for weight in created] == ["112|112", "111|111"]
        assert all(weight.catapult > 0 for weight in created)

    def test_regular_off_skips_sources_below_configured_catapult_minimum(self):
        random = SystemRandom("test_write_ram")
        outline = self.get_outline(test_world=True)
        outline.initial_outline_min_off = 1000
        outline.initial_outline_max_off = 2000
        outline.initial_outline_maximum_off_dist = 100
        outline.initial_outline_catapult_min_value = 25
        self.create_target_on_test_world(outline=outline)
        target = Target.objects.get(target="200|200")
        target.ruin = True
        target.required_off = 1
        target.mode_off = "closest"
        target.save()

        real_weight_max = self.create_weight_maximum(outline=outline)
        weight_max = FastWeightMaximum(real_weight_max, 0, outline)
        weight_max.off_left = 1500
        weight_max.catapult_left = 5
        weight_max.distance = 1

        write_ram = WriteRamTarget(
            target=target,
            outline=outline,
            weight_max_list=[weight_max],
            random=random,
        )

        created = write_ram.weight_create_list()

        assert created == []
        assert weight_max.catapult_left == 5

    def test_ruin_handle_assigns_larger_force_to_higher_building_level(self):
        outline = self.get_outline(test_world=True)
        weight_maximum = self.create_weight_maximum(outline=outline)
        small_force = FastWeightMaximum(weight_maximum, 0, outline)
        large_force = FastWeightMaximum(weight_maximum, 1, outline)
        small_force.catapult_left = 55
        large_force.catapult_left = 500

        ruin_handle = RuinHandle(outline, target_points=9000)
        ruin_handle.current_building = BUILDING.FARM.value
        ruin_handle.current_level = 30
        ruin_handle.building_is_not_set = False

        planned = ruin_handle.plan_catapults(
            [small_force, large_force], minimum_catapults=25
        )

        assert planned[0] == (large_force, 500, BUILDING.FARM.value)
        assert planned[1] == (small_force, 55, BUILDING.FARM.value)
        assert ruin_handle.current_level == 13

    def test_ruin_handle_infers_building_levels_from_target_points(self):
        outline = self.get_outline(test_world=True)
        outline.initial_outline_buildings = [BUILDING.FARM.value]
        self.create_target_on_test_world(outline=outline)
        target = Target.objects.get(target="200|200")
        target.ruin = True
        target.save()
        weight_maximum = self.create_weight_maximum(outline=outline)

        levels_by_points = {}
        for target_points in (8000, 8001):
            target.points = target_points
            target.save()
            target = Target.objects.get(pk=target.pk)
            ruin_handle = target.ruin_handle(outline)
            assert ruin_handle is not None

            weight_max = FastWeightMaximum(weight_maximum, 0, outline)
            weight_max.catapult_left = 1000
            planned = ruin_handle.plan_catapults([weight_max], minimum_catapults=25)
            levels_by_points[target_points] = (
                planned[0][1],
                ruin_handle.current_level,
                ruin_handle.building_is_not_set,
            )

        assert levels_by_points[8000] == (1000, 25, True)
        assert levels_by_points[8001] == (1000, 5, False)

    def test_ruin_handle_caps_exactly_at_catapults_needed_for_level_zero(self):
        outline = self.get_outline(test_world=True)
        weight_maximum = self.create_weight_maximum(outline=outline)
        weight_max = FastWeightMaximum(weight_maximum, 0, outline)
        weight_max.catapult_left = 100

        ruin_handle = RuinHandle(outline, target_points=5000)
        ruin_handle.current_building = BUILDING.WORKSHOP.value
        ruin_handle.current_level = 5
        ruin_handle.building_is_not_set = False

        planned = ruin_handle.plan_catapults([weight_max], minimum_catapults=1)

        assert planned == [(weight_max, 100, BUILDING.WORKSHOP.value)]
        assert ruin_handle.building_is_not_set

    def test_ruin_handle_sends_minimum_when_it_exceeds_exact_destruction_count(self):
        outline = self.get_outline(test_world=True)
        weight_maximum = self.create_weight_maximum(outline=outline)
        weight_max = FastWeightMaximum(weight_maximum, 0, outline)
        weight_max.catapult_left = 100

        ruin_handle = RuinHandle(outline, target_points=5000)
        ruin_handle.current_building = BUILDING.WORKSHOP.value
        ruin_handle.current_level = 5
        ruin_handle.building_is_not_set = False

        planned = ruin_handle.plan_catapults([weight_max], minimum_catapults=25)

        assert planned == [(weight_max, 100, BUILDING.WORKSHOP.value)]
        assert ruin_handle.building_is_not_set

    def test_ruin_handle_returns_no_attacks_when_no_buildings_remain(self):
        outline = self.get_outline(test_world=True)
        outline.initial_outline_buildings = []
        weight_maximum = self.create_weight_maximum(outline=outline)
        weight_max = FastWeightMaximum(weight_maximum, 0, outline)
        weight_max.catapult_left = 100
        ruin_handle = RuinHandle(outline, target_points=5000)

        assert ruin_handle.plan_catapults([weight_max], minimum_catapults=25) == []

    def test__ruin_query_filter_ruin(self):
        random = SystemRandom("test_write_ram")
        outline = self.get_outline(test_world=True)
        outline.initial_outline_min_off = 9000
        outline.initial_outline_max_off = 13500
        outline.initial_outline_min_ruin_attack_off = 200
        self.create_target_on_test_world(outline=outline)
        target = Target.objects.get(target="200|200")
        real_weight_max = self.create_weight_maximum(outline=outline)
        weight_max = FastWeightMaximum(real_weight_max, 0, outline)

        write_ram = WriteRamTarget(
            target=target,
            outline=outline,
            weight_max_list=[weight_max],
            random=random,
        )

        ruin_filter = write_ram._ruin_query(catapults=50)

        weight_max.off_left = 5000
        weight_max.catapult_left = 50
        assert ruin_filter(weight_max)
        weight_max.catapult_left = 49
        assert not ruin_filter(weight_max)
        weight_max.catapult_left = 500
        weight_max.off_left = 4000
        assert not ruin_filter(weight_max)
        weight_max.catapult_left = 500
        weight_max.off_left = 4200
        assert ruin_filter(weight_max)

        ruin_filter = write_ram._ruin_query(catapults=150)

        weight_max.off_left = 5000
        weight_max.catapult_left = 50
        assert not ruin_filter(weight_max)
        weight_max.catapult_left = 49
        assert not ruin_filter(weight_max)
        weight_max.catapult_left = 500
        weight_max.off_left = 4000
        assert not ruin_filter(weight_max)
        weight_max.catapult_left = 500
        weight_max.off_left = 4200
        assert ruin_filter(weight_max)

    def test_ram_filter_casual_attack_block_ratio(self) -> None:
        random = SystemRandom("test_write_ram")
        outline = self.get_outline(test_world=True)
        outline.world.casual_attack_block_ratio = 20
        outline.world.save()
        self.create_target_on_test_world(outline=outline)
        target = Target.objects.get(target="200|200")
        real_weight_max = self.create_weight_maximum(outline=outline)
        weight_max = FastWeightMaximum(real_weight_max, 0, outline)

        write_ram = WriteRamTarget(
            target=target,
            outline=outline,
            weight_max_list=[weight_max],
            random=random,
        )

        filter_casual_attack_block_ratio = write_ram._casual_attack_block_ratio()

        target.points = 100
        weight_max.points = 130
        assert not filter_casual_attack_block_ratio(weight_max)

        weight_max.points = 119
        assert filter_casual_attack_block_ratio(weight_max)

        weight_max.points = 80
        assert not filter_casual_attack_block_ratio(weight_max)

        weight_max.points = 90
        assert filter_casual_attack_block_ratio(weight_max)

        target.player = ""
        target.points = 0
        weight_max.points = 10000
        assert filter_casual_attack_block_ratio(weight_max)


class TestWriteRamTarget(TestCase):
    def setUp(self):
        activate("pl")
        create_initial_data_write_outline()
        self.outline: Outline = Outline.objects.get(id=1)
        make_outline: MakeOutline = MakeOutline(self.outline)
        make_outline()
        self.weight0 = FastWeightMaximum(
            WeightMaximum.objects.get(start="500|500"), 0, self.outline
        )
        self.weight1 = FastWeightMaximum(
            WeightMaximum.objects.get(start="500|501"), 0, self.outline
        )
        self.weight2 = FastWeightMaximum(
            WeightMaximum.objects.get(start="500|502"), 0, self.outline
        )
        self.weight3 = FastWeightMaximum(
            WeightMaximum.objects.get(start="500|503"), 0, self.outline
        )
        self.weight4 = FastWeightMaximum(
            WeightMaximum.objects.get(start="500|504"), 0, self.outline
        )
        self.weight5 = FastWeightMaximum(
            WeightMaximum.objects.get(start="500|505"), 0, self.outline
        )
        self.random = SystemRandom("test_write_target")

    def target(self, coord: str = "500|499") -> TargetVertex:
        target = Target.objects.create(
            outline=self.outline, target=coord, player="player1"
        )
        return target

    def get_weight_max_lst(self, target: TargetVertex) -> list[FastWeightMaximum]:
        coord = target.coord_tuple()
        weights = list(
            WeightMaximum.objects.filter(
                outline=self.outline, too_far_away=False
            ).annotate(
                distance=ExpressionWrapper(
                    ((F("x_coord") - coord[0]) ** 2 + (F("y_coord") - coord[1]) ** 2)
                    ** (1 / 2),
                    output_field=FloatField(max_length=5),
                )
            )
        )
        lst = [FastWeightMaximum(weight, 0, self.outline) for weight in weights]
        for i, weight in enumerate(lst):
            weight.distance = weights[i].distance
        return lst

    def get_write_target(self, target: TargetVertex) -> WriteRamTarget:
        write_noble = WriteRamTarget(
            target=target,
            outline=self.outline,
            weight_max_list=self.get_weight_max_lst(target),
            random=self.random,
        )
        return write_noble

    def test__add_night_bonus_annotations_cases(self):
        cases = [
            ("500|510", 1, 1, 7, 7, 1),
            ("500|515", 1, 1, 7, 7, 3),
            ("500|514", 1, 1, 7, 7, 2),
            ("500|513", 1, 1, 7, 7, 1),
            ("500|563", 1, 1, 7, 7, 3),
            ("500|562", 1, 1, 7, 7, 2),
            ("500|600", 0.5, 0.5, 7, 7, 3),
            ("499|600", 0.5, 0.5, 7, 9, 2),
            ("500|600", 0.5, 0.5, 21, 21, 3),
            ("500|600", 0.5, 0.5, 15, 15, 3),
            ("500|600", 0.5, 0.5, 22, 24, 3),
        ]
        for i, case in enumerate(cases):
            with self.subTest(number=i):
                target = self.target(case[0])
                self.outline.world.speed_world = case[1]
                self.outline.world.speed_units = case[2]
                self.outline.enter_t1 = case[3]
                self.outline.enter_t2 = case[4]
                write_target = self.get_write_target(target)
                write_target._add_night_bonus_annotations(write_target.weight_max_list)
                assert write_target.weight_max_list[0].night_bool == case[5], (
                    f"case {i} {write_target.weight_max_list[0].start}"
                )
