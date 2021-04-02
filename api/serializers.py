from rest_framework import serializers

class ChangeBuildingsArraySerializer(serializers.Serializer):
    buildings = serializers.ListField(child=serializers.CharField(max_length=100))

    def validate_buildings(self, value):
        BUILDINGS = {
            "headquarters",
            "barracks",
            "stable",
            "workshop",
            "church",
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
