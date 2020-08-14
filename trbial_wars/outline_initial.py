""" File with outline making and getting stuff """
import random
import datetime
from trbial_wars import basic
from collections import deque
from math import inf
from base import models


def make_outline(outline: models.Outline):
    """ Make empty outline """
    village_dict = basic.coord_to_player(outline=outline)
    evidence = basic.world_evidence(outline.world)
    target_info_dict = {}
    for target_info in outline.initial_outline_targets.split("\r\n"):
        target_info = target_info.split(":")
        target_info_dict[target_info[0]] = {
            "off": int(target_info[1]),
            "nob": int(target_info[2]),
        }

    target_vertex_list = []
    off_troops = outline.off_troops.split("\r\n")
    # Target creating
    target_village_dict = basic.coord_to_player_from_string(
        village_coord_list=" ".join(target_info_dict), world=outline.world,
    )
    for target in target_info_dict:
        target_vertex_list.append(
            models.TargetVertex(
                outline_id=outline.id,
                target=target,
                player=target_village_dict[target],
            )
        )

    query1 = models.TargetVertex.objects.filter(outline=outline)
    query2 = models.WeightModel.objects.filter(target__in=query1)
    query2._raw_delete(query2.db)
    query1._raw_delete(query1.db)
    models.TargetVertex.objects.bulk_create(target_vertex_list)
    # Weight max creating
    weight_max_list = []
    for line in off_troops:
        army = basic.Army(text_army=line, evidence=evidence)
        try:
            player = village_dict[army.coord]
        except KeyError:
            raise KeyError()
        if army.off < 500 and army.nobleman == 0:
            continue
        if army.deff > 5000 and army.nobleman == 0:
            continue
        weight_max_list.append(
            models.WeightMaximum(
                outline_id=outline.id,
                player=player,
                start=army.coord,
                off_max=army.off,
                off_left=army.off,
                nobleman_max=army.nobleman,
                nobleman_left=army.nobleman,
            )
        )

    query3 = models.WeightMaximum.objects.filter(outline=outline)
    query3._raw_delete(query3.db)
    models.WeightMaximum.objects.bulk_create(weight_max_list)

    query4 = models.OutlineTime.objects.filter(outline=outline)
    query5 = models.PeriodModel.objects.filter(outline_time__in=query4)

    query5._raw_delete(query5.db)
    query4._raw_delete(query4.db)

    return make_outline_next(target_info_dict, outline)


def make_outline_next(target_info_dict: dict, outline: models.Outline):
    weight_max_list = list(models.WeightMaximum.objects.filter(outline=outline))
    targets = models.TargetVertex.objects.filter(outline=outline)
    weight_create_list = []
    weight_max_update = []
    context_off = {}
    context_nob = {}

    for target in targets:
        context_nob[target] = target_info_dict[target.target]["nob"]
        context_off[target] = target_info_dict[target.target]["off"]

    excluded = set()
    for target in targets:
        actual_list = [weight for weight in weight_max_list if weight not in excluded]
        actual_list.sort(key=lambda weight: basic.dist(weight.start, target.target))

        for weight_max in actual_list:
            required = context_nob[target]
            if required == 0:
                break

            if weight_max.nobleman_max == 0:
                continue

            if weight_max.off_max < 400:
                continue

            if weight_max.nobleman_max > required:
                nob = required

            else:
                nob = weight_max.nobleman_max

            army = weight_max.off_max // nob
            for i in range(len(excluded)*50+50, len(excluded)*50+50 + nob):
                weight_create_list.append(
                    models.WeightModel(
                        target=target,
                        player=weight_max.player,
                        start=weight_max.start,
                        state=weight_max,
                        off=army,
                        distance=basic.dist(weight_max.start, target.target),
                        nobleman=1,
                        order=i,
                    )
                )
            excluded.add(weight_max)
            context_nob[target] -= nob
            weight_max.nobleman_left = weight_max.nobleman_max - nob
            weight_max.nobleman_state = nob
            weight_max.off_state = weight_max.off_max
            weight_max.off_left = 0
            weight_max_update.append(weight_max)


    random.shuffle(weight_max_list)
    for weight in weight_max_list:
        if weight.off_max < 19000 and weight.nobleman_max == 0:
            continue

        off = weight.off_max
        if off > 19000 and len(context_off) != 0:
            min_off_target = min(
                context_off, key=lambda target: basic.dist(weight.start, target.target)
            )
            required = context_off[min_off_target]
            army = weight.off_max
            weight_create_list.append(
                models.WeightModel(
                    target=min_off_target,
                    player=weight.player,
                    start=weight.start,
                    state=weight,
                    off=army,
                    distance=basic.dist(weight.start, min_off_target.target),
                    nobleman=0,
                    order=required,
                )
            )
            context_off[min_off_target] -= 1
            if context_off[min_off_target] == 0:
                del context_off[min_off_target]
            weight.off_state = weight.off_max
            weight.off_left = 0
            weight_max_update.append(weight)
            continue
        continue

    models.WeightModel.objects.bulk_create(weight_create_list)
    models.WeightMaximum.objects.bulk_update(
        weight_max_update, ["nobleman_left", "nobleman_state", "off_left", "off_state"]
    )


class FromPeriods:
    def __init__(self, periods: list(), world: models.World, date: datetime.date):
        self.date_time = datetime.datetime(year=date.year, month=date.month, day=date.day)
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
        if weight.nobleman == 0:
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

    def overwrite_weight(self, period: models.PeriodModel, weight: models.WeightModel):

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
            unit = "nobleman"
        else:
            unit = "ram"
        time_distance = datetime.timedelta(
            seconds=village1.time_distance(other=village2, unit=unit, world=self.world)
        )
        t1_shipment = t1 - time_distance
        t2_shipment = t2 - time_distance
        weight.t1 = t1
        weight.t2 = t2
        weight.sh_t1 = t1_shipment
        weight.sh_t2 = t1_shipment
        return weight


@basic.timing
def make_final_outline(outline: models.Outline):
    village_dict = basic.coord_to_player(outline=outline)
    evidence = basic.world_evidence(outline.world)

    context_with_target_id = {}
    context_with_target_weight = {}
    context_with_target_period = {}
    context_with_time_period = {}

    targets = models.TargetVertex.objects.select_related("outline_time").filter(
        outline=outline
    )

    for target in targets:
        context_with_target_id[target.id] = target
        context_with_target_weight[target.id] = deque()
        context_with_time_period[target.outline_time.id] = deque()

    periods = (
        models.PeriodModel.objects.select_related("outline_time")
        .filter(outline_time__in=[target.outline_time.id for target in targets])
        .order_by("from_time", "-unit")
    )

    for period in periods:
        context_with_time_period[period.outline_time.id].append(period)

    for target in targets:
        context_with_target_period[target.id] = context_with_time_period[
            target.outline_time.id
        ]

    weights = models.WeightModel.objects.select_related("target").filter(
        target__in=targets
    )
    villages_id = set()
    for weight in weights:
        villages_id.add(f'{weight.target.target[0:3]}{weight.target.target[4:7]}{outline.world}')
        villages_id.add(f'{weight.start[0:3]}{weight.start[4:7]}{outline.world}')
        context_with_target_weight[weight.target.id].append(weight)
    world_model = models.World.objects.get(world=outline.world)

    village_id = {}
    result_dictionary = {}

    for village in models.VillageModel.objects.filter(id__in=villages_id):
        village_id[f'{village.x_coord}|{village.y_coord}'] = village.village_id


    for target_id, lst in context_with_target_weight.items():
        periods_list = list(context_with_target_period[target_id])
        from_period = FromPeriods(periods=periods_list, world=world_model, date=outline.date)
        for weight in lst:
            if weight.nobleman > 0:
                unit = 'noble'
            else:
                unit = 'ram'
            
            weight = from_period.next(weight=weight)
            link = f'https://pl{outline.world}.plemiona.pl/game.php?village={village_id[weight.start]}&screen=place&target={village_id[weight.target.target]}'
            try:
                result_dictionary[
                    village_dict[weight.start]
                ] += f'[*][url={link}]Link[/url][|][coord]{weight.start}[/coord][|][coord]{weight.target.target}[/coord][|]{unit}[|]{weight.off}[|]{weight.nobleman}[|]{weight.sh_t1}[|]{weight.sh_t2}[|]{weight.t1}[|]{weight.t2}'
            except KeyError:
                result_dictionary[
                    village_dict[weight.start]
                ] = f'[*][url={link}]Link[/url][|][coord]{weight.start}[/coord][|][coord]{weight.target.target}[/coord][|]{unit}[|]{weight.off}[|]{weight.nobleman}[|]{weight.sh_t1}[|]{weight.sh_t2}[|]{weight.t1}[|]{weight.t2}'
    
    prefix = '[table][**]LINK[||]Z WIOSKI[||]CEL[||]PRĘDKOŚĆ[||]OFF[||]SZLACHTA[||]MIN WYSYŁKA[||]MAX WYSYŁKA[||]MIN WEJŚCIE[||]MAX WEJŚCIE[/**]'
    postfix = '[/table]'
    result = ''
    for i, j in result_dictionary.items():
        j = prefix + j + postfix
        result += '\r\n\r\n'+i+'\r\n'+j
    res = outline.result
    res.results_outline = result
    res.save()



