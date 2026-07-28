from enum import Enum, auto


class Action(Enum):
    """
    All legal player actions in Texas Hold'em.

    Used by:
    - Player state
    - Betting engine
    - AI decisions
    - Replay system
    - Statistics
    """

    FOLD = auto()

    CHECK = auto()

    CALL = auto()

    BET = auto()

    RAISE = auto()

    ALL_IN = auto()

    POST_BLIND = auto()


    # ==================================================
    # Action Classification
    # ==================================================

    def is_aggressive(self) -> bool:
        """
        Returns True if action applies pressure.
        """

        return self in [

            Action.BET,

            Action.RAISE,

            Action.ALL_IN

        ]


    # --------------------------------------------------

    def is_passive(self) -> bool:
        """
        Returns True for non-aggressive actions.
        """

        return self in [

            Action.CHECK,

            Action.CALL

        ]


    # --------------------------------------------------

    def is_terminal(self) -> bool:
        """
        Returns True if player leaves the hand.
        """

        return self == Action.FOLD


    # --------------------------------------------------

    def puts_money_in(self) -> bool:
        """
        Returns True if action adds chips to pot.
        """

        return self in [

            Action.CALL,

            Action.BET,

            Action.RAISE,

            Action.ALL_IN,

            Action.POST_BLIND

        ]


    # ==================================================
    # AI Helpers
    # ==================================================

    @property
    def aggression_score(self) -> int:
        """
        Numeric aggression level.

        Used by AI analysis.
        """

        scores = {

            Action.FOLD: 0,

            Action.CHECK: 1,

            Action.CALL: 2,

            Action.POST_BLIND: 2,

            Action.BET: 3,

            Action.RAISE: 4,

            Action.ALL_IN: 5

        }

        return scores[self]


    # ==================================================
    # Display
    # ==================================================

    def __str__(self):

        return self.name.replace(
            "_",
            " "
        ).title()


    # --------------------------------------------------

    def __repr__(self):

        return f"Action.{self.name}"