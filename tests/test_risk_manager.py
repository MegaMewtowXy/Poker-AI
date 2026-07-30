from AI.risk_manager import RiskManager

def test_risk_manager():

    print("\n========== RISK MANAGER TEST ==========")

    manager = RiskManager()

    short_stack = manager.analyze(

        player_stack=500,

        big_blind=50,

        strategy="tight_aggressive"

    )

    deep_stack = manager.analyze(

        player_stack=10000,

        big_blind=50,

        strategy="balanced"

    )

    print("\nShort Stack")

    print(short_stack)

    print("\nDeep Stack")

    print(deep_stack)

    assert short_stack["stack_bb"] == 10

    assert short_stack["risk_level"] > deep_stack["risk_level"]

    assert short_stack["aggression_modifier"] > deep_stack["aggression_modifier"]

    print(
        "\n========== RISK MANAGER TEST PASSED =========="
    )

if __name__ == "__main__":

    test_risk_manager()