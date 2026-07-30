from models.player import Player
from models.card import Card, Suit, Rank
from models.deck import Deck
from models.table import Table

from engine.pot_manager import PotManager
from engine.showdown import Showdown


def card(rank, suit):

    return Card(
        suit,
        rank
    )


def test_tie_split():

    print("\n========== TIE SPLIT TEST ==========")


    # ==========================================
    # Players
    # ==========================================

    alice = Player(
        "Alice",
        1000
    )

    bob = Player(
        "Bob",
        1000
    )


    players = [
        alice,
        bob
    ]


    # ==========================================
    # Same Straight for Both Players
    #
    # Board:
    # Q J 10 2 3
    #
    # Both have:
    # A K Q J 10 Straight
    #
    # ==========================================

    alice.hand = [

        card(
            Rank.ACE,
            Suit.SPADES
        ),

        card(
            Rank.KING,
            Suit.SPADES
        )

    ]


    bob.hand = [

        card(
            Rank.ACE,
            Suit.HEARTS
        ),

        card(
            Rank.KING,
            Suit.HEARTS
        )

    ]


    table = Table()


    table.community_cards = [

        card(
            Rank.QUEEN,
            Suit.CLUBS
        ),

        card(
            Rank.JACK,
            Suit.DIAMONDS
        ),

        card(
            Rank.TEN,
            Suit.SPADES
        ),

        card(
            Rank.TWO,
            Suit.HEARTS
        ),

        card(
            Rank.THREE,
            Suit.CLUBS
        )

    ]


    # ==========================================
    # Create Pot
    # ==========================================

    pot_manager = PotManager()


    alice.place_bet(
        100
    )

    bob.place_bet(
        100
    )


    pot_manager.add_to_main_pot(
        alice,
        100
    )

    pot_manager.add_to_main_pot(
        bob,
        100
    )


    print(
        "Pot:",
        pot_manager.total_pot()
    )


    # ==========================================
    # Showdown
    # ==========================================

    showdown = Showdown()


    results = showdown.resolve(

        players,

        table.community_cards,

        pot_manager

    )


    print("\nResults")

    for player_name, result in results["results"].items():

        print(
            player_name,
            result
        )


    # ==========================================
    # Verify Split
    # ==========================================

    print("\nChip Counts")

    print(
        "Alice:",
        alice.chips
    )

    print(
        "Bob:",
        bob.chips
    )


    assert alice.chips == 1000

    assert bob.chips == 1000


    print(
        "\n========== TIE SPLIT TEST PASSED =========="
    )


if __name__ == "__main__":

    test_tie_split()