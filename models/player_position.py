from enum import Enum, auto

class PlayerPosition(Enum):
    """
    Poker table positions.

    Position represents where a player sits
    at the table.

    Temporary responsibilities like:
        - Dealer
        - Small Blind
        - Big Blind

    are handled separately using PlayerRole.
    """

    # ==================================================
    # Positions
    # ==================================================

    BUTTON = auto()

    UNDER_THE_GUN = auto()

    UNDER_THE_GUN_PLUS_ONE = auto()

    MIDDLE_POSITION = auto()

    MIDDLE_POSITION_PLUS_ONE = auto()

    HIJACK = auto()

    CUTOFF = auto()

    BIG_BLIND = auto()

    UNKNOWN = auto()

    # ==================================================
    # Position Categories
    # ==================================================

    def is_early_position(self) -> bool:
        """
        Early table positions.
        """

        return self in {

            PlayerPosition.UNDER_THE_GUN,

            PlayerPosition.UNDER_THE_GUN_PLUS_ONE

        }

    # --------------------------------------------------

    def is_middle_position(self) -> bool:
        """
        Middle table positions.
        """

        return self in {

            PlayerPosition.MIDDLE_POSITION,

            PlayerPosition.MIDDLE_POSITION_PLUS_ONE

        }

    # --------------------------------------------------

    def is_late_position(self) -> bool:
        """
        Late positions.

        Late positions generally have
        positional advantage.
        """

        return self in {

            PlayerPosition.BUTTON,

            PlayerPosition.HIJACK,

            PlayerPosition.CUTOFF

        }

    # --------------------------------------------------

    def is_blind_position(self) -> bool:
        """
        Returns true for forced blind position.

        Big Blind remains a position because
        it affects betting order.
        """

        return self == PlayerPosition.BIG_BLIND

    # --------------------------------------------------

    def is_button(self) -> bool:

        return self == PlayerPosition.BUTTON

    # --------------------------------------------------

    def is_unknown(self) -> bool:

        return self == PlayerPosition.UNKNOWN

    # ==================================================
    # Display Helpers
    # ==================================================

    def short_name(self) -> str:
        """
        Standard poker abbreviations.
        """

        names = {

            PlayerPosition.BUTTON:
                "BTN",

            PlayerPosition.BIG_BLIND:
                "BB",

            PlayerPosition.UNDER_THE_GUN:
                "UTG",

            PlayerPosition.UNDER_THE_GUN_PLUS_ONE:
                "UTG+1",

            PlayerPosition.MIDDLE_POSITION:
                "MP",

            PlayerPosition.MIDDLE_POSITION_PLUS_ONE:
                "MP+1",

            PlayerPosition.HIJACK:
                "HJ",

            PlayerPosition.CUTOFF:
                "CO",

            PlayerPosition.UNKNOWN:
                "UNK"

        }

        return names[self]

    # ==================================================
    # Debug
    # ==================================================

    def __str__(self):

        return self.name.replace(
            "_",
            " "
        ).title()

    def __repr__(self):

        return (

            f"PlayerPosition.{self.name}"

        )