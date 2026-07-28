from enum import Enum, auto


class Action(Enum):

    FOLD = auto()

    CHECK = auto()

    CALL = auto()

    RAISE = auto()

    ALL_IN = auto()