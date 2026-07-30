from models.player import Player

from engine.pot_manager import PotManager

def test_side_pots():

    print(
        "\n========== SIDE POT TEST =========="
    )

    # ==========================================
    # Players
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
    # ==========================================

    contributions = [

        (alice,100),

        (bob,300),

        (charlie,500)

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
    # Build Pots
    # ==========================================

    pot_manager.build_side_pots()

    print("\nGenerated Pots")

    pot_manager.print_pots()

    pots = pot_manager.get_all_pots()

    # ==========================================
    # Amount Validation
    # ==========================================

    assert len(pots) == 3

    assert pots[0].amount == 300

    assert pots[1].amount == 400

    assert pots[2].amount == 200

    assert pot_manager.total_pot() == 900

    # ==========================================
    # Eligibility Validation
    # ==========================================

    main_players = pot_manager.eligible_players(

        pots[0],

        players

    )

    side_one_players = pot_manager.eligible_players(

        pots[1],

        players

    )

    side_two_players = pot_manager.eligible_players(

        pots[2],

        players

    )

    assert set(main_players) == {

        alice,

        bob,

        charlie

    }

    assert set(side_one_players) == {

        bob,

        charlie

    }

    assert set(side_two_players) == {

        charlie

    }

    print("\nTotal Pot:")

    print(

        pot_manager.total_pot()

    )

    print(

        "\n========== SIDE POT TEST PASSED =========="

    )

if __name__ == "__main__":

    test_side_pots()