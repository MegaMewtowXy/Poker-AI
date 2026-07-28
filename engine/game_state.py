from enum import Enum, auto


class GameState(Enum):
    """
    Represents the current state of a
    Texas Hold'em game.
    """

    # Waiting to begin
    WAITING = auto()

    # A new hand is being prepared
    STARTING_HAND = auto()

    # Hole cards dealt
    PRE_FLOP = auto()

    # Three community cards dealt
    FLOP = auto()

    # Fourth community card dealt
    TURN = auto()

    # Fifth community card dealt
    RIVER = auto()

    # Determining winner(s)
    SHOWDOWN = auto()

    # Hand has ended
    HAND_COMPLETE = auto()

    # Tournament finished
    GAME_OVER = auto()

    # ==================================================
    # Helpers
    # ==================================================

    def is_betting_round(self) -> bool:
        """
        Returns True if the game is currently
        in a betting street.
        """

        return self in {

            GameState.PRE_FLOP,
            GameState.FLOP,
            GameState.TURN,
            GameState.RIVER

        }

    # --------------------------------------------------

    def is_finished(self) -> bool:
        """
        Returns True if the game has ended.
        """

        return self == GameState.GAME_OVER

    # --------------------------------------------------

    def is_showdown(self) -> bool:
        """
        Returns True during showdown.
        """

        return self == GameState.SHOWDOWN

    # ==================================================
    # Debug
    # ==================================================

    def __str__(self):

        return self.name.replace(
            "_",
            " "
        ).title()