from AI.bot_player import BotPlayer

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


    bot = BotPlayer(

        "DeepBot",

        Difficulty.HARD,

        Strategy.TIGHT_AGGRESSIVE

    )


    # ==========================================
    # Profile
    # ==========================================

    profile = bot.profile()


    print("\nBot Profile")

    print(profile)


    assert profile["name"] == "DeepBot"

    assert profile["difficulty"] == "hard"

    assert profile["strategy"] == "tight_aggressive"



    # ==========================================
    # Hand Decision
    # ==========================================

    hole_cards = [

        card(

            Rank.ACE,

            Suit.SPADES

        ),

        card(

            Rank.ACE,

            Suit.HEARTS

        )

    ]


    community_cards = [

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

    ]


    result = bot.decide(

        hole_cards,

        community_cards,

        opponent_count=2,

        position="BUTTON"

    )


    print("\nDecision")

    print(result)



    assert "action" in result

    assert "analysis" in result



    # ==========================================
    # Opponent Memory
    # ==========================================

    bot.new_hand()


    bot.record_opponent_action(

        "Alice",

        "raise"

    )


    bot.record_opponent_action(

        "Alice",

        "bet"

    )


    opponent = bot.opponent_model(

        "Alice"

    )


    print("\nOpponent Profile")

    print(

        opponent.ai_profile()

    )


    assert opponent is not None


    print(
        "\n========== BOT PLAYER TEST PASSED =========="
    )



if __name__ == "__main__":

    test_bot_player()