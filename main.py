from engine.evaluator import HandEvaluator
from models.card import Card, Rank, Suit

evaluator = HandEvaluator()

hole_cards = [
    Card(Suit.SPADES, Rank.ACE),
    Card(Suit.SPADES, Rank.KING)
]

community_cards = [
    Card(Suit.SPADES, Rank.QUEEN),
    Card(Suit.SPADES, Rank.JACK),
    Card(Suit.SPADES, Rank.TEN),
    Card(Suit.HEARTS, Rank.TWO),
    Card(Suit.CLUBS, Rank.THREE)
]

result = evaluator.evaluate(
    hole_cards,
    community_cards
)

print("Hand Name :", result.hand_name)
print("Rank      :", result.rank)
print("Score     :", result.score)