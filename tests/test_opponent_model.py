from AI.opponent_model import OpponentModel



def test_opponent_model():

    print("\n========== OPPONENT MODEL TEST ==========\n")



    # ======================================
    # Loose Aggressive Player
    # ======================================

    aggressive = OpponentModel(

        "Aggressive Bob"

    )


    for _ in range(100):

        aggressive.record_hand()

        aggressive.record_entry()

        aggressive.record_preflop_raise()

        aggressive.record_raise(

            200

        )

        aggressive.record_bet()



    aggressive_profile = aggressive.ai_profile()



    print("Aggressive Player")

    print(

        aggressive_profile

    )



    assert aggressive_profile["VPIP"] == 100.0

    assert aggressive_profile["PFR"] == 100.0

    assert aggressive_profile["aggression"] > 1

    assert aggressive_profile["type"] == "loose_aggressive"



    # ======================================
    # Calling Station
    # ======================================

    passive = OpponentModel(

        "Passive Alice"

    )


    for _ in range(100):

        passive.record_hand()

        passive.record_entry()

        passive.record_call()



    passive_profile = passive.ai_profile()



    print("\nCalling Station")

    print(

        passive_profile

    )



    assert passive_profile["VPIP"] == 100.0

    assert passive_profile["PFR"] == 0.0

    assert passive_profile["aggression"] == 0.0

    assert passive_profile["type"] == "calling_station"



    # ======================================
    # Tight Aggressive Player
    # ======================================

    tight = OpponentModel(

        "Tight Tom"

    )


    for _ in range(100):

        tight.record_hand()



    for _ in range(20):

        tight.record_entry()

        tight.record_preflop_raise()

        tight.record_raise(

            300

        )

        tight.record_bet()



    tight_profile = tight.ai_profile()



    print("\nTight Aggressive Player")

    print(

        tight_profile

    )



    assert tight_profile["VPIP"] == 20.0

    assert tight_profile["PFR"] == 20.0

    assert tight_profile["type"] == "tight_aggressive"



    # ======================================
    # Unknown Player
    # ======================================

    unknown = OpponentModel(

        "New Player"

    )


    unknown.record_hand()



    unknown_profile = unknown.ai_profile()



    print("\nUnknown Player")

    print(

        unknown_profile

    )



    assert unknown_profile["type"] == "unknown"



    print(

        "\n========== OPPONENT MODEL TEST PASSED =========="

    )




if __name__ == "__main__":

    test_opponent_model()