from models.card import Card, Suit, Rank

from engine.evaluator import HandEvaluator


def card(
    rank,
    suit
):
    """
    Helper to create cards.
    """

    return Card(
        suit,
        rank
    )


def test_evaluator():

    evaluator = HandEvaluator()


    # ==================================================
    # High Card
    # ==================================================

    result = evaluator.evaluate(

        [
            card(Rank.ACE, Suit.SPADES),
            card(Rank.SEVEN, Suit.CLUBS)

        ],

        [
            card(Rank.KING, Suit.DIAMONDS),
            card(Rank.JACK, Suit.SPADES),
            card(Rank.NINE, Suit.CLUBS),
            card(Rank.FOUR, Suit.HEARTS),
            card(Rank.TWO, Suit.DIAMONDS)

        ]

    )

    print(
        "High Card:",
        result.hand_name
    )


    assert result.hand_name == "High Card"



    # ==================================================
    # Pair
    # ==================================================

    result = evaluator.evaluate(

        [
            card(Rank.ACE, Suit.SPADES),
            card(Rank.ACE, Suit.CLUBS)

        ],

        [
            card(Rank.KING, Suit.DIAMONDS),
            card(Rank.JACK, Suit.SPADES),
            card(Rank.NINE, Suit.CLUBS),
            card(Rank.FOUR, Suit.HEARTS),
            card(Rank.TWO, Suit.DIAMONDS)

        ]

    )


    print(
        "Pair:",
        result.hand_name
    )


    assert result.hand_name == "Pair"



    # ==================================================
    # Straight
    # ==================================================

    result = evaluator.evaluate(

        [
            card(Rank.ACE, Suit.SPADES),
            card(Rank.KING, Suit.CLUBS)

        ],

        [
            card(Rank.QUEEN, Suit.DIAMONDS),
            card(Rank.JACK, Suit.SPADES),
            card(Rank.TEN, Suit.CLUBS),
            card(Rank.FOUR, Suit.HEARTS),
            card(Rank.TWO, Suit.DIAMONDS)

        ]

    )


    print(
        "Straight:",
        result.hand_name
    )


    assert result.hand_name == "Straight"



    # ==================================================
    # Flush
    # ==================================================

    result = evaluator.evaluate(

        [
            card(Rank.ACE, Suit.SPADES),
            card(Rank.SEVEN, Suit.SPADES)

        ],

        [
            card(Rank.KING, Suit.SPADES),
            card(Rank.JACK, Suit.SPADES),
            card(Rank.NINE, Suit.SPADES),
            card(Rank.FOUR, Suit.SPADES),
            card(Rank.TWO, Suit.DIAMONDS)

        ]

    )


    print(
        "Flush:",
        result.hand_name
    )


    assert result.hand_name == "Flush"



    # ==================================================
    # Full House
    # ==================================================

    result = evaluator.evaluate(

        [
            card(Rank.ACE, Suit.SPADES),
            card(Rank.ACE, Suit.CLUBS)

        ],

        [
            card(Rank.ACE, Suit.DIAMONDS),
            card(Rank.KING, Suit.SPADES),
            card(Rank.KING, Suit.CLUBS),
            card(Rank.FOUR, Suit.HEARTS),
            card(Rank.TWO, Suit.DIAMONDS)

        ]

    )


    print(
        "Full House:",
        result.hand_name
    )


    assert result.hand_name == "Full House"


    print(
        "\n========== EVALUATOR TEST PASSED =========="
    )


if __name__ == "__main__":

    test_evaluator()