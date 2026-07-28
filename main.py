from models.deck import Deck

deck = Deck()

print("Cards in deck:", deck.cards_remaining())

deck.shuffle()

print("First Card :", deck.deal_card())
print("Second Card:", deck.deal_card())

print("Cards Remaining:", deck.cards_remaining())