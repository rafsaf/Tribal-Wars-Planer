from base import models
from tribal_wars import basic


class TargetWeightQueries:
    def __init__(self, outline):
        self.targets = models.TargetVertex.objects.select_related(
            "outline_time"
        ).filter(outline=outline)

    def __create_target_dict(self):
        result = {}
        for target in self.targets:
            result[target] = list()
        return result

    def __weights(self):
        return models.WeightModel.objects.select_related("target").filter(
            target__in=self.targets
        )

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
            context[weight.target]

            ids.add(
                f"{weight.start[0:3]}{weight.start[4:7]}{self.outline.world}"
            )
            ids.add(
                f"{weight.target.target[0:3]}"
                f"{weight.target.target[4:7]}{self.outline.world}"
            )
        return {
            "weights": context,
            "village_ids": self.__dict_with_village_ids(ids),
        }

    def __time_periods(self):
        periods = (
            models.PeriodModel.objects.select_related("outline_time")
            .filter(
                outline_time__in=[
                    target.outline_time.id for target in self.targets
                ]
            )
            .order_by("from_time", "-unit")
        )
        return periods

    def __dict_with_village_ids(self, iterable_with_ids):
        result_id_dict = {}

        for village in models.VillageModel.objects.filter(
            id__in=iterable_with_ids
        ):

            result_id_dict[
                f"{village.x_coord}|{village.y_coord}"
            ] = village.village_id

        return result_id_dict


class AllyEnemyVillagesQueries:
    def __init__(self, outline: models.Outline):
        self.outline = outline

    def __ally_tribes(self, id_list_only=True):
        ally_tribes_tags = self.outline.ally_tribe_tag
        ally_tribes_pk = [
            f"{tag}::{self.outline.world}" for tag in ally_tribes_tags
        ]
        tribes = models.Tribe.objects.filter(pk__in=ally_tribes_pk)
        if id_list_only:
            return [tribe.tribe_id for tribe in tribes]
        return tribes

    def __enemy_tribes(self, id_list_only=True):
        enemy_tribes_tags = self.outline.enemy_tribe_tag
        enemy_tribes_pk = [
            f"{tag}::{self.outline.world}" for tag in enemy_tribes_tags
        ]
        tribes = models.Tribe.objects.filter(pk__in=enemy_tribes_pk)
        if id_list_only:
            return [tribe.tribe_id for tribe in tribes]
        return tribes

    def __ally_players(self, id_list_only=True):
        ally_players = models.Player.objects.filter(
            tribe_id__in=self.__ally_tribes(), world=self.outline.world
        )
        if id_list_only:
            return [player.player_id for player in ally_players]
        return ally_players

    def __enemy_players(self, id_list_only=True):
        enemy_players = models.Player.objects.filter(
            tribe_id__in=self.__enemy_tribes(), world=self.outline.world
        )
        if id_list_only:
            return [player.player_id for player in enemy_players]
        return enemy_players

    def ally_villages(self):
        """ get all ally villages which belong to ally tribes in outline """
        ally_villages = models.VillageModel.objects.filter(
            player_id__in=self.__ally_players(), world=self.outline.world
        )
        return ally_villages

    def enemy_villages(self):
        """ get all enemy villages which belong to enemy tribes in outline """
        enemy_villages = models.VillageModel.objects.filter(
            player_id__in=self.__enemy_players(), world=self.outline.world
        )
        return enemy_villages
