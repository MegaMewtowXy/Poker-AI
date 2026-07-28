from AI.board_analysis import BoardAnalyzer

from models.card import Card, Suit, Rank



def test_board_analysis():

    print("\n========== BOARD ANALYSIS TEST ==========")


    analyzer = BoardAnalyzer()



    # ==========================================
    # Wet Board Example
    # ==========================================

    board = [

        Card(

            Suit.SPADES,

            Rank.NINE

        ),

        Card(

            Suit.SPADES,

            Rank.EIGHT

        ),

        Card(

            Suit.SPADES,

            Rank.SEVEN

        )

    ]



    result = analyzer.analyze(

        board

    )


    print(result)



    # ==========================================
    # Validation
    # ==========================================

    assert result["flush_possible"] == True


    assert result["straight_possible"] == True


    assert result["paired_board"] == False


    assert result["texture"] == "wet"


    assert result["danger_level"] >= 3



    print(
        "\n========== BOARD ANALYSIS TEST PASSED =========="
    )



if __name__ == "__main__":

    test_board_analysis()