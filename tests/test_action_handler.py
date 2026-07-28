from integration.action_handler import ActionHandler

from AI.bot_player import BotPlayer

from AI.difficulty import Difficulty

from AI.strategy import Strategy

from models.action import Action

from models.card import Card, Suit, Rank



def card(rank, suit):

    return Card(
        suit,
        rank
    )




class FakeBettingEngine:


    def __init__(self):

        self.last_action = None

        self.last_amount = 0



    def fold(self, player):

        self.last_action = "fold"



    def call(self, player):

        self.last_action = "call"



    def check(self, player):

        self.last_action = "check"



    def bet(self, player, amount):

        self.last_action = "bet"

        self.last_amount = amount



    def raise_bet(self, player, amount):

        self.last_action = "raise"

        self.last_amount = amount



    def all_in(self, player):

        self.last_action = "all_in"





class FakePlayer:


    def __init__(self):

        self.hand = [

            card(
                Rank.ACE,
                Suit.SPADES
            ),

            card(
                Rank.ACE,
                Suit.HEARTS
            )

        ]

        self.current_bet = 50

        self.chips = 1000




class FakeTable:


    def __init__(self):

        self.community_cards = [

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

        self.pot = 200

        self.min_raise = 100

        self.big_blind = 50

        self.players = [

            "player1",

            "player2",

            "player3"

        ]





def test_action_handler():


    print("\n========== ACTION HANDLER TEST ==========")



    # ==========================================
    # Engine
    # ==========================================

    engine = FakeBettingEngine()



    handler = ActionHandler(

        engine

    )




    # ==========================================
    # Bot
    # ==========================================

    bot = BotPlayer(

        "DeepBot",

        Difficulty.HARD,

        Strategy.TIGHT_AGGRESSIVE

    )



    player = FakePlayer()



    handler.register_bot(

        player,

        bot

    )




    table = FakeTable()




    # ==========================================
    # AI Decision
    # ==========================================

    decision = handler.handle_action(

        player,

        table,

        position="BUTTON",

        street="flop"

    )



    print("\nAI Decision")

    print(decision)



    print("\nEngine Action")

    print(engine.last_action)




    # ==========================================
    # Validation
    # ==========================================

    assert isinstance(

        decision,

        dict

    )



    assert isinstance(

        decision["action"],

        Action

    )



    assert "amount" in decision

    assert "confidence" in decision

    assert "analysis" in decision



    assert engine.last_action == decision["action"].name.lower()




    if decision["action"] in [

        Action.BET,

        Action.RAISE

    ]:

        assert engine.last_amount == decision["amount"]




    # ==========================================
    # History
    # ==========================================

    history = handler.get_history()



    print("\nHistory")

    print(history)



    assert len(history) == 1




    # ==========================================
    # Profile
    # ==========================================

    profile = handler.profile()



    print("\nProfile")

    print(profile)



    assert profile["registered_bots"] == 1

    assert profile["actions_processed"] == 1




    print(

        "\n========== ACTION HANDLER TEST PASSED =========="

    )




if __name__ == "__main__":

    test_action_handler()