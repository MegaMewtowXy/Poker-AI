from AI.opponent_model import (
    OpponentModel,
    OpponentType
)


def test_opponent_model():

    print("\n========== OPPONENT MODEL TEST ==========")


    # ==========================================
    # Loose Aggressive Player
    # ==========================================

    aggressive = OpponentModel(
        "Aggressive Bob"
    )


    for _ in range(100):

        aggressive.record_hand()

        aggressive.record_entry()

        aggressive.record_raise()

        aggressive.record_bet()



    for _ in range(20):

        aggressive.record_call()



    profile = aggressive.ai_profile()


    print("\nAggressive Player")

    print(profile)



    assert profile["VPIP"] == 100.0

    assert profile["PFR"] == 100.0

    assert profile["type"] == (

        OpponentType.LOOSE_AGGRESSIVE.value

    )


    assert profile["threat_level"] > 5



    # ==========================================
    # Tight Passive Player
    # ==========================================

    passive = OpponentModel(
        "Passive Alice"
    )


    for _ in range(100):

        passive.record_hand()



    for _ in range(20):

        passive.record_entry()

        passive.record_call()



    for _ in range(50):

        passive.record_fold()



    passive_profile = passive.ai_profile()


    print("\nPassive Player")

    print(passive_profile)



    assert passive_profile["VPIP"] == 20.0

    assert passive_profile["PFR"] == 0.0

    assert passive_profile["type"] == (

        OpponentType.TIGHT_PASSIVE.value

    )



    # ==========================================
    # Unknown Player
    # ==========================================

    new_player = OpponentModel(
        "New Player"
    )


    unknown = new_player.classify()


    print("\nNew Player Type")

    print(
        unknown.value
    )


    assert unknown == OpponentType.UNKNOWN



    print(
        "\n========== OPPONENT MODEL TEST PASSED =========="
    )


if __name__ == "__main__":

    test_opponent_model()