from models.player import Player


class BettingRound:
    """
    Controls a single betting street.

    (Pre-Flop, Flop, Turn or River)
    """

    def __init__(
        self,
        players: list[Player],
        starting_index: int
    ):

        self.players = players

        # Player whose turn it is
        self.current_index = starting_index

        # Player who made the most recent raise
        self.last_raiser = None

        # Last player that still needs to act
        self.last_to_act = None

        # Whether this betting round has ended
        self.finished = False

    # ==================================================
    # Round Management
    # ==================================================

    def reset(
        self,
        starting_index: int
    ):
        """
        Prepare for a new betting street.
        """

        self.current_index = starting_index

        self.last_raiser = None

        self.last_to_act = None

        self.finished = False

        for player in self.players:
            player.current_bet = 0

    # ==================================================
    # Current Player
    # ==================================================

    def current_player(self) -> Player:
        """
        Returns the player whose turn it is.
        """

        return self.players[self.current_index]

    # ==================================================
    # Turn Order
    # ==================================================

    def next_player(self):
        """
        Move to the next active player.
        """

        total = len(self.players)

        while True:

            self.current_index = (
                self.current_index + 1
            ) % total

            player = self.players[self.current_index]

            if (
                not player.folded
                and not player.all_in
                and not player.eliminated
            ):
                break

    # ==================================================
    # Player Lists
    # ==================================================

    def active_players(self):
        """
        Returns all players still in the hand.
        """

        return [

            player

            for player in self.players

            if (
                not player.folded
                and not player.eliminated
            )

        ]

    def players_still_to_act(self):
        """
        Placeholder.

        Will later return players who still
        need to respond to the latest bet.
        """

        return []

    # ==================================================
    # Round Status
    # ==================================================

    def only_one_player_left(self):
        """
        True if everyone else folded.
        """

        return len(
            self.active_players()
        ) == 1

    def end_round(self):
        """
        Finish this betting street.
        """

        self.finished = True

    def is_finished(self):
        """
        Returns whether betting has ended.
        """

        return self.finished

    # ==================================================
    # String Representation
    # ==================================================

    def __str__(self):

        return (
            f"Current Player Index : {self.current_index}\n"
            f"Last Raiser          : "
            f"{self.last_raiser.name if self.last_raiser else 'None'}\n"
            f"Finished             : {self.finished}"
        )