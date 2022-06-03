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

from rest_framework import serializers

BUILDINGS = {
    "headquarters",
    "barracks",
    "stable",
    "workshop",
    "academy",
    "smithy",
    "rally_point",
    "statue",
    "market",
    "timber_camp",
    "clay_pit",
    "iron_mine",
    "farm",
    "warehouse",
    "wall",
}


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

    def validate_buildings(self, value):
        applied_buildings = []
        for item in value:
            if item not in BUILDINGS:
                raise serializers.ValidationError(f"Invalid building: {item}")
            elif item in applied_buildings:
                raise serializers.ValidationError(
                    f"Building occured more than once: {item}"
                )
            else:
                applied_buildings.append(item)
        return value


class ChangeWeightBuildingSerializer(serializers.Serializer):
    building = serializers.CharField(max_length=100)
    outline_id = serializers.IntegerField()
    weight_id = serializers.IntegerField()

    def validate_building(self, value):
        if value not in BUILDINGS:
            raise serializers.ValidationError(f"Invalid building: {value}")
        return value


class UpdateOutlineOffTroops(serializers.Serializer):
    outline_id = serializers.IntegerField()
    old_line = serializers.CharField(max_length=200)
    new_line = serializers.CharField(max_length=200)
