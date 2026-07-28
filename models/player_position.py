from enum import Enum, auto


class PlayerPosition(Enum):
    """
    Poker table positions.

    Supports full-ring (9 players)
    and short-handed games.
    """

    BUTTON = auto()

    SMALL_BLIND = auto()

    BIG_BLIND = auto()

    UNDER_THE_GUN = auto()

    UNDER_THE_GUN_PLUS_ONE = auto()

    MIDDLE_POSITION = auto()

    MIDDLE_POSITION_PLUS_ONE = auto()

    HIJACK = auto()

    CUTOFF = auto()

    UNKNOWN = auto()

    def __str__(self):

        return self.name.replace(
            "_",
            " "
        ).title()