from itertools import combinations

from engine.comparator import HandComparator
from engine.evaluator import HandEvaluator


class TexasHoldemEvaluator:

    @staticmethod
    def evaluate_best_hand(cards):
        """
        Evaluate the best possible 5-card hand
        from 7 Texas Hold'em cards.

        Parameters
        ----------
        cards : list[Card]
            7 cards (2 hole + 5 community)

        Returns
        -------
        HandResult
        """

        if len(cards) != 7:
            raise ValueError(
                "Texas Hold'em evaluation requires exactly 7 cards."
            )

        best_hand = None

        for combo in combinations(cards, 5):

            current_hand = HandEvaluator.evaluate(list(combo))

            if best_hand is None:
                best_hand = current_hand
                continue

            result = HandComparator.compare(
                current_hand,
                best_hand
            )

            if result == 1:
                best_hand = current_hand

        return best_hand