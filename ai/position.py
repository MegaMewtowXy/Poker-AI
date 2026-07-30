from models.player_position import PlayerPosition
from models.player_role import PlayerRole

class PositionAnalyzer:

    """
    Analyzes Texas Hold'em table position.

    Responsibilities
    ----------------
    • Convert engine positions into AI profiles
    • Provide aggression modifiers
    • Provide range modifiers
    • Provide positional advantage

    Does NOT:
    • Change player position
    • Control betting
    • Make decisions
    """

    POSITION_VALUES = {

        PlayerPosition.UNDER_THE_GUN: {

            "advantage": 1,

            "aggression_modifier": 0.8,

            "range_modifier": 0.8

        },

        PlayerPosition.UNDER_THE_GUN_PLUS_ONE: {

            "advantage": 1,

            "aggression_modifier": 0.85,

            "range_modifier": 0.85

        },

        PlayerPosition.MIDDLE_POSITION: {

            "advantage": 2,

            "aggression_modifier": 0.9,

            "range_modifier": 0.9

        },

        PlayerPosition.MIDDLE_POSITION_PLUS_ONE: {

            "advantage": 3,

            "aggression_modifier": 1.0,

            "range_modifier": 1.0

        },

        PlayerPosition.HIJACK: {

            "advantage": 4,

            "aggression_modifier": 1.1,

            "range_modifier": 1.1

        },

        PlayerPosition.CUTOFF: {

            "advantage": 4,

            "aggression_modifier": 1.2,

            "range_modifier": 1.2

        },

        PlayerPosition.BUTTON: {

            "advantage": 5,

            "aggression_modifier": 1.3,

            "range_modifier": 1.3

        },

        PlayerPosition.BIG_BLIND: {

            "advantage": 2,

            "aggression_modifier": 1.0,

            "range_modifier": 1.0

        }

    }

    # ==================================================
    # Analysis
    # ==================================================

    def analyze(

        self,

        position: PlayerPosition,

        roles: set[PlayerRole] | None = None

    ) -> dict:

        """
        Return AI position information.
        """

        if position not in self.POSITION_VALUES:

            return self.unknown()

        data = self.POSITION_VALUES[position]

        aggression_modifier = data["aggression_modifier"]

        range_modifier = data["range_modifier"]

        # Small Blind adjustment
        if (

            roles is not None

            and

            PlayerRole.SMALL_BLIND in roles

        ):

            aggression_modifier *= 0.9

            range_modifier *= 0.8

        return {

            "position":

                position.name,

            "advantage":

                data["advantage"],

            "aggression_modifier":

                aggression_modifier,

            "range_modifier":

                range_modifier

        }

    # ==================================================
    # Helpers
    # ==================================================

    def is_early_position(

        self,

        position: PlayerPosition

    ) -> bool:

        return isinstance(position, PlayerPosition) and position.is_early_position()

    # --------------------------------------------------

    def is_middle_position(

        self,

        position: PlayerPosition

    ) -> bool:

        return isinstance(position, PlayerPosition) and position.is_middle_position()
        # --------------------------------------------------

    def is_late_position(

        self,

        position: PlayerPosition

    ) -> bool:

        return isinstance(position, PlayerPosition) and position.is_late_position()

    # --------------------------------------------------

    def is_blind(

        self,

        position: PlayerPosition,

        roles: set[PlayerRole] | None = None

    ) -> bool:

        """
        Returns True if the player is in a blind.

        Big Blind is represented by PlayerPosition.

        Small Blind is represented by PlayerRole.
        """

        if position == PlayerPosition.BIG_BLIND:

            return True

        if (

            roles is not None

            and

            PlayerRole.SMALL_BLIND in roles

        ):

            return True

        return False

    # ==================================================
    # Unknown Handling
    # ==================================================

    @staticmethod

    def unknown():

        return {

            "position": "UNKNOWN",

            "advantage": 0,

            "aggression_modifier": 1.0,

            "range_modifier": 1.0

        }

    # ==================================================
    # Debug
    # ==================================================

    def __repr__(self):

        return "PositionAnalyzer()"

    def __str__(self):

        return (

            "Texas Hold'em "

            "Position Analyzer"

        )
