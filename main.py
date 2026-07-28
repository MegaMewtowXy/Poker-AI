from models.deck import Deck
from models.player import Player
from models.table import Table

deck = Deck()
deck.shuffle()

table = Table()

player1 = Player("Kshitij")
player2 = Player("Bot 1", is_ai=True)

# Deal hole cards
for _ in range(2):
    player1.receive_card(deck.deal_card())
    player2.receive_card(deck.deal_card())

# Simulate flop
for _ in range(3):
    table.add_community_card(deck.deal_card())

print(player1)
print("Hand:", player1.show_hand())

print()

print(player2)
print("Hand:", player2.show_hand())

print()

print(table)

print()

print("Cards Remaining:", deck.cards_remaining())