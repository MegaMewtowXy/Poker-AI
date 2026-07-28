from engine.evaluator import HandEvaluator
from models.card import Card, Suit, Rank


def test(cards, expected):

    hand = HandEvaluator.evaluate(cards)

    print(
        f"{hand.hand_name:18} | "
        f"{'PASS' if hand.hand_name == expected else 'FAIL'}"
    )


print("\n----- Poker Hand Tests -----\n")

# Royal Flush

test([
    Card(Suit.SPADES, Rank.ACE),
    Card(Suit.SPADES, Rank.KING),
    Card(Suit.SPADES, Rank.QUEEN),
    Card(Suit.SPADES, Rank.JACK),
    Card(Suit.SPADES, Rank.TEN)
], "Royal Flush")


# Straight Flush

test([
    Card(Suit.HEARTS, Rank.NINE),
    Card(Suit.HEARTS, Rank.EIGHT),
    Card(Suit.HEARTS, Rank.SEVEN),
    Card(Suit.HEARTS, Rank.SIX),
    Card(Suit.HEARTS, Rank.FIVE)
], "Straight Flush")


# Four of a Kind

test([
    Card(Suit.SPADES, Rank.ACE),
    Card(Suit.HEARTS, Rank.ACE),
    Card(Suit.CLUBS, Rank.ACE),
    Card(Suit.DIAMONDS, Rank.ACE),
    Card(Suit.SPADES, Rank.KING)
], "Four of a Kind")


# Full House

test([
    Card(Suit.SPADES, Rank.ACE),
    Card(Suit.HEARTS, Rank.ACE),
    Card(Suit.CLUBS, Rank.ACE),
    Card(Suit.DIAMONDS, Rank.KING),
    Card(Suit.SPADES, Rank.KING)
], "Full House")


# Flush

test([
    Card(Suit.CLUBS, Rank.ACE),
    Card(Suit.CLUBS, Rank.JACK),
    Card(Suit.CLUBS, Rank.NINE),
    Card(Suit.CLUBS, Rank.SIX),
    Card(Suit.CLUBS, Rank.TWO)
], "Flush")


# Straight

test([
    Card(Suit.SPADES, Rank.TEN),
    Card(Suit.HEARTS, Rank.JACK),
    Card(Suit.CLUBS, Rank.QUEEN),
    Card(Suit.DIAMONDS, Rank.KING),
    Card(Suit.SPADES, Rank.ACE)
], "Straight")


# Wheel Straight

test([
    Card(Suit.SPADES, Rank.ACE),
    Card(Suit.HEARTS, Rank.TWO),
    Card(Suit.CLUBS, Rank.THREE),
    Card(Suit.DIAMONDS, Rank.FOUR),
    Card(Suit.SPADES, Rank.FIVE)
], "Straight")


# Three of a Kind

test([
    Card(Suit.SPADES, Rank.SEVEN),
    Card(Suit.HEARTS, Rank.SEVEN),
    Card(Suit.CLUBS, Rank.SEVEN),
    Card(Suit.DIAMONDS, Rank.ACE),
    Card(Suit.SPADES, Rank.KING)
], "Three of a Kind")


# Two Pair

test([
    Card(Suit.SPADES, Rank.ACE),
    Card(Suit.HEARTS, Rank.ACE),
    Card(Suit.CLUBS, Rank.KING),
    Card(Suit.DIAMONDS, Rank.KING),
    Card(Suit.SPADES, Rank.FIVE)
], "Two Pair")


# One Pair

test([
    Card(Suit.SPADES, Rank.ACE),
    Card(Suit.HEARTS, Rank.ACE),
    Card(Suit.CLUBS, Rank.KING),
    Card(Suit.DIAMONDS, Rank.QUEEN),
    Card(Suit.SPADES, Rank.EIGHT)
], "One Pair")


# High Card

test([
    Card(Suit.SPADES, Rank.ACE),
    Card(Suit.HEARTS, Rank.KING),
    Card(Suit.CLUBS, Rank.QUEEN),
    Card(Suit.DIAMONDS, Rank.NINE),
    Card(Suit.SPADES, Rank.FIVE)
], "High Card")