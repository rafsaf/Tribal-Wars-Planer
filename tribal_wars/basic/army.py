""" Army and Defence """
from .cached_property import cached_property
from base import models
from tribal_wars import basic


def world_evidence(world: models.World):
    """ For world return [T/F, .. , ..] [paladin, archer, militia]"""
    result = []
    if world.paladin == "active":
        result.append(1)
    else:
        result.append(0)
    if world.archer == "active":
        result.append(1)
    else:
        result.append(0)
    if world.militia == "active":
        result.append(1)
    else:
        result.append(0)
    return tuple(result)


class ArmyError(Exception):
    """ Army and Defence base error """


class Army:
    """ Off line in off troops """

    def __init__(self, text_army: str, evidence):
        self.text_army = text_army.split(",")
        self.world_evidence = evidence

    def clean_init(self, player_dictionary):
        """ Text army validation """

        text_army_length = len(self.text_army)
        evidence_dictionary = {
            (1, 1, 1): {16, 17},
            (1, 1, 0): {15, 16},
            (0, 1, 1): {15, 16},
            (1, 0, 1): {14, 15},
            (1, 0, 0): {13, 14},
            (0, 0, 1): {13, 14},
            (0, 1, 0): {14, 15},
            (0, 0, 0): {12, 13},
        }
        if text_army_length not in evidence_dictionary[self.world_evidence]:
            raise ArmyError(f"Długość: {text_army_length} nie jest poprawna")
        try:
            village = basic.Village(self.text_army[0])
        except basic.VillageError as identifier:
            raise ArmyError(identifier)
        else:
            if village.coord not in player_dictionary:
                raise ArmyError(
                    f"{village.coord} nie należy do żadnego plemienia!"
                )
        for army_element in self.text_army[1:-1]:
            if not army_element.isnumeric():
                raise ArmyError(f"{army_element} nie jest liczbą")
        if self.text_army[-1] != "":
            raise ArmyError(f"Błąd w składni {self.text_army[-1]}")

    @cached_property
    def coord(self):
        """ return kordy of village """
        return self.text_army[0]

    @cached_property
    def village(self):
        """ return Village instance of text[0] """
        return basic.Village(self.text_army[0])

    @cached_property
    def nobleman(self):
        """ Number of nobleman """
        if self.world_evidence[1] == 0:
            if self.world_evidence[0] == 0:
                return int(self.text_army[9])
            return int(self.text_army[10])
        if self.world_evidence[0] == 0:
            return int(self.text_army[11])
        return int(self.text_army[12])

    @cached_property
    def off(self):
        """ Number of off """

        if self.world_evidence[1] == 0: # no archers
            
            return (
                int(self.text_army[3])
                + int(self.text_army[5]) * 4
                + int(self.text_army[7]) * 5
                + int(self.text_army[8]) * 8
            ) 
        return ( # with archers
            int(self.text_army[3])
            + int(self.text_army[6]) * 4
            + int(self.text_army[7]) * 5
            + int(self.text_army[9]) * 5
            + int(self.text_army[10]) * 8
        )

    @cached_property
    def deff(self):
        """ Number of deff """
        if self.world_evidence[1] == 0: # no archers
            return (
                int(self.text_army[1])
                + int(self.text_army[2])
                + int(self.text_army[6]) * 4
            )
        return ( # with archers
            int(self.text_army[1])
            + int(self.text_army[2])
            + int(self.text_army[4])
            + int(self.text_army[8]) * 4
        )


class DefenceError(Exception):
    """ Defence Error  """


class Defence:
    """ Deff line in deff troops """

    def __init__(self, text_army: str, evidence):
        self.text_army = text_army.split(",")
        self.world_evidence = evidence

    def clean_init(self, player_dictionary):
        """ Text army validation """

        text_army_length = len(self.text_army)
        evidence_dictionary = {
            (1, 1, 1): 17,
            (1, 1, 0): 16,
            (0, 1, 1): 16,
            (1, 0, 1): 15,
            (1, 0, 0): 14,
            (0, 0, 1): 14,
            (0, 1, 0): 15,
            (0, 0, 0): 13,
        }
        if text_army_length != evidence_dictionary[self.world_evidence]:
            raise DefenceError(
                f"Długość: {text_army_length} nie jest poprawna"
            )
        try:
            village = basic.Village(self.text_army[0])
        except basic.VillageError as identifier:
            raise DefenceError(identifier)
        else:
            if village.coord not in player_dictionary:
                raise DefenceError(
                    f"{village.coord} nie należy do żadnego plemienia!"
                )
        for army_element in self.text_army[2:-1]:
            if not army_element.isnumeric():
                raise DefenceError(f"{army_element} nie jest liczbą")
        if self.text_army[1] not in {"w drodze", "w wiosce"}:
            raise DefenceError("Drugi element nieprawidłowy")
        if self.text_army[-1] != "":
            raise DefenceError(f"Błąd w składni {self.text_army[-1]}")

    @cached_property
    def coord(self):
        """ return kordy of village """
        return self.text_army[0]

    @cached_property
    def village(self):
        """ return Village instance of text[0] """
        return basic.Village(self.text_army[0])

    @cached_property
    def nobleman(self):
        """ Number of nobleman """
        if self.world_evidence[1] == 0:
            if self.world_evidence[0] == 0:
                return int(self.text_army[10])
            return int(self.text_army[11])
        if self.world_evidence[0] == 0:
            return int(self.text_army[12])
        return int(self.text_army[13])

    @cached_property
    def off(self):
        """ Number of off """

        if self.world_evidence[1] == 0:
            return (
                int(self.text_army[4])
                + int(self.text_army[6]) * 4
                + int(self.text_army[8]) * 5
                + int(self.text_army[9]) * 8
            )
        return (
            int(self.text_army[4])
            + int(self.text_army[7]) * 4
            + int(self.text_army[8]) * 5
            + int(self.text_army[10]) * 5
            + int(self.text_army[11]) * 8
        )

    @cached_property
    def deff(self):
        """ Number of deff """
        if self.world_evidence[1] == 0:
            return (
                int(self.text_army[2])
                + int(self.text_army[3])
                + int(self.text_army[7]) * 4
            )
        return (
            int(self.text_army[2])
            + int(self.text_army[3])
            + int(self.text_army[5])
            + int(self.text_army[9]) * 4
        )
