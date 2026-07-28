from dataclasses import dataclass
from enum import Enum


# =====================================================
# Suit
# =====================================================

class Suit(Enum):
    CLUBS = "c"
    DIAMONDS = "d"
    HEARTS = "h"
    SPADES = "s"

    @property
    def symbol(self) -> str:

        return {
            Suit.CLUBS: "♣",
            Suit.DIAMONDS: "♦",
            Suit.HEARTS: "♥",
            Suit.SPADES: "♠"
        }[self]


# =====================================================
# Rank
# =====================================================

class Rank(Enum):

    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "T"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"

    @property
    def value(self) -> int:

        return {
            Rank.TWO: 2,
            Rank.THREE: 3,
            Rank.FOUR: 4,
            Rank.FIVE: 5,
            Rank.SIX: 6,
            Rank.SEVEN: 7,
            Rank.EIGHT: 8,
            Rank.NINE: 9,
            Rank.TEN: 10,
            Rank.JACK: 11,
            Rank.QUEEN: 12,
            Rank.KING: 13,
            Rank.ACE: 14
        }[self]


# =====================================================
# Card
# =====================================================

@dataclass(frozen=True, slots=True)
class Card:
    """
    Represents a standard playing card.
    """

    suit: Suit

    rank: Rank

    # -------------------------------------------------

    @property
    def treys(self) -> str:
        """
        Card string used by Treys.

        Example:
            As
            Th
            7d
        """

        return f"{self.rank.value}{self.suit.value}"

    # -------------------------------------------------

    @property
    def eval7(self) -> str:
        """
        Card string used by Eval7.
        """

        return self.treys

    # -------------------------------------------------

    @property
    def numeric_rank(self) -> int:

        return self.rank.value

    # -------------------------------------------------

    def __str__(self):

        return (
            f"{self.rank.value}"
            f"{self.suit.symbol}"
        )

    # -------------------------------------------------

    def __repr__(self):

        return str(self)