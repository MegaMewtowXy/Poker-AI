from AI.equity import EquityCalculator

from models.card import Card, Suit, Rank



def test_equity():

    print("\n========== EQUITY TEST ==========")


    calculator = EquityCalculator()



    hero_cards = [

        Card(
            Suit.SPADES,
            Rank.ACE
        ),

        Card(
            Suit.HEARTS,
            Rank.ACE
        )

    ]



    community_cards = [

        Card(
            Suit.CLUBS,
            Rank.KING
        ),

        Card(
            Suit.DIAMONDS,
            Rank.SEVEN
        ),

        Card(
            Suit.SPADES,
            Rank.TWO
        )

    ]



    result = calculator.calculate(

        hero_cards,

        community_cards,

        opponent_count=1,

        simulations=1000

    )


    print(result)



    assert "win_percentage" in result

    assert "tie_percentage" in result

    assert "lose_percentage" in result



    print(
        "\n========== EQUITY TEST PASSED =========="
    )



if __name__ == "__main__":

    test_equity()