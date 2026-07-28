from models.deck import Deck
from models.player import Player

deck = Deck()
deck.shuffle()

player1 = Player("Kshitij")
player2 = Player("Bot 1", is_ai=True)

player1.receive_card(deck.deal_card())
player1.receive_card(deck.deal_card())

player2.receive_card(deck.deal_card())
player2.receive_card(deck.deal_card())

print(player1)
print("Hand:", player1.show_hand())

print()

print(player2)
print("Hand:", player2.show_hand())

print()

print("Cards Remaining:", deck.cards_remaining())