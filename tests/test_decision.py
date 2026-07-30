from AI.decision import (
    DecisionEngine,
    Action
)

from AI.difficulty import (
    Difficulty,
    DifficultyManager
)

from AI.strategy import (
    Strategy,
    StrategyManager
)

def test_decision():

    print("\n========== DECISION TEST ==========")

    # ==========================================
    # Hard Aggressive AI
    # ==========================================

    engine = DecisionEngine(

        DifficultyManager(
            Difficulty.HARD
        ),

        StrategyManager(
            Strategy.TIGHT_AGGRESSIVE
        )

    )

    # ==========================================
    # Strong Hand
    # ==========================================

    strong_analysis = {

        "strength": 85,

        "equity": 80,

        "pot_odds": 20,

        "position": {

            "advantage": 5

        },

        "opponent": {

            "threat_level": 3

        },

        "range": {

            "range_strength": 40

        },

        "bluff": {

            "should_bluff": False

        },

        "risk": {

            "aggression_modifier": 1.2

        }

    }

    decision = engine.decide(

        strong_analysis

    )

    print(

        "\nStrong Hand:"

    )

    print(decision)

    assert decision["action"] in [

        Action.RAISE,

        Action.BET,

        Action.ALL_IN

    ]

    # ==========================================
    # Weak Hand
    # ==========================================

    weak_analysis = {

        "strength": 10,

        "equity": 15,

        "pot_odds": 40,

        "position": {

            "advantage": 0

        },

        "opponent": {

            "threat_level": 8

        },

        "range": {

            "range_strength": 80

        },

        "bluff": {

            "should_bluff": False

        },

        "risk": {

            "aggression_modifier": 1.0

        }

    }

    decision = engine.decide(

        weak_analysis

    )

    print(

        "\nWeak Hand:"

    )

    print(decision)

    assert decision["action"] in [

        Action.FOLD,

        Action.CALL

    ]

    # ==========================================
    # Bluff Situation
    # ==========================================

    bluff_analysis = {

        "strength": 25,

        "equity": 35,

        "pot_odds": 50,

        "position": {

            "advantage": 10

        },

        "opponent": {

            "threat_level": 2

        },

        "range": {

            "range_strength": 30

        },

        "bluff": {

            "should_bluff": True

        },

        "risk": {

            "aggression_modifier": 1.3

        }

    }

    decision = engine.decide(

        bluff_analysis

    )

    print(

        "\nBluff Situation:"

    )

    print(decision)

    assert decision["action"] in [

        Action.BET,

        Action.RAISE,

        Action.CHECK,

        Action.CALL,

        Action.FOLD

    ]

    print(

        "\n========== DECISION TEST PASSED =========="

    )

if __name__ == "__main__":

    test_decision()
