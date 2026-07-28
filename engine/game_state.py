from enum import Enum, auto


class GameState(Enum):
    WAITING = auto()
    PRE_FLOP = auto()
    FLOP = auto()
    TURN = auto()
    RIVER = auto()
    SHOWDOWN = auto()
    ROUND_END = auto()