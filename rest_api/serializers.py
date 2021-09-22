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


class ChangeBuildingsArraySerializer(serializers.Serializer):
    buildings = serializers.ListField(child=serializers.CharField(max_length=100))

    def validate_buildings(self, value):
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
        for item in value:
            if item not in BUILDINGS:
                raise serializers.ValidationError("")
            else:
                BUILDINGS.discard(item)
        return value


class ChangeWeightBuildingSerializer(serializers.Serializer):
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
    building = serializers.CharField(max_length=100)

    def validate_building(self, value):
        if value not in self.BUILDINGS:
            raise serializers.ValidationError("")
        return value
