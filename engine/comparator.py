from models.hand_result import HandResult


class HandComparator:

    @staticmethod
    def compare(hand1: HandResult, hand2: HandResult):
        """
        Compare two poker hands.

        Returns:
            1  -> hand1 wins
            -1 -> hand2 wins
            0  -> tie
        """

        # Compare hand ranking first
        if hand1.hand_rank > hand2.hand_rank:
            return 1

        if hand1.hand_rank < hand2.hand_rank:
            return -1

        # Compare primary values
        for v1, v2 in zip(hand1.primary_values, hand2.primary_values):

            if v1 > v2:
                return 1

            if v1 < v2:
                return -1

        # Compare kickers
        for k1, k2 in zip(hand1.kickers, hand2.kickers):

            if k1 > k2:
                return 1

            if k1 < k2:
                return -1

        return 0