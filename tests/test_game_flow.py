from models.player import Player

from engine.game import Game


def test_game_flow():

    print("\n========== GAME FLOW TEST ==========")


    # ==========================================
    # Create Players
    # ==========================================

    players = [

        Player(
            "Alice",
            1000
        ),

        Player(
            "Bob",
            1000
        ),

        Player(
            "Charlie",
            1000
        )

    ]


    # ==========================================
    # Create Game
    # ==========================================

    game = Game(
        players
    )


    print(
        "\nStarting Game"
    )


    game.start_game()


    print(
        "Game Running:",
        game.is_running()
    )


    # ==========================================
    # Start Hand
    # ==========================================

    game.start_hand()


    print(
        "\nHand Number:",
        game.current_hand()
    )


    # ==========================================
    # Verify Hole Cards
    # ==========================================

    print(
        "\nHole Cards"
    )

    for player in players:

        print(
            player.name,
            player.show_hand()
        )


        assert len(player.hand) == 2


    # ==========================================
    # Verify Positions
    # ==========================================

    print(
        "\nPositions"
    )

    for player in players:

        print(
            player.name,
            player.position
        )


    # ==========================================
    # Verify Table
    # ==========================================

    print(
        "\nCommunity Cards:"
    )

    print(
        len(
            game.table.community_cards
        )
    )


    assert len(
        game.table.community_cards
    ) == 0


    # ==========================================
    # Stop Game
    # ==========================================

    game.stop_game()


    assert not game.is_running()


    print(
        "\n========== GAME FLOW TEST PASSED =========="
    )


if __name__ == "__main__":

    test_game_flow()