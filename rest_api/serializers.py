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

from typing import Any

from rest_framework import serializers

from utils.buildings import BUILDINGS_TRANSLATION


class TargetTimeUpdateSerializer(serializers.Serializer):
    target_id = serializers.IntegerField()
    time_id = serializers.IntegerField()


class TargetDeleteSerializer(serializers.Serializer):
    target_id = serializers.IntegerField()


class StripeSessionAmount(serializers.Serializer):
    amount = serializers.IntegerField()


class OverwiewStateHideSerializer(serializers.Serializer):
    outline_id = serializers.IntegerField()
    token = serializers.CharField()


class ChangeBuildingsArraySerializer(serializers.Serializer):
    buildings = serializers.ListField(child=serializers.CharField(max_length=100))
    outline_id = serializers.IntegerField()

    def validate_buildings(self, value: list[str]) -> list[str]:
        applied_buildings: set[str] = set()
        if not len(value):
            raise serializers.ValidationError("Buildings list is empty")
        for item in value:
            if item not in BUILDINGS_TRANSLATION:
                raise serializers.ValidationError(f"Invalid building: {item}")
            elif item in applied_buildings:
                raise serializers.ValidationError(
                    f"Building occured more than once: {item}"
                )
            else:
                applied_buildings.add(item)
        return value


class ChangeWeightBuildingSerializer(serializers.Serializer):
    building = serializers.CharField(max_length=100)
    outline_id = serializers.IntegerField()
    weight_id = serializers.IntegerField()

    def validate_building(self, value):
        if value not in BUILDINGS_TRANSLATION:
            raise serializers.ValidationError(f"Invalid building: {value}")
        return value


class OutlineSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    date = serializers.DateField()


class WorldSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    server = serializers.CharField()
    full_game_name = serializers.CharField(allow_blank=True)
    speed_units = serializers.FloatField()
    speed_world = serializers.FloatField()


class TargetSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    target = serializers.CharField()
    player = serializers.CharField(allow_blank=True)
    fake = serializers.BooleanField()
    ruin = serializers.BooleanField()
    village_id = serializers.IntegerField()
    player_id = serializers.IntegerField(allow_null=True)


class WeightSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    start = serializers.CharField()
    player = serializers.CharField()
    off = serializers.IntegerField()
    nobleman = serializers.IntegerField()
    catapult = serializers.IntegerField()
    ruin = serializers.BooleanField()
    distance = serializers.FloatField()
    time_seconds = serializers.IntegerField()
    t1 = serializers.TimeField()
    t2 = serializers.TimeField()
    building = serializers.CharField(allow_blank=True, allow_null=True)
    building_name = serializers.SerializerMethodField()
    delivery_t1 = serializers.DateTimeField()
    delivery_t2 = serializers.DateTimeField()
    shipment_t1 = serializers.DateTimeField()
    shipment_t2 = serializers.DateTimeField()
    village_id = serializers.IntegerField()
    player_id = serializers.IntegerField()
    send_url = serializers.CharField()

    def get_building_name(self, obj: Any) -> str:
        return BUILDINGS_TRANSLATION.get(obj.get("building"))  # type: ignore


class TargetOrdersSerializer(serializers.Serializer):
    target = TargetSerializer()
    my_orders = WeightSerializer(many=True)
    other_orders = WeightSerializer(many=True)


class OverviewSerializer(serializers.Serializer):
    outline = OutlineSerializer()
    world = WorldSerializer()
    targets = TargetOrdersSerializer(many=True)


class ErrorDetailSerializer(serializers.Serializer):
    detail = serializers.CharField()
