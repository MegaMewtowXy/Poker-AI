import random

from models.card import Card, Suit, Rank


class Deck:

    def __init__(self):
        self.cards = []
        self.create_deck()

    def create_deck(self):
        """Creates a standard 52-card deck."""
        self.cards.clear()

        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        """Shuffles the deck."""
        random.shuffle(self.cards)

    def deal_card(self):
        """Deals one card from the top of the deck."""

        if len(self.cards) == 0:
            raise ValueError("No cards left in the deck!")

        return self.cards.pop()

    def cards_remaining(self):
        """Returns the number of cards remaining."""
        return len(self.cards)