from AI.range_model import RangeModel



def test_range_model():

    print("\n========== RANGE MODEL TEST ==========\n")



    # ======================================
    # Initial Range
    # ======================================

    model = RangeModel(

        "Alice"

    )


    print("Initial Range")

    print(

        model.get_range()

    )



    assert model.range["AA"] == 1.0

    assert model.range["AK"] == 1.0



    # ======================================
    # UTG Raise Test
    # ======================================

    model.observe_action(

        "raise",

        "UTG"

    )


    print("\nAfter UTG Raise")

    print(

        model.get_range()

    )



    assert model.range["KQ"] < 1.0

    assert model.range["bluffs"] < 1.0



    # ======================================
    # Button Raise Test
    # ======================================

    button_model = RangeModel(

        "Bob"

    )


    button_model.observe_action(

        "raise",

        "BUTTON"

    )


    print("\nAfter BUTTON Raise")

    print(

        button_model.get_range()

    )



    assert button_model.range["bluffs"] > 0.3



    # ======================================
    # Player Type Adjustment
    # ======================================

    lag_model = RangeModel(

        "Aggressive Player"

    )


    lag_model.observe_action(

        "raise",

        "BUTTON",

        "loose_aggressive"

    )


    print("\nLoose Aggressive Adjustment")

    print(

        lag_model.get_range()

    )



    assert lag_model.range["bluffs"] > 0.3



    # ======================================
    # 3 Bet Test
    # ======================================

    three_bet_model = RangeModel(

        "3Bet Player"

    )


    three_bet_model.observe_action(

        "3bet"

    )


    print("\nAfter 3Bet")

    print(

        three_bet_model.get_range()

    )


    assert three_bet_model.range["bluffs"] < 0.3



    # ======================================
    # Profile Test
    # ======================================

    profile = model.profile()



    print("\nProfile")

    print(profile)



    assert profile["confidence"] > 0

    assert profile["observations"] == 1

    assert profile["range_strength"] > 0



    # ======================================
    # Reset Test
    # ======================================

    model.reset()



    print("\nAfter Reset")

    print(

        model.get_range()

    )



    assert model.range["KQ"] == 0.8

    assert model.observations == 0



    print(

        "\n========== RANGE MODEL TEST PASSED =========="

    )




if __name__ == "__main__":

    test_range_model()