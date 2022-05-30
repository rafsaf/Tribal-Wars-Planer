from base.models import Outline
from utils import basic


class SingleVillageAnalize:
    def __init__(self) -> None:
        self.all_army: basic.Army | None = None
        self.in_village_army: basic.Army | None = None
        self.enroute_army: basic.Army | None = None

        self.player: str = ""
        self.suspicious: bool = False

    @property
    def coord(self):
        return self.all_army.coord if self.all_army is not None else "X"


class OutlineTroopsAnalysis:
    def __init__(self, outline: Outline) -> None:
        self.outline = outline
        self.evidence = basic.world_evidence(world=outline.world)
        self.village_dictionary: dict[str, str] = basic.coord_to_player(outline=outline)
        self.villages: dict[str, SingleVillageAnalize] = {}

    def run_analize(self):
        self.process_off_troops()
        self.process_deff_troops()

        for vill_analize in self.villages.values():
            if (
                vill_analize.all_army is None
                or vill_analize.in_village_army is None
                or vill_analize.enroute_army is None
            ):
                continue
            if (
                vill_analize.all_army.nobleman != vill_analize.in_village_army.nobleman
                or vill_analize.in_village_army.off < 0.85 * vill_analize.all_army.off
            ):
                # too much off difference or nobles mismatch
                vill_analize.suspicious = True

        return self.villages.values()

    def process_off_troops(self):
        for line in self.outline.off_troops.split("\r\n"):
            army = basic.Army(line, self.evidence)
            player_name: str = self.village_dictionary[army.coord]
            vill_analize = SingleVillageAnalize()
            vill_analize.all_army = army
            vill_analize.player = player_name
            self.villages[army.coord] = vill_analize

    def process_deff_troops(self):
        current_coord = ""
        for line in self.outline.deff_troops.split("\r\n"):
            army = basic.Army(line, self.evidence, from_defence_line=True)
            if army.coord not in self.villages:
                continue
            if army.coord == current_coord:
                self.villages[army.coord].enroute_army = army
            else:
                self.villages[army.coord].in_village_army = army
            current_coord = army.coord
