from enum import Enum, auto

class Street(Enum):
    """
    Represents the current stage of a Texas Hold'em hand.
    """

    PRE_FLOP = auto()

    FLOP = auto()

    TURN = auto()

    RIVER = auto()

    SHOWDOWN = auto()

    def __str__(self):

        return self.name.replace("_", " ").title()