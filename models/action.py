from enum import Enum, auto


class Action(Enum):
    """
    All legal player actions in Texas Hold'em.
    """

    FOLD = auto()

    CHECK = auto()

    CALL = auto()

    BET = auto()

    RAISE = auto()

    ALL_IN = auto()