from treys import Card as TreysCard
from treys import Evaluator

from models.card import Card, Rank, Suit
from models.hand_result import HandResult


class HandEvaluator:
    """
    Wrapper around the Treys poker evaluator.

    Accepts our Card objects and returns a HandResult.
    """

    def __init__(self):
        self.evaluator = Evaluator()

    @staticmethod
    def _convert_card(card: Card) -> int:
        """
        Convert our Card object to a Treys card.
        """

        rank_map = {
            Rank.TWO: "2",
            Rank.THREE: "3",
            Rank.FOUR: "4",
            Rank.FIVE: "5",
            Rank.SIX: "6",
            Rank.SEVEN: "7",
            Rank.EIGHT: "8",
            Rank.NINE: "9",
            Rank.TEN: "T",
            Rank.JACK: "J",
            Rank.QUEEN: "Q",
            Rank.KING: "K",
            Rank.ACE: "A"
        }

        suit_map = {
            Suit.SPADES: "s",
            Suit.HEARTS: "h",
            Suit.DIAMONDS: "d",
            Suit.CLUBS: "c"
        }

        return TreysCard.new(
            rank_map[card.rank] +
            suit_map[card.suit]
        )

    def evaluate(
        self,
        hole_cards: list[Card],
        community_cards: list[Card]
    ) -> HandResult:
        """
        Evaluate a Texas Hold'em hand.

        Parameters
        ----------
        hole_cards : Exactly 2 cards

        community_cards : 0-5 cards

        Returns
        -------
        HandResult
        """

        if len(hole_cards) != 2:
            raise ValueError(
                "Texas Hold'em requires exactly 2 hole cards."
            )

        if len(community_cards) > 5:
            raise ValueError(
                "Community cards cannot exceed 5."
            )

        treys_hand = [
            self._convert_card(card)
            for card in hole_cards
        ]

        treys_board = [
            self._convert_card(card)
            for card in community_cards
        ]

        score = self.evaluator.evaluate(
            treys_board,
            treys_hand
        )

        rank = self.evaluator.get_rank_class(score)

        hand_name = self.evaluator.class_to_string(rank)

        return HandResult(
            score=score,
            rank=rank,
            hand_name=hand_name
        )

    def compare(
        self,
        hand1: HandResult,
        hand2: HandResult
    ) -> HandResult:
        """
        Return the better hand.

        Treys scores work like golf:
        Lower score = Better hand.
        """

        if hand1.score < hand2.score:
            return hand1

        return hand2