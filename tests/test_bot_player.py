from AI.bot_player import BotPlayer

from AI.game_context import GameContext

from AI.difficulty import Difficulty

from AI.strategy import Strategy

from models.card import Card, Suit, Rank

def card(rank, suit):

    return Card(

        suit,

        rank

    )

def test_bot_player():

    print("\n========== BOT PLAYER TEST ==========")

    # ==========================================
    # Create Bot
    # ==========================================

    bot = BotPlayer(

        "DeepBot",

        Difficulty.HARD,

        Strategy.TIGHT_AGGRESSIVE

    )

    print("\nBot Profile")

    print(

        bot.profile()

    )

    profile = bot.profile()

    assert profile["name"] == "DeepBot"

    assert profile["difficulty"] == "hard"

    assert profile["strategy"] == "tight_aggressive"

    # ==========================================
    # Create Game Context
    # ==========================================

    context = GameContext(

        hole_cards=[

            card(

                Rank.ACE,

                Suit.SPADES

            ),

            card(

                Rank.ACE,

                Suit.HEARTS

            )

        ],

        community_cards=[

            card(

                Rank.KING,

                Suit.CLUBS

            ),

            card(

                Rank.SEVEN,

                Suit.DIAMONDS

            ),

            card(

                Rank.TWO,

                Suit.SPADES

            )

        ],

        position="BUTTON",

        street="flop",

        pot_size=200,

        current_bet=50,

        min_raise=100,

        big_blind=50,

        player_stack=1000,

        players_remaining=3

    )

    # ==========================================
    # Decision Test
    # ==========================================

    decision = bot.decide(

        context

    )

    print("\nDecision")

    print(

        decision

    )

    assert "action" in decision

    assert "amount" in decision

    assert "confidence" in decision

    assert "analysis" in decision

    assert decision["action"] is not None

    analysis = decision["analysis"]

    assert "strength" in analysis

    assert "equity" in analysis

    assert "bluff" in analysis

    assert "risk" in analysis

    # ==========================================
    # Opponent Model Test
    # ==========================================

    bot.add_opponent(

        "Alice"

    )

    opponent = bot.opponent_model(

        "Alice"

    )

    print("\nOpponent Profile")

    print(

        opponent.ai_profile()

    )

    assert opponent is not None

    # ==========================================
    # Range Model Test
    # ==========================================

    opponent_range = bot.opponent_range(

        "Alice"

    )

    print("\nOpponent Range")

    print(

        opponent_range.profile()

    )

    assert opponent_range is not None

    assert "range" in opponent_range.profile()

    # ==========================================
    # Learning Test
    # ==========================================

    bot.record_opponent_action(

        "Alice",

        "raise",

        "BUTTON"

    )

    updated_range = bot.opponent_range(

        "Alice"

    )

    assert len(

        updated_range.get_history()

    ) > 0

    # ==========================================
    # New Hand Reset
    # ==========================================

    bot.new_hand()

    print(

        "\n========== BOT PLAYER TEST PASSED =========="

    )

if __name__ == "__main__":

    test_bot_player()