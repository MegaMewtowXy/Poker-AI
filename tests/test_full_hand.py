from models.player import Player
from models.deck import Deck
from models.table import Table

from engine.dealer import Dealer
from engine.pot_manager import PotManager
from engine.showdown import Showdown

def test_full_hand():

    print("\n========== START FULL HAND TEST ==========")

    # ==================================================
    # Create Players
    # ==================================================

    players = [

        Player(
            name="Alice",
            chips=1000
        ),

        Player(
            name="Bob",
            chips=1000
        )

    ]

    # ==================================================
    # Create Engine Components
    # ==================================================

    deck = Deck()

    dealer = Dealer(
        deck
    )

    table = Table()

    pot_manager = PotManager()

    showdown = Showdown()

    # ==================================================
    # Start Hand
    # ==================================================

    dealer.start_new_hand()

    print("\nDeck created:")
    print(
        f"Cards remaining: {deck.cards_remaining()}"
    )

    # ==================================================
    # Deal Hole Cards
    # ==================================================

    dealer.deal_hole_cards(
        players
    )

    print("\nHole Cards")

    for player in players:

        print(
            f"{player.name}: {player.show_hand()}"
        )

    # ==================================================
    # Deal Community Cards
    # ==================================================

    dealer.deal_flop(
        table
    )

    dealer.deal_turn(
        table
    )

    dealer.deal_river(
        table
    )

    print("\nCommunity Cards")

    print(
        table.show_community_cards()
    )

    # ==================================================
    # Simulate Betting
    # ==================================================

    print("\nBetting")

    bet_amount = 100

    for player in players:

        placed = player.place_bet(
            bet_amount
        )

        pot_manager.add_to_main_pot(

            player,

            placed

        )

        print(
            f"{player.name} bet {placed}"
        )

    print(
        f"Pot size: {pot_manager.total_pot()}"
    )

    # ==================================================
    # Showdown
    # ==================================================

    print("\n========== SHOWDOWN ==========")

    results = showdown.resolve(

        players,

        table.community_cards,

        pot_manager

    )

    for player_name, result in results["results"].items():

        print(
            f"{player_name}: {result}"
        )

    # ==================================================
    # Final Chips
    # ==================================================

    print("\nFinal Chips")

    for player in players:

        print(
            f"{player.name}: {player.chips}"
        )

    print("\n========== TEST COMPLETE ==========")

if __name__ == "__main__":

    test_full_hand()