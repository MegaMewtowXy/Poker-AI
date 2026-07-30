from enum import Enum, auto

class PlayerRole(Enum):

    DEALER = auto()

    SMALL_BLIND = auto()

    BIG_BLIND = auto()

    def __str__(self):

        return self.name.replace(
            "_",
            " "
        ).title()