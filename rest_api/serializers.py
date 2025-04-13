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
    id = serializers.IntegerField(help_text="Primary key in database for this outline.")
    date = serializers.DateField(help_text="Date of outline execution.")


class WorldSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text="Primary key in database for this world.")
    name = serializers.CharField(
        help_text="Prefix name of the world, for example 'pl180' or 'csc1'."
    )
    server = serializers.CharField(help_text="Server domain name.")
    full_game_name = serializers.CharField(
        allow_blank=True,
        help_text="Pretty, human readable name of the game server. This value is directly scraped from Tribal Wars.",
    )
    speed_units = serializers.FloatField(
        help_text="Speed multiplier for units on this world."
    )
    speed_world = serializers.FloatField(
        help_text="Speed multiplier for world settings."
    )


class TargetSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text="Primary key in database for this target.")
    target = serializers.CharField(help_text="Coords of village.")
    player = serializers.CharField(
        allow_blank=True, help_text="Name of the player owning the village."
    )
    fake = serializers.BooleanField(help_text="Whether this is a fake attack target.")
    ruin = serializers.BooleanField(help_text="Whether this target is ruin target.")
    village_id = serializers.IntegerField(help_text="Game ID of the village.")
    player_id = serializers.IntegerField(
        allow_null=True, help_text="Game ID of the player."
    )


class WeightSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text="Primary key in database for this order.")
    start = serializers.CharField(help_text="Coords of village.")
    player = serializers.CharField(help_text="Name of the player owning the village.")
    off = serializers.IntegerField(
        help_text="Number of offensive units including catapults. Substract catapult * 8 to get sum of other troops"
    )
    nobleman = serializers.IntegerField(help_text="Number of nobleman units.")
    catapult = serializers.IntegerField(help_text="Number of catapult units.")
    ruin = serializers.BooleanField(help_text="Whether the order is ruin attack.")
    distance = serializers.FloatField(
        help_text="Distance between this village and target one."
    )
    time_seconds = serializers.IntegerField(help_text="Travel time in seconds.")
    t1 = serializers.TimeField(help_text="Time only part of `delivery_t1`.")
    t2 = serializers.TimeField(help_text="Time only part of `delivery_t2`.")
    building = serializers.CharField(
        allow_blank=True,
        allow_null=True,
        help_text="Target building code. Lowercase, exactly the same as in game, for example 'barracks'.",
    )
    building_name = serializers.SerializerMethodField(
        help_text="Translated and prettified name of the target building in given language."
    )
    delivery_t1 = serializers.DateTimeField(
        help_text="Earliest delivery time in ISO 8601."
    )
    delivery_t2 = serializers.DateTimeField(
        help_text="Latest delivery time in ISO 8601."
    )
    shipment_t1 = serializers.DateTimeField(
        help_text="Earliest shipment time in ISO 8601."
    )
    shipment_t2 = serializers.DateTimeField(
        help_text="Latest shipment time in ISO 8601."
    )
    village_id = serializers.IntegerField(help_text="Game ID of the village.")
    player_id = serializers.IntegerField(help_text="Game ID of the player.")
    send_url = serializers.CharField(help_text="URL for sending the attack.")
    deputy_send_url = serializers.SerializerMethodField(
        help_text="URL for deputy to send the attack."
    )

    def get_building_name(self, obj: Any) -> str:
        return BUILDINGS_TRANSLATION.get(obj.get("building"))  # type: ignore

    def get_deputy_send_url(self, obj: Any) -> str:
        return f"{obj.get('send_url')}?t={obj.get('player_id')}"


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
