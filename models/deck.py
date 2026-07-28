import random

from models.card import Card, Rank, Suit


class Deck:
    """
    Represents a standard 52-card deck.
    """

    def __init__(self):
        self.cards: list[Card] = []
        self.create_deck()

    # ----------------------------------
    # Deck Management
    # ----------------------------------

    def create_deck(self):
        """
        Create a fresh 52-card deck.
        """

        self.cards.clear()

        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        """
        Shuffle the deck.
        """

        random.shuffle(self.cards)

    def reset(self):
        """
        Create and shuffle a fresh deck.
        """

        self.create_deck()
        self.shuffle()

    # ----------------------------------
    # Card Operations
    # ----------------------------------

    def deal_card(self) -> Card:
        """
        Deal one card from the top of the deck.
        """

        if not self.cards:
            raise ValueError("No cards left in the deck.")

        return self.cards.pop()

    def cards_remaining(self) -> int:
        """
        Return number of cards remaining.
        """

        return len(self.cards)

    # ----------------------------------
    # String Representation
    # ----------------------------------

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return f"Deck({len(self.cards)} cards remaining)"