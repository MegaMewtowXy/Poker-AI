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
    Evaluates Texas Hold'em hands using Treys.

    Responsibilities
    ----------------
    • Convert project cards to Treys cards
    • Evaluate poker hands
    • Return HandResult objects
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
        Convert project Card objects into
        Treys card integers.
        """

        return [

            TreysCard.new(
                card.treys
            )

            for card in cards

        ]

    # ==================================================
    # Validation
    # ==================================================

    def validate(
        self,
        hole_cards: list[Card],
        community_cards: list[Card]
    ):
        """
        Validate card counts.
        """

        if len(hole_cards) != 2:

            raise ValueError(
                "Exactly two hole cards are required."
            )

        if len(community_cards) > 5:

            raise ValueError(
                "Community cards cannot exceed five."
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
        Evaluate a player's hand.
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

        hand_name = RANK_CLASS_TO_NAME.get(
            rank,
            "Unknown"
        )

        return HandResult(
            score=score,
            rank=rank,
            hand_name=hand_name
        )
        # ==================================================
    # Hand Information
    # ==================================================

    def hand_name(
        self,
        score: int
    ) -> str:
        """
        Return the poker hand name for a score.
        """

        rank = self.hand_rank(score)

        return RANK_CLASS_TO_NAME.get(
            rank,
            "Unknown"
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

        Returns
        -------
        -1 : First hand wins
         0 : Tie
         1 : Second hand wins
        """

        if first.score < second.score:
            return -1

        if first.score > second.score:
            return 1

        return 0

    # ==================================================
    # Player Evaluation
    # ==================================================

    def evaluate_player(
        self,
        player,
        table
    ) -> HandResult:
        """
        Evaluate a player's current hand.
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

        Returns
        -------
        dict[Player, HandResult]
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
    # Future Expansion
    # ==================================================

    def best_five_cards(
        self,
        hole_cards: list[Card],
        community_cards: list[Card]
    ):
        """
        Reserved for future implementation.

        Will return the exact five cards
        that make the evaluated hand.

        Useful for:
        • GUI highlighting
        • Hand history
        • Replay mode
        • AI explanations
        """

        return None

    # ==================================================
    # Utility
    # ==================================================

    def is_better(
        self,
        first: HandResult,
        second: HandResult
    ) -> bool:
        """
        Returns True if first hand is better.
        """

        return first.score < second.score

    # --------------------------------------------------

    def is_tie(
        self,
        first: HandResult,
        second: HandResult
    ) -> bool:
        """
        Returns True if both hands tie.
        """

        return first.score == second.score

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