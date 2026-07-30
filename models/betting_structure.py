from enum import Enum, auto

class BettingStructure(Enum):
    """
    Poker betting formats.
    """

    NO_LIMIT = auto()

    POT_LIMIT = auto()

    FIXED_LIMIT = auto()

    def __str__(self):

        return self.name.replace(
            "_",
            " "
        ).title()