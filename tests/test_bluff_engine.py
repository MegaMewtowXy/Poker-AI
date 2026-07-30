from AI.bluff_engine import BluffEngine

from AI.strategy import (
    Strategy,
    StrategyManager
)

from AI.difficulty import (
    Difficulty,
    DifficultyManager
)

def test_bluff_engine():

    print("\n========== BLUFF ENGINE TEST ==========")

    engine = BluffEngine(

        StrategyManager(

            Strategy.BALANCED

        ),

        DifficultyManager(

            Difficulty.HARD

        )

    )

    # ======================================
    # Good Bluff Situation
    # ======================================

    result = engine.evaluate(

        position="BUTTON",

        board_analysis={

            "texture":

                "dry"

        },

        opponent_profile={

            "type":

                "tight_passive"

        },

        equity=20,

        range_profile={

            "range_strength":

                30

        }

    )

    print(

        "\nGood Bluff Situation"

    )

    print(result)

    assert result["should_bluff"] == True

    assert result["frequency"] > 0

    # ======================================
    # Bad Bluff Situation
    # ======================================

    result2 = engine.evaluate(

        position="UTG",

        board_analysis={

            "texture":

                "wet"

        },

        opponent_profile={

            "type":

                "loose_aggressive"

        },

        equity=20,

        range_profile={

            "range_strength":

                85

        }

    )

    print(

        "\nBad Bluff Situation"

    )

    print(result2)

    assert result2["frequency"] < result["frequency"]

    # ======================================
    # Expert AI Check
    # ======================================

    expert_engine = BluffEngine(

        StrategyManager(

            Strategy.LOOSE_AGGRESSIVE

        ),

        DifficultyManager(

            Difficulty.EXPERT

        )

    )

    expert_result = expert_engine.evaluate(

        position="BUTTON",

        board_analysis={

            "texture":

                "dry"

        },

        opponent_profile={

            "type":

                "tight_passive"

        },

        equity=25,

        range_profile={

            "range_strength":

                25

        }

    )

    print(

        "\nExpert Bluff Situation"

    )

    print(expert_result)

    assert expert_result["frequency"] >= result["frequency"]

    print(

        "\n========== BLUFF ENGINE TEST PASSED =========="

    )

if __name__ == "__main__":

    test_bluff_engine()