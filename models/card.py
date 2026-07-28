from dataclasses import dataclass
from enum import Enum


# =====================================================
# Suit
# =====================================================

class Suit(Enum):
    """
    Card suits.
    """

    CLUBS = "c"

    DIAMONDS = "d"

    HEARTS = "h"

    SPADES = "s"


    # -------------------------------------------------

    @property
    def symbol(self) -> str:

        return {

            Suit.CLUBS: "♣",

            Suit.DIAMONDS: "♦",

            Suit.HEARTS: "♥",

            Suit.SPADES: "♠"

        }[self]


    # -------------------------------------------------

    @property
    def color(self) -> str:

        if self in [

            Suit.HEARTS,

            Suit.DIAMONDS

        ]:

            return "red"


        return "black"



# =====================================================
# Rank
# =====================================================

class Rank(Enum):
    """
    Poker card ranks.

    Stores:
    - display symbol
    - numeric strength
    """


    TWO = ("2", 2)

    THREE = ("3", 3)

    FOUR = ("4", 4)

    FIVE = ("5", 5)

    SIX = ("6", 6)

    SEVEN = ("7", 7)

    EIGHT = ("8", 8)

    NINE = ("9", 9)

    TEN = ("T", 10)

    JACK = ("J", 11)

    QUEEN = ("Q", 12)

    KING = ("K", 13)

    ACE = ("A", 14)



    def __init__(
        self,
        symbol: str,
        strength: int
    ):

        self.symbol = symbol

        self.strength = strength



    # -------------------------------------------------

    def __str__(self):

        return self.symbol



    # -------------------------------------------------

    @property
    def is_face(self) -> bool:

        return self in [

            Rank.JACK,

            Rank.QUEEN,

            Rank.KING

        ]



    # -------------------------------------------------

    @property
    def is_high(self) -> bool:

        return self.strength >= 10




# =====================================================
# Card
# =====================================================

@dataclass(
    frozen=True,
    slots=True
)
class Card:
    """
    Represents a standard playing card.

    Immutable because cards should never
    change after creation.
    """


    suit: Suit

    rank: Rank



    # =====================================================
    # External Evaluator Formats
    # =====================================================


    @property
    def treys(self) -> str:
        """
        Treys compatible format.

        Examples:
            As
            Th
            7d
        """

        return (

            f"{self.rank.symbol}"

            f"{self.suit.value}"

        )



    # -------------------------------------------------

    @property
    def eval7(self) -> str:
        """
        Eval7 compatible format.
        """

        return self.treys




    # =====================================================
    # Card Information
    # =====================================================


    @property
    def numeric_rank(self) -> int:

        return self.rank.strength



    # -------------------------------------------------

    @property
    def is_face_card(self) -> bool:

        return self.rank.is_face



    # -------------------------------------------------

    @property
    def is_ace(self) -> bool:

        return self.rank == Rank.ACE



    # -------------------------------------------------

    @property
    def color(self) -> str:

        return self.suit.color



    # -------------------------------------------------

    @property
    def is_red(self) -> bool:

        return self.color == "red"



    # -------------------------------------------------

    @property
    def is_black(self) -> bool:

        return self.color == "black"



    # =====================================================
    # Comparison Helpers
    # =====================================================


    def beats(
        self,
        other: "Card"
    ) -> bool:
        """
        Compare rank strength.
        """

        return (

            self.numeric_rank

            >

            other.numeric_rank

        )



    # =====================================================
    # Display
    # =====================================================


    def __str__(self):

        return (

            f"{self.rank.symbol}"

            f"{self.suit.symbol}"

        )



    # -------------------------------------------------

    def __repr__(self):

        return (

            f"Card("

            f"{self.rank.symbol}"

            f"{self.suit.value}"

            ")"

        )