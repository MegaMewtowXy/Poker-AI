from AI.difficulty import (
    Difficulty,
    DifficultyManager
)


def test_difficulty():

    print("\n========== DIFFICULTY TEST ==========")


    # ==========================================
    # EASY
    # ==========================================

    easy = DifficultyManager(
        Difficulty.EASY
    )


    print("\nEasy Config")

    print(
        easy.config()
    )


    assert not easy.can_use_probability()

    assert not easy.can_use_opponent_model()

    assert not easy.can_bluff()

    assert not easy.can_adapt()


    # ==========================================
    # MEDIUM
    # ==========================================

    medium = DifficultyManager(
        Difficulty.MEDIUM
    )


    print("\nMedium Config")

    print(
        medium.config()
    )


    assert medium.can_use_probability()

    assert not medium.can_use_opponent_model()

    assert not medium.can_bluff()


    # ==========================================
    # HARD
    # ==========================================

    hard = DifficultyManager(
        Difficulty.HARD
    )


    print("\nHard Config")

    print(
        hard.config()
    )


    assert hard.can_use_probability()

    assert hard.can_use_opponent_model()

    assert hard.can_bluff()

    assert hard.can_adapt()

    assert not hard.can_self_train()


    # ==========================================
    # EXPERT
    # ==========================================

    expert = DifficultyManager(
        Difficulty.EXPERT
    )


    print("\nExpert Config")

    print(
        expert.config()
    )


    assert expert.can_use_probability()

    assert expert.can_use_opponent_model()

    assert expert.can_bluff()

    assert expert.can_adapt()

    assert expert.can_self_train()


    print(
        "\n========== DIFFICULTY TEST PASSED =========="
    )


if __name__ == "__main__":

    test_difficulty()