from models.player import Player


class BettingRound:
    """
    Controls one betting street in Texas Hold'em.
    Responsible only for turn order and betting flow.
    """

    def __init__(
        self,
        players: list[Player],
        starting_index: int
    ):

        self.players = players

        self.current_index = starting_index

        self.last_raiser = None

        self.last_to_act = None

        self.finished = False

    # ==================================================
    # Round Management
    # ==================================================

    def reset(
        self,
        starting_index: int
    ):

        self.current_index = starting_index

        self.last_raiser = None

        self.last_to_act = None

        self.finished = False

        for player in self.players:
            player.reset_betting_round()

    # ==================================================
    # Current Player
    # ==================================================

    def current_player(self) -> Player:

        return self.players[self.current_index]

    # ==================================================
    # Player State
    # ==================================================

    def is_player_active(
        self,
        player: Player
    ) -> bool:

        return (
            not player.folded
            and not player.eliminated
            and not player.all_in
        )

    def active_players(self):

        return [

            player

            for player in self.players

            if (
                not player.folded
                and not player.eliminated
            )

        ]

    def only_one_player_left(self):

        return len(
            self.active_players()
        ) == 1

    # ==================================================
    # Turn Order
    # ==================================================

    def next_player(self):

        total = len(self.players)

        while True:

            self.current_index = (
                self.current_index + 1
            ) % total

            player = self.players[self.current_index]

            if self.is_player_active(player):
                return player

    # ==================================================
    # Betting Flow
    # ==================================================

    def set_last_raiser(
        self,
        player: Player
    ):

        self.last_raiser = player

    def set_last_to_act(
        self,
        player: Player
    ):

        self.last_to_act = player

    def should_finish(
        self,
        player: Player
    ) -> bool:

        if self.only_one_player_left():

            self.finished = True

            return True

        if (
            self.last_to_act is not None
            and player == self.last_to_act
        ):

            self.finished = True

            return True

        return False

    # ==================================================
    # Round Status
    # ==================================================

    def end_round(self):

        self.finished = True

    def is_finished(self):

        return self.finished

    # ==================================================
    # Debug
    # ==================================================

    def __str__(self):

        return (
            f"Current Player : "
            f"{self.current_player().name}\n"
            f"Finished : {self.finished}"
        )