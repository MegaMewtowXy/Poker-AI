from AI.decision import (
    DecisionEngine,
    Action
)

from AI.hand_strength import HandStrength

from AI.difficulty import (
    Difficulty,
    DifficultyManager
)

from AI.strategy import (
    Strategy,
    StrategyManager
)

from AI.opponent_model import (
    OpponentModel
)


def test_decision():

    print("\n========== DECISION TEST ==========")


    # ==========================================
    # Hard Aggressive AI
    # ==========================================

    engine = DecisionEngine(

        HandStrength(),

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

    action = engine.decide(

        strength=85

    )


    print(
        "\nStrong Hand:"
    )

    print(
        action.value
    )


    assert action in [

        Action.RAISE,

        Action.BET

    ]



    # ==========================================
    # Weak Hand
    # ==========================================

    action = engine.decide(

        strength=10

    )


    print(
        "\nWeak Hand:"
    )

    print(
        action.value
    )


    assert action in [

        Action.FOLD,

        Action.BET

    ]



    # ==========================================
    # Opponent Adaptation
    # ==========================================

    opponent = OpponentModel(
        "Aggressive Bob"
    )


    for _ in range(20):

        opponent.record_hand()

        opponent.record_entry()

        opponent.record_raise()

        opponent.record_bet()



    action = engine.decide(

        strength=30,

        opponent_model=opponent

    )


    print(
        "\nAgainst Aggressive Opponent:"
    )

    print(
        action.value
    )


    assert action in [

        Action.CALL,

        Action.BET,

        Action.RAISE,

        Action.FOLD

    ]


    print(
        "\n========== DECISION TEST PASSED =========="
    )


if __name__ == "__main__":

    test_decision()