from AI.bot_controller import BotController

from AI.bot_player import BotPlayer

from AI.game_context import GameContext

from AI.difficulty import Difficulty

from AI.strategy import Strategy

from models.action import Action

from models.card import Card, Suit, Rank

def card(rank, suit):

    return Card(

        suit,

        rank

    )

class MockBettingManager:

    def __init__(self):

        self.action = None

        self.amount = 0

    def fold(self, player):

        self.action = "fold"

    def check(self, player):

        self.action = "check"

    def call(self, player):

        self.action = "call"

    def bet(self, player, amount):

        self.action = "bet"

        self.amount = amount

    def raise_bet(self, player, amount):

        self.action = "raise"

        self.amount = amount

    def all_in(self, player):

        self.action = "all_in"

def test_bot_controller():

    print("\n========== BOT CONTROLLER TEST ==========")

    # ==========================================
    # Create Bot
    # ==========================================

    bot = BotPlayer(

        "DeepBot",

        Difficulty.HARD,

        Strategy.TIGHT_AGGRESSIVE

    )

    controller = BotController(

        bot

    )

    print("\nController Profile")

    print(

        controller.profile()

    )

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
    # Get Decision
    # ==========================================

    decision = controller.get_action(

        context

    )

    print("\nAI Decision")

    print(decision)

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

    # ==========================================
    # Action Conversion
    # ==========================================

    action_name = controller.action_name(

        Action.RAISE

    )

    print("\nAction Name")

    print(action_name)

    assert action_name == "raise"

    # ==========================================
    # Execute Action
    # ==========================================

    manager = MockBettingManager()

    controller.execute_action(

        decision,

        "DeepBot",

        manager

    )

    print("\nExecuted Action")

    print(manager.action)

    assert manager.action is not None

    # ==========================================
    # History
    # ==========================================

    history = controller.get_history()

    print("\nHistory")

    print(history)

    assert len(history) == 1

    assert controller.get_last_decision() == decision

    # ==========================================
    # Validation
    # ==========================================

    assert controller.validate_decision(

        decision

    )

    print(

        "\n========== BOT CONTROLLER TEST PASSED =========="

    )

if __name__ == "__main__":

    test_bot_controller()