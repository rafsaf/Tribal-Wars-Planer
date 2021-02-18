import json

from base import models
from tribal_wars import basic
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder


class TargetWeightQueries:
    def __init__(self, outline, ruin=False, fake=False, every=False, only_with_weights=False, filtr=None):
        self.outline = outline
        targets = (
            models.TargetVertex.objects.select_related("outline_time")
            .filter(outline=outline)
            .order_by("id")
        )
        if not every:
            self.targets = targets.filter(fake=fake, ruin=ruin)
        else:
            if only_with_weights:
                with_weight_targets = models.WeightModel.objects.select_related("target").filter(
                    target__outline=outline
                ).distinct("target").values_list("target", flat=True)

                self.targets = targets.filter(id__in=with_weight_targets)
            else:
                self.targets = targets
        if filtr is not None:
            player = filtr[0]
            coord = filtr[1]
            self.targets = self.targets.filter(target__icontains=coord, player__icontains=player)


    def targets_json_format(self):
        context = {}
        target: models.TargetVertex
        for target in self.targets:
            context[target.pk] = {
                "target": target.target,
                "player": target.player,
                "fake": target.fake,
                "ruin": target.ruin,
            }
        return json.dumps(context)

    def __create_target_dict(self, for_json=False):
        if for_json:
            result = {}
            for target in self.targets:
                result[target.target] = list()
            return result
        result = {}
        for target in self.targets:
            result[target] = list()
        return result

    def __weights(self):
        return (
            models.WeightModel.objects.select_related("target")
            .filter(target__in=self.targets)
            .order_by("order")
        )

    def target_dict_with_weights_read(self):
        """ Create dict key-target, value-lst with weights, add dist """
        context = self.__create_target_dict()
        for weight in self.__weights():
            weight.distance = round(basic.dist(weight.start, weight.target.target), 1)
            weight.off = f"{round(weight.off / 1000,1)}k"
            context[weight.target].append(weight)
        return context

    def target_dict_with_weights_extended(self):
        context = self.__create_target_dict()
        for weight in self.__weights().iterator(chunk_size=3000):
            context[weight.target].append(weight)
        return context

    def target_dict_with_weights_json_format(self):
        context = self.__create_target_dict(for_json=True)
        for weight in self.__weights().iterator(chunk_size=3000):
            context[weight.target.target].append(
                model_to_dict(
                    weight,
                    fields=[
                        "start",
                        "player",
                        "off",
                        "nobleman",
                        "distance",
                        "t1",
                        "t2",
                    ],
                )
            )
        return json.dumps(context, cls=DjangoJSONEncoder)

    def target_period_dictionary(self):
        result_dict = {}
        outline_time_dict = {}

        for target in self.targets:
            outline_time_dict[target.outline_time] = list()
        for period in self.__time_periods():
            outline_time_dict[period.outline_time].append(period)

        for target in self.targets:
            result_dict[target] = outline_time_dict[target.outline_time]

        return result_dict

    def time_period_dictionary(self):
        id_time = {}
        time_periods = {}
        for time in self.__all_outline_times():
            time_periods[time] = list()

        for period in self.__all_time_periods():
            id_time[period.outline_time.order] = period.outline_time
            time_periods[period.outline_time].append(period)

        return (id_time, time_periods)

    def __all_time_periods(self):
        times = self.__all_outline_times()
        periods = (
            models.PeriodModel.objects.select_related("outline_time").filter(
                outline_time__in=times
            )
        ).order_by("from_time", "-unit")
        return periods

    def __all_outline_times(self):
        try:
            outline_times = self.outline_times
        except AttributeError:
            outline_times = list(
                (models.OutlineTime.objects.filter(outline=self.outline)).order_by(
                    "order"
                )
            )
            self.outline_times = outline_times
        finally:
            return outline_times

    def __time_periods(self):
        periods = (
            models.PeriodModel.objects.select_related("outline_time")
            .filter(outline_time__in=[target.outline_time for target in self.targets])
            .order_by("from_time", "-unit")
        )
        return periods

    def __dict_with_village_ids(self, iterable_with_ids):
        result_id_dict = {}

        for village in (
            models.VillageModel.objects.select_related()
            .filter(coord__in=iterable_with_ids, world=self.outline.world)
            .values("coord", "village_id", "player__player_id")
        ):

            result_id_dict[village["coord"]] = village["village_id"]

        return result_id_dict
