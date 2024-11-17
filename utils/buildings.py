import enum

from django.utils.translation import gettext_lazy


class BUILDING(enum.StrEnum):
    HEADQUARTERS = "headquarters"
    BARRACKS = "barracks"
    STABLE = "stable"
    WORKSHOP = "workshop"
    SMITHY = "smithy"
    ACADEMY = "academy"
    RALLY_POINT = "rally_point"
    STATUE = "statue"
    MARKET = "market"
    TIMBER_CAMP = "timber_camp"
    CLAY_PIT = "clay_pit"
    IRON_MINE = "iron_mine"
    FARM = "farm"
    WAREHOUSE = "warehouse"
    WALL = "wall"
    WATCHTOWER = "watchtower"


BUILDINGS_TRANSLATION: dict[str, str] = {
    BUILDING.HEADQUARTERS.value: gettext_lazy("Headquarters"),
    BUILDING.BARRACKS.value: gettext_lazy("Barracks"),
    BUILDING.STABLE.value: gettext_lazy("Stable"),
    BUILDING.WORKSHOP.value: gettext_lazy("Workshop"),
    BUILDING.ACADEMY.value: gettext_lazy("Academy"),
    BUILDING.SMITHY.value: gettext_lazy("Smithy"),
    BUILDING.RALLY_POINT.value: gettext_lazy("Rally point"),
    BUILDING.STATUE.value: gettext_lazy("Statue"),
    BUILDING.MARKET.value: gettext_lazy("Market"),
    BUILDING.TIMBER_CAMP: gettext_lazy("Timber camp"),
    BUILDING.CLAY_PIT: gettext_lazy("Clay pit"),
    BUILDING.IRON_MINE: gettext_lazy("Iron mine"),
    BUILDING.FARM: gettext_lazy("Farm"),
    BUILDING.WAREHOUSE: gettext_lazy("Warehouse"),
    BUILDING.WALL: gettext_lazy("Wall"),
    BUILDING.WATCHTOWER: gettext_lazy("Watchtower"),
}
