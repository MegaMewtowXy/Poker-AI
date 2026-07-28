from models.player import Player

from engine.pot_manager import PotManager


def test_side_pots():

    print("\n========== SIDE POT TEST ==========")


    # ==========================================
    # Create Players
    # ==========================================

    alice = Player(
        "Alice",
        100
    )

    bob = Player(
        "Bob",
        500
    )

    charlie = Player(
        "Charlie",
        1000
    )


    players = [

        alice,
        bob,
        charlie

    ]


    pot_manager = PotManager()


    # ==========================================
    # Contributions
    #
    # Alice   -> 100 all-in
    # Bob     -> 300 total
    # Charlie -> 500 total
    #
    # Expected:
    #
    # Main Pot:
    # 100 * 3 = 300
    #
    # Side Pot 1:
    # 200 * 2 = 400
    #
    # Side Pot 2:
    # 200 * 1 = 200
    #
    # Total:
    # 900
    #
    # ==========================================


    contributions = [

        (alice, 100),

        (bob, 300),

        (charlie, 500)

    ]


    for player, amount in contributions:

        player.place_bet(
            amount
        )

        pot_manager.add_to_main_pot(

            player,

            amount

        )


    print("\nBefore Building Pots")

    pot_manager.print_contributions()


    # ==========================================
    # Build Side Pots
    # ==========================================

    pot_manager.build_side_pots()


    print("\nGenerated Pots")

    pot_manager.print_pots()


    # ==========================================
    # Validation
    # ==========================================

    pots = pot_manager.get_all_pots()


    assert len(pots) == 3


    assert pots[0].amount == 300

    assert pots[1].amount == 400

    assert pots[2].amount == 200


    assert pot_manager.total_pot() == 900


    print("\nTotal Pot:")

    print(
        pot_manager.total_pot()
    )


    print(
        "\n========== SIDE POT TEST PASSED =========="
    )


if __name__ == "__main__":

    test_side_pots()