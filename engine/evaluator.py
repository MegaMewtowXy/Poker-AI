from treys import Card as TreysCard
from treys import Evaluator as TreysEvaluator

from models.card import Card
from models.hand_result import HandResult

# ==========================================================
# Treys Rank Class → Hand Name
# ==========================================================

RANK_CLASS_TO_NAME = {

    0: "Royal Flush",

    1: "Straight Flush",

    2: "Four of a Kind",

    3: "Full House",

    4: "Flush",

    5: "Straight",

    6: "Three of a Kind",

    7: "Two Pair",

    8: "Pair",

    9: "High Card"

}

class HandEvaluator:
    """
    Evaluates Texas Hold'em hands.

    Responsibilities:

    - Convert cards to Treys format
    - Evaluate hands
    - Compare results
    - Generate HandResult objects

    Does NOT:

    - Manage betting
    - Manage pots
    - Decide winners
    """

    def __init__(self):

        self.evaluator = TreysEvaluator()

    # ==================================================
    # Card Conversion
    # ==================================================

    def to_treys(
        self,
        cards: list[Card]
    ) -> list[int]:
        """
        Convert project Card objects
        into Treys integers.
        """

        suit_map = {

            "HEARTS": "h",

            "DIAMONDS": "d",

            "CLUBS": "c",

            "SPADES": "s"

        }

        converted = []

        for card in cards:

            if not hasattr(card.rank, "symbol"):

                raise ValueError(
                    f"Invalid rank: {card.rank}"
                )

            if card.suit.name not in suit_map:

                raise ValueError(
                    f"Invalid suit: {card.suit}"
                )

            converted.append(

                TreysCard.new(

                    card.rank.symbol
                    +

                    suit_map[card.suit.name]

                )

            )

        return converted
        # ==================================================
    # Validation
    # ==================================================

    def validate(
        self,
        hole_cards: list[Card],
        community_cards: list[Card]
    ):
        """
        Validate Texas Hold'em cards.
        """

        if len(hole_cards) != 2:

            raise ValueError(
                "Exactly two hole cards are required."
            )

        if len(community_cards) > 5:

            raise ValueError(
                "Community cards cannot exceed five."
            )

        if (

            len(hole_cards)

            +

            len(community_cards)

        ) > 7:

            raise ValueError(
                "Texas Hold'em supports maximum seven cards."
            )

    # ==================================================
    # Evaluation
    # ==================================================

    def evaluate(
        self,
        hole_cards: list[Card],
        community_cards: list[Card]
    ) -> HandResult:
        """
        Evaluate one player's hand.
        """

        self.validate(

            hole_cards,

            community_cards

        )

        treys_hole = self.to_treys(

            hole_cards

        )

        treys_board = self.to_treys(

            community_cards

        )

        score = self.evaluator.evaluate(

            treys_board,

            treys_hole

        )

        rank = self.evaluator.get_rank_class(

            score

        )

        return HandResult(

            score=score,

            rank=rank,

            hand_name=self.rank_name(rank)

        )

    # ==================================================
    # Hand Information
    # ==================================================

    def rank_name(
        self,
        rank: int
    ) -> str:
        """
        Convert Treys rank class
        into readable name.
        """

        return RANK_CLASS_TO_NAME.get(

            rank,

            "Unknown"

        )

    # --------------------------------------------------

    def hand_name(
        self,
        score: int
    ) -> str:
        """
        Return readable hand name
        from Treys score.
        """

        rank = self.hand_rank(

            score

        )

        return self.rank_name(

            rank

        )

    # --------------------------------------------------

    def hand_rank(
        self,
        score: int
    ) -> int:
        """
        Return Treys rank class.
        """

        return self.evaluator.get_rank_class(

            score

        )
        # ==================================================
    # Comparison
    # ==================================================

    def compare(
        self,
        first: HandResult,
        second: HandResult
    ) -> int:
        """
        Compare two evaluated hands.

        Returns:

        -1 -> first hand wins
         0 -> tie
         1 -> second hand wins

        Treys uses lower score = stronger hand.
        """

        if self.is_better(
            first,
            second
        ):

            return -1

        if self.is_better(
            second,
            first
        ):

            return 1

        return 0

    # --------------------------------------------------

    def is_better(
        self,
        first: HandResult,
        second: HandResult
    ) -> bool:
        """
        Check if first hand beats second hand.
        """

        return (

            first.score

            <

            second.score

        )

    # --------------------------------------------------

    def is_tie(
        self,
        first: HandResult,
        second: HandResult
    ) -> bool:
        """
        Check if two hands are equal.
        """

        return (

            first.score

            ==

            second.score

        )

    # ==================================================
    # Player Evaluation
    # ==================================================

    def evaluate_player(
        self,
        player,
        table
    ) -> HandResult:
        """
        Evaluate one player's hand.
        """

        return self.evaluate(

            player.hand,

            table.community_cards

        )

    # --------------------------------------------------

    def evaluate_players(
        self,
        players,
        table
    ) -> dict:
        """
        Evaluate all active players.

        Returns:

        {
            player: HandResult
        }
        """

        results = {}

        for player in players:

            if not player.is_active():

                continue

            results[player] = self.evaluate(

                player.hand,

                table.community_cards

            )

        return results

    # ==================================================
    # Winner Detection
    # ==================================================

    def winners(
        self,
        results: dict
    ) -> list:
        """
        Return all players tied
        for the best hand.
        """

        if not results:

            return []

        best_score = min(

            result.score

            for result in results.values()

        )

        return [

            player

            for player, result in results.items()

            if result.score == best_score

        ]

    # ==================================================
    # Best Five Cards
    # ==================================================

    def best_five_cards(
        self,
        hole_cards: list[Card],
        community_cards: list[Card]
    ):
        """
        Reserved for future implementation.

        Used for:

        - GUI highlighting
        - Hand history
        - Replay system
        - AI explanation

        Treys score does not directly expose
        the exact five cards.
        """

        return None

    # ==================================================
    # Debug
    # ==================================================

    def __repr__(self):

        return "HandEvaluator()"

    # --------------------------------------------------

    def __str__(self):

        return (

            "Texas Hold'em "

            "Hand Evaluator"

        )