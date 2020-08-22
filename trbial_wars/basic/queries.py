from base import models
from trbial_wars import basic


class TargetWeightQueries:
    def __init__(self, outline):
        self.targets = models.TargetVertex.objects.select_related(
            "outline_time"
        ).filter(outline=outline)
        self.weigths = models.WeightModel.objects.select_related(
            "target"
        ).filter(target__in=self.targets)

    def create_target_dict(self):
        result = {}
        for target in self.targets:
            result[target] = list()
        return result

    def readonly_target_dict(self):
        context = self.create_target_dict()
        for weight in self.weights:
            weight.distance = round(
                basic.dist(weight.start, weight.target.target), 1
            )
            weight.off = f"{round(weight.off / 1000,1)}k"
            context[weight.target].append(weight)


class AllyEnemyVillagesQueries:
    def __init__(self, outline: models.Outline):
        self.outline = outline

    def ally_tribes(self, id_list_only=True):
        ally_tribes_tags = self.outline.ally_tribe_tag
        ally_tribes_pk = [
            f"{tag}::{self.outline.world}" for tag in ally_tribes_tags
        ]
        tribes = models.Tribe.objects.filter(pk__in=ally_tribes_pk)
        if id_list_only:
            return [tribe.tribe_id for tribe in tribes]
        return tribes

    def enemy_tribes(self, id_list_only=True):
        enemy_tribes_tags = self.outline.enemy_tribe_tag
        enemy_tribes_pk = [
            f"{tag}::{self.outline.world}" for tag in enemy_tribes_tags
        ]
        tribes = models.Tribe.objects.filter(pk__in=enemy_tribes_pk)
        if id_list_only:
            return [tribe.tribe_id for tribe in tribes]
        return tribes

    def ally_players(self, id_list_only=True):
        ally_players = models.Player.objects.filter(
            tribe_id__in=self.ally_tribes(), world=self.outline.world
        )
        if id_list_only:
            return [player.player_id for player in ally_players]
        return ally_players

    def enemy_players(self, id_list_only=True):
        enemy_players = models.Player.objects.filter(
            tribe_id__in=self.enemy_tribes(), world=self.outline.world
        )
        if id_list_only:
            return [player.player_id for player in enemy_players]
        return enemy_players

    def ally_villages(self):
        ally_villages = models.VillageModel.objects.filter(
            player_id__in=self.ally_players(), world=self.outline.world
        )
        return ally_villages

    def enemy_villages(self):
        enemy_villages = models.VillageModel.objects.filter(
            player_id__in=self.enemy_players(), world=self.outline.world
        )
        return enemy_villages
