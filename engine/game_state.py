from enum import Enum, auto

class GameState(Enum):
    """
    Represents the current state of a
    Texas Hold'em game.

    This enum only manages game flow.

    It does NOT handle:
    - Players
    - Betting
    - Cards
    - Pots
    - Winners
    """

    # ==================================================
    # States
    # ==================================================

    WAITING = auto()

    STARTING_HAND = auto()

    PRE_FLOP = auto()

    FLOP = auto()

    TURN = auto()

    RIVER = auto()

    SHOWDOWN = auto()

    HAND_COMPLETE = auto()

    GAME_OVER = auto()

    # ==================================================
    # State Helpers
    # ==================================================

    def is_betting_round(
        self
    ) -> bool:
        """
        Returns True if players can make bets.
        """

        return self in {

            GameState.PRE_FLOP,

            GameState.FLOP,

            GameState.TURN,

            GameState.RIVER

        }

    # --------------------------------------------------

    def is_showdown(
        self
    ) -> bool:
        """
        Check showdown state.
        """

        return (

            self == GameState.SHOWDOWN

        )

    # --------------------------------------------------

    def is_finished(
        self
    ) -> bool:
        """
        Check if entire game ended.
        """

        return (

            self == GameState.GAME_OVER

        )

    # --------------------------------------------------

    def is_playing(
        self
    ) -> bool:
        """
        Returns True while a hand is active.
        """

        return self in {

            GameState.STARTING_HAND,

            GameState.PRE_FLOP,

            GameState.FLOP,

            GameState.TURN,

            GameState.RIVER,

            GameState.SHOWDOWN

        }

    # ==================================================
    # State Transitions
    # ==================================================

    def next_state(self):
        """
        Return the normal next state.

        Game controller decides whether
        transition is allowed.
        """

        transitions = {

            GameState.WAITING:

                GameState.STARTING_HAND,

            GameState.STARTING_HAND:

                GameState.PRE_FLOP,

            GameState.PRE_FLOP:

                GameState.FLOP,

            GameState.FLOP:

                GameState.TURN,

            GameState.TURN:

                GameState.RIVER,

            GameState.RIVER:

                GameState.SHOWDOWN,

            GameState.SHOWDOWN:

                GameState.HAND_COMPLETE,

            GameState.HAND_COMPLETE:

                GameState.STARTING_HAND

        }

        return transitions.get(
            self,
            None
        )

    # --------------------------------------------------

    def can_transition_to(
        self,
        new_state
    ) -> bool:
        """
        Validate a state transition.
        """

        return (

            self.next_state()

            ==

            new_state

        )

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

            f"GameState.{self.name}"

        )