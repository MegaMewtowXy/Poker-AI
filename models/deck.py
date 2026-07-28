import random

from models.card import Card, Suit, Rank


class Deck:
    """
    Represents a standard 52-card deck.
    """

    def __init__(self):

        self.cards: list[Card] = []

        self.reset()

    # =====================================================
    # Deck Management
    # =====================================================

    def reset(self):
        """
        Creates a fresh 52-card deck.
        """

        self.cards = [

            Card(suit, rank)

            for suit in Suit

            for rank in Rank

        ]

    # -----------------------------------------------------

    def shuffle(self):
        """
        Randomly shuffle the deck.
        """

        random.shuffle(self.cards)

    # =====================================================
    # Card Operations
    # =====================================================

    def deal(self) -> Card:
        """
        Deal one card from the top of the deck.
        """

        if self.is_empty():

            raise RuntimeError(
                "Cannot deal from an empty deck."
            )

        return self.cards.pop()

    # -----------------------------------------------------

    def burn(self):
        """
        Burn one card.
        """

        self.deal()

    # =====================================================
    # Probability / Simulation Helpers
    # =====================================================

    def copy(self):
        """
        Create an independent copy of the deck.

        Used by Monte Carlo simulations.
        """

        new_deck = Deck()

        new_deck.cards = self.cards.copy()

        return new_deck

    # -----------------------------------------------------

    def remaining_cards(self) -> list[Card]:
        """
        Return remaining cards without
        modifying the deck.
        """

        return self.cards.copy()

    # =====================================================
    # Information
    # =====================================================

    def cards_remaining(self) -> int:

        return len(self.cards)

    # -----------------------------------------------------

    def is_empty(self) -> bool:

        return len(self.cards) == 0

    # =====================================================
    # Debug
    # =====================================================

    def __len__(self):

        return len(self.cards)

    # -----------------------------------------------------

    def __iter__(self):

        return iter(self.cards)

    # -----------------------------------------------------

    def __repr__(self):

        return f"Deck({len(self.cards)} cards)"