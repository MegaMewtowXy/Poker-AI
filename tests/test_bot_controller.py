from AI.bot_controller import BotController

from AI.bot_player import BotPlayer

from AI.difficulty import Difficulty

from AI.strategy import Strategy

from AI.decision import Action

from models.card import Card, Suit, Rank



def card(rank, suit):

    return Card(

        suit,

        rank

    )



def test_bot_controller():

    print("\n========== BOT CONTROLLER TEST ==========")



    bot = BotPlayer(

        "DeepBot",

        Difficulty.HARD,

        Strategy.TIGHT_AGGRESSIVE

    )


    controller = BotController(

        bot

    )


    # ==========================================
    # Action Request
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



    action = controller.get_action(

        hole_cards,

        community_cards,

        opponent_count=2,

        position="BUTTON"

    )


    print("\nAI Action")

    print(

        action.value

    )


    assert isinstance(

        action,

        Action

    )



    # ==========================================
    # Action Conversion
    # ==========================================

    name = controller.action_name(

        Action.RAISE

    )


    print("\nConverted Action")

    print(name)


    assert name == "raise"



    print(
        "\n========== BOT CONTROLLER TEST PASSED =========="
    )



if __name__ == "__main__":

    test_bot_controller()