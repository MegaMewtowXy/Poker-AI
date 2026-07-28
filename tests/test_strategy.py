from AI.strategy import (
    Strategy,
    StrategyManager
)


def test_strategy():

    print("\n========== STRATEGY TEST ==========")


    # ==========================================
    # Tight Aggressive
    # ==========================================

    tag = StrategyManager(
        Strategy.TIGHT_AGGRESSIVE
    )


    print("\nTight Aggressive")

    print(
        tag.config()
    )


    assert tag.starting_hand_range() == 0.20

    assert tag.aggression() == 0.85

    assert tag.bluff_frequency() == 0.15



    # ==========================================
    # Loose Aggressive
    # ==========================================

    lag = StrategyManager(
        Strategy.LOOSE_AGGRESSIVE
    )


    print("\nLoose Aggressive")

    print(
        lag.config()
    )


    assert lag.starting_hand_range() == 0.45

    assert lag.aggression() == 0.95

    assert lag.bluff_frequency() == 0.30



    # ==========================================
    # Tight Passive
    # ==========================================

    tp = StrategyManager(
        Strategy.TIGHT_PASSIVE
    )


    print("\nTight Passive")

    print(
        tp.config()
    )


    assert tp.aggression() == 0.30

    assert tp.risk_tolerance() == 0.25



    # ==========================================
    # Balanced
    # ==========================================

    balanced = StrategyManager(
        Strategy.BALANCED
    )


    print("\nBalanced")

    print(
        balanced.config()
    )


    assert balanced.aggression() == 0.55

    assert balanced.risk_tolerance() == 0.50



    print(
        "\n========== STRATEGY TEST PASSED =========="
    )


if __name__ == "__main__":

    test_strategy()