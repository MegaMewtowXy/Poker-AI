from models.player import Player
from models.table import Table


class BettingEngine:
    """
    Handles all betting operations.
    """

    def __init__(self, table: Table):
        self.table = table

    # ----------------------------------
    # Blinds
    # ----------------------------------

    def post_small_blind(self, player: Player):

        amount = player.place_bet(
            self.table.small_blind
        )

        self.table.add_to_pot(amount)

        self.table.current_bet = max(
            self.table.current_bet,
            amount
        )

    def post_big_blind(self, player: Player):

        amount = player.place_bet(
            self.table.big_blind
        )

        self.table.add_to_pot(amount)

        self.table.current_bet = max(
            self.table.current_bet,
            amount
        )

    # ----------------------------------
    # Player Actions
    # ----------------------------------

    def check(self, player: Player):

        return True

    def fold(self, player: Player):

        player.fold()

    def call(self, player: Player):

        amount = (
            self.table.current_bet
            - player.current_bet
        )

        amount = player.place_bet(amount)

        self.table.add_to_pot(amount)

    def bet(
        self,
        player: Player,
        amount: int
    ):

        amount = player.place_bet(amount)

        self.table.current_bet = amount

        self.table.add_to_pot(amount)

    def raise_bet(
        self,
        player: Player,
        raise_to: int
    ):

        amount = (
            raise_to
            - player.current_bet
        )

        amount = player.place_bet(amount)

        self.table.current_bet = raise_to

        self.table.add_to_pot(amount)

    def all_in(self, player: Player):

        amount = player.place_bet(
            player.chips
        )

        if player.current_bet > self.table.current_bet:

            self.table.current_bet = (
                player.current_bet
            )

        self.table.add_to_pot(amount)