from enum import Enum, auto


class Action(Enum):

    FOLD = auto()

    CHECK = auto()

    CALL = auto()

    BET = auto()

    RAISE = auto()

    ALL_IN = auto()