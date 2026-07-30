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

    assert tag.range_width() == 0.20

    assert tag.aggression() == 0.85

    assert tag.bluff_frequency() == 0.15

    assert tag.risk_tolerance() == 0.60

    assert tag.pressure_factor() == 0.80

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

    assert lag.range_width() == 0.45

    assert lag.aggression() == 0.95

    assert lag.bluff_frequency() == 0.30

    assert lag.risk_tolerance() == 0.85

    assert lag.pressure_factor() == 1.00

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

    assert tp.pressure_factor() == 0.30

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

    assert balanced.range_width() == 0.30

    assert balanced.aggression() == 0.55

    assert balanced.risk_tolerance() == 0.50

    assert balanced.pressure_factor() == 0.55

    # ==========================================
    # Profile Test
    # ==========================================

    profile = balanced.profile()

    print("\nBalanced Profile")

    print(profile)

    assert profile["strategy"] == "balanced"

    assert profile["description"] != ""

    print(

        "\n========== STRATEGY TEST PASSED =========="

    )

if __name__ == "__main__":

    test_strategy()