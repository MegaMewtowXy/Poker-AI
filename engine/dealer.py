from models.deck import Deck
from models.player import Player
from models.table import Table


class Dealer:
    """
    Responsible for all card dealing operations.
    """

    def __init__(self, deck: Deck):
        self.deck = deck

    # ----------------------------------
    # Hole Cards
    # ----------------------------------

    def deal_hole_cards(self, players: list[Player]):
        """
        Deal two cards to every player.
        """

        for _ in range(2):

            for player in players:

                player.receive_card(
                    self.deck.deal_card()
                )

    # ----------------------------------
    # Burn Card
    # ----------------------------------

    def burn_card(self):
        """
        Burn the top card.
        """

        self.deck.deal_card()

    # ----------------------------------
    # Community Cards
    # ----------------------------------

    def deal_flop(self, table: Table):
        """
        Burn one card and deal the flop.
        """

        self.burn_card()

        for _ in range(3):

            table.add_community_card(
                self.deck.deal_card()
            )

    def deal_turn(self, table: Table):
        """
        Burn one card and deal the turn.
        """

        self.burn_card()

        table.add_community_card(
            self.deck.deal_card()
        )

    def deal_river(self, table: Table):
        """
        Burn one card and deal the river.
        """

        self.burn_card()

        table.add_community_card(
            self.deck.deal_card()
        )