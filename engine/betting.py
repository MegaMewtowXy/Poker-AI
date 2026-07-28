from engine.pot_manager import PotManager
from models.player import Player
from models.table import Table


class BettingEngine:
    """
    Handles all betting operations.
    Does NOT decide whose turn it is.
    Does NOT evaluate poker hands.
    """

    def __init__(
        self,
        table: Table,
        pot_manager: PotManager
    ):
        self.table = table
        self.pot_manager = pot_manager

    # =====================================================
    # Blinds
    # =====================================================

    def post_small_blind(self, player: Player):

        amount = player.place_bet(
            self.table.small_blind
        )

        self.pot_manager.add_to_main_pot(
            player,
            amount
        )

        self.table.current_bet = max(
            self.table.current_bet,
            player.current_bet
        )

    def post_big_blind(self, player: Player):

        amount = player.place_bet(
            self.table.big_blind
        )

        self.pot_manager.add_to_main_pot(
            player,
            amount
        )

        self.table.current_bet = max(
            self.table.current_bet,
            player.current_bet
        )

    # =====================================================
    # Basic Actions
    # =====================================================

    def fold(self, player: Player):

        player.fold()

    def check(self, player: Player):

        return True

    def call(self, player: Player):

        amount = (
            self.table.current_bet
            - player.current_bet
        )

        if amount < 0:
            amount = 0

        amount = player.place_bet(amount)

        self.pot_manager.add_to_main_pot(
            player,
            amount
        )

    def bet(
        self,
        player: Player,
        amount: int
    ):

        amount = player.place_bet(amount)

        self.table.current_bet = player.current_bet

        self.table.minimum_raise = amount

        self.pot_manager.add_to_main_pot(
            player,
            amount
        )

    def raise_bet(
        self,
        player: Player,
        raise_to: int
    ):

        additional = (
            raise_to
            - player.current_bet
        )

        additional = player.place_bet(
            additional
        )

        self.table.minimum_raise = (
            raise_to
            - self.table.current_bet
        )

        self.table.current_bet = raise_to

        self.pot_manager.add_to_main_pot(
            player,
            additional
        )

    def all_in(self, player: Player):

        amount = player.place_bet(
            player.chips
        )

        if player.current_bet > self.table.current_bet:

            self.table.minimum_raise = (
                player.current_bet
                - self.table.current_bet
            )

            self.table.current_bet = (
                player.current_bet
            )

        self.pot_manager.add_to_main_pot(
            player,
            amount
        )

    # =====================================================
    # Future Features
    # =====================================================

    def create_side_pots(self):
        """
        Will be implemented later.
        """
        pass

    def distribute_pots(self):
        """
        Will be implemented later.
        """
        pass