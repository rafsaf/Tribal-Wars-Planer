from base import models
from tribal_wars import basic


class TargetWeightQueries:
    def __init__(self, outline, fake=False, every=False):
        self.outline = outline
        targets = models.TargetVertex.objects.select_related(
            "outline_time"
        ).filter(outline=outline).order_by('id')
        if not every:
            self.targets = targets.filter(fake=fake)
        else:
            self.targets = targets

    def __create_target_dict(self):
        result = {}
        for target in self.targets:
            result[target] = list()
        return result

    def __weights(self):
        return models.WeightModel.objects.select_related("target").filter(
            target__in=self.targets
        ).order_by('order')

    def target_dict_with_weights_read(self):
        """ Create dict key-target, value-lst with weights, add dist """
        context = self.__create_target_dict()
        for weight in self.__weights():
            weight.distance = round(
                basic.dist(weight.start, weight.target.target), 1
            )
            weight.off = f"{round(weight.off / 1000,1)}k"
            context[weight.target].append(weight)
        return context

    def target_dict_with_weights_extended(self):
        ids = set()
        context = self.__create_target_dict()
        for weight in self.__weights():
            context[weight.target].append(weight)

            ids.add(weight.start)
            ids.add(weight.target.target)
        result = self.__dict_with_village_ids(ids)
        return {
            "weights": context,
            "village_ids": result[0],
            "player_ids": result[1],
        }

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
            models.PeriodModel.objects.select_related('outline_time').filter(
                outline_time__in=times
            )
        ).order_by("from_time", "-unit")
        return periods

    def __all_outline_times(self):
        try:
            outline_times = self.outline_times
        except AttributeError:
            outline_times = list((
                models.OutlineTime.objects.filter(
                    outline=self.outline
                )
            ).order_by('order'))
            self.outline_times = outline_times
        finally:
            return outline_times

    def __time_periods(self):
        periods = (
            models.PeriodModel.objects.select_related("outline_time")
            .filter(
                outline_time__in=[
                    target.outline_time for target in self.targets
                ]
            )
            .order_by("from_time", "-unit")
        )
        return periods

    def __dict_with_village_ids(self, iterable_with_ids):
        result_id_dict = {}
        result_player_id = {}

        for village in models.VillageModel.objects.select_related().filter(
            coord__in=iterable_with_ids, world=self.outline.world
            ).values("coord", "village_id", "player__player_id"):

            result_id_dict[
                village["coord"]
            ] = village["village_id"]

            result_player_id[village["coord"]] = village["player__player_id"]
        return (result_id_dict, result_player_id)

