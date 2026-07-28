from models.deck import Deck
from models.player import Player
from models.table import Table


class Dealer:
    """
    Handles all card dealing operations.
    """

    def __init__(self):
        self.deck = Deck()

    def start_new_round(self):
        """Reset and shuffle the deck."""
        self.deck.create_deck()
        self.deck.shuffle()

    def deal_hole_cards(self, players: list[Player]):
        """
        Give each active player two cards.
        """

        for player in players:
            player.clear_hand()

        for _ in range(2):
            for player in players:
                player.receive_card(self.deck.deal_card())

    def burn_card(self):
        """
        Burn one card before community cards.
        """
        self.deck.deal_card()

    def deal_flop(self, table: Table):
        """
        Burn one card and deal three community cards.
        """

        self.burn_card()

        for _ in range(3):
            table.add_community_card(self.deck.deal_card())

    def deal_turn(self, table: Table):
        """
        Burn one card and deal one community card.
        """

        self.burn_card()
        table.add_community_card(self.deck.deal_card())

    def deal_river(self, table: Table):
        """
        Burn one card and deal one community card.
        """

        self.burn_card()
        table.add_community_card(self.deck.deal_card())