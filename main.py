from engine.dealer import Dealer
from models.player import Player
from models.table import Table


dealer = Dealer()

table = Table()

players = [
    Player("Kshitij"),
    Player("Bot 1", is_ai=True),
    Player("Bot 2", is_ai=True),
    Player("Bot 3", is_ai=True)
]

dealer.start_new_round()

dealer.deal_hole_cards(players)

dealer.deal_flop(table)

dealer.deal_turn(table)

dealer.deal_river(table)

print("========== PLAYERS ==========")

for player in players:
    print(player)
    print(player.show_hand())
    print()

print("========== COMMUNITY ==========")
print(table.show_community_cards())

print()

print("Cards Remaining:", dealer.deck.cards_remaining())