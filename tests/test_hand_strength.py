from models.card import Card, Suit, Rank
from models.player_position import PlayerPosition

from AI.hand_strength import HandStrength

def card(rank, suit):

    return Card(
        suit,
        rank
    )

def test_hand_strength():

    print("\n========== HAND STRENGTH TEST ==========")

    analyzer = HandStrength()

    # ==================================================
    # Strong Hand Test
    # Pair of Aces
    # ==================================================

    hole_cards = [

        card(
            Rank.ACE,
            Suit.SPADES
        ),

        card(
            Rank.ACE,
            Suit.HEARTS
        )

    ]

    community_cards = [

        card(
            Rank.KING,
            Suit.CLUBS
        ),

        card(
            Rank.SEVEN,
            Suit.DIAMONDS
        ),

        card(
            Rank.TWO,
            Suit.SPADES
        )

    ]

    result = analyzer.analyze_hand(

        hole_cards,

        community_cards,

        opponent_count=2,

        position=PlayerPosition.BUTTON

    )

    print("\nPair Analysis")

    print(result)

    assert result["hand_name"] == "Pair"

    assert result["base_strength"] == 35

    assert result["final_strength"] > 35

    # ==================================================
    # Flush Draw Test
    # ==================================================

    hole_cards = [

        card(
            Rank.ACE,
            Suit.SPADES
        ),

        card(
            Rank.SEVEN,
            Suit.SPADES
        )

    ]

    community_cards = [

        card(
            Rank.KING,
            Suit.SPADES
        ),

        card(
            Rank.TEN,
            Suit.SPADES
        ),

        card(
            Rank.TWO,
            Suit.HEARTS
        )

    ]

    result = analyzer.analyze_hand(

        hole_cards,

        community_cards,

        opponent_count=1,

        position=PlayerPosition.BUTTON

    )

    print("\nFlush Draw Analysis")

    print(result)

    assert "Flush Draw" in result["draws"]

    assert result["draw_strength"] >= 10

    # ==================================================
    # Many Opponents Modifier
    # ==================================================

    weak_result = analyzer.analyze_hand(

        [

            card(
                Rank.ACE,
                Suit.CLUBS
            ),

            card(
                Rank.KING,
                Suit.DIAMONDS
            )

        ],

        [

            card(
                Rank.TWO,
                Suit.CLUBS
            ),

            card(
                Rank.SEVEN,
                Suit.HEARTS
            ),

            card(
                Rank.NINE,
                Suit.SPADES
            )

        ],

        opponent_count=8,

        position=PlayerPosition.BIG_BLIND

    )

    print("\nMulti Opponent Analysis")

    print(weak_result)

    assert weak_result["final_strength"] < 50

    print(
        "\n========== HAND STRENGTH TEST PASSED =========="
    )

if __name__ == "__main__":

    test_hand_strength()