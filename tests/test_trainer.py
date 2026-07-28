import os

from AI.trainer import Trainer


def test_trainer():

    print("\n========== TRAINER TEST ==========")


    trainer = Trainer()


    # ==========================================
    # Reward Calculation
    # ==========================================

    positive = trainer.calculate_reward(
        500
    )

    negative = trainer.calculate_reward(
        -500
    )


    print("\nRewards")

    print(
        "Positive:",
        positive
    )

    print(
        "Negative:",
        negative
    )


    assert positive == 0.5

    assert negative == -0.5



    # ==========================================
    # Experience Recording
    # ==========================================

    trainer.record_experience(

        {
            "strength": 80,

            "position": "BUTTON"

        },

        "raise",

        0.8

    )


    trainer.record_experience(

        {
            "strength": 20

        },

        "bluff",

        -0.5

    )


    stats = trainer.statistics()


    print("\nStatistics")

    print(stats)


    assert stats["experiences"] == 2



    # ==========================================
    # Learning
    # ==========================================

    before = trainer.get_weights()


    trainer.learn()


    after = trainer.get_weights()


    print("\nWeights Before")

    print(before)


    print("\nWeights After")

    print(after)


    assert before != after



    # ==========================================
    # Save / Load
    # ==========================================

    path = "data/training_data/test_trainer.json"


    trainer.save(
        path
    )


    assert os.path.exists(
        path
    )


    new_trainer = Trainer()


    new_trainer.load(
        path
    )


    assert len(
        new_trainer.experiences
    ) == 2



    # ==========================================
    # Reset
    # ==========================================

    new_trainer.reset()


    assert len(
        new_trainer.experiences
    ) == 0



    print(
        "\n========== TRAINER TEST PASSED =========="
    )


if __name__ == "__main__":

    test_trainer()