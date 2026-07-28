from AI.hand_strength import HandStrength

from AI.decision import DecisionEngine

from AI.difficulty import (
    Difficulty,
    DifficultyManager
)

from AI.strategy import (
    Strategy,
    StrategyManager
)

from AI.opponent_model import OpponentModel


class BotPlayer:
    """
    AI controlled poker player.

    Responsibilities
    ----------------
    • Manage AI personality
    • Analyze situations
    • Make decisions

    This class does NOT:
        • Manage chips
        • Deal cards
        • Control game flow
    """


    def __init__(
        self,
        name: str,
        difficulty: Difficulty,
        strategy: Strategy
    ):


        self.name = name


        # ======================================
        # AI Configuration
        # ======================================

        self.difficulty = DifficultyManager(

            difficulty

        )


        self.strategy = StrategyManager(

            strategy

        )


        # ======================================
        # AI Components
        # ======================================

        self.hand_strength = HandStrength()


        self.decision_engine = DecisionEngine(

            self.hand_strength,

            self.difficulty,

            self.strategy

        )


        # ======================================
        # Opponent Memory
        # ======================================

        self.opponents = {}



    # ==========================================
    # Opponent Management
    # ==========================================

    def add_opponent(
        self,
        opponent_name: str
    ):
        """
        Add opponent to memory.
        """

        if opponent_name not in self.opponents:

            self.opponents[opponent_name] = OpponentModel(

                opponent_name

            )



    def opponent_model(
        self,
        opponent_name: str
    ):
        """
        Retrieve opponent profile.
        """

        return self.opponents.get(

            opponent_name

        )
        # ==========================================
    # Hand Analysis
    # ==========================================

    def analyze(
        self,
        hole_cards,
        community_cards,
        opponent_count,
        position=None
    ):
        """
        Analyze current poker situation.
        """

        return self.hand_strength.analyze_hand(

            hole_cards,

            community_cards,

            opponent_count,

            position

        )



    # ==========================================
    # Decision Making
    # ==========================================

    def decide(
        self,
        hole_cards,
        community_cards,
        opponent_count,
        position=None,
        opponent_name=None
    ):
        """
        Decide next poker action.
        """


        analysis = self.analyze(

            hole_cards,

            community_cards,

            opponent_count,

            position

        )


        opponent = None


        if opponent_name:

            opponent = self.opponent_model(

                opponent_name

            )


        action = self.decision_engine.decide(

            analysis["final_strength"],

            opponent

        )


        return {

            "action":

                action,


            "analysis":

                analysis

        }
        # ==========================================
    # Learning / Memory
    # ==========================================

    def record_opponent_action(
        self,
        opponent_name: str,
        action: str
    ):
        """
        Update opponent behaviour memory.
        """


        self.add_opponent(

            opponent_name

        )


        opponent = self.opponent_model(

            opponent_name

        )


        action = action.lower()



        if action == "raise":

            opponent.record_raise()


        elif action == "bet":

            opponent.record_bet()


        elif action == "call":

            opponent.record_call()


        elif action == "fold":

            opponent.record_fold()



    # ==========================================
    # Hand Tracking
    # ==========================================

    def new_hand(
        self
    ):
        """
        Called when a new hand starts.
        """

        for opponent in self.opponents.values():

            opponent.record_hand()



    # ==========================================
    # Bot Information
    # ==========================================

    def profile(
        self
    ):
        """
        Return bot configuration.
        """

        return {

            "name":

                self.name,


            "difficulty":

                self.difficulty.difficulty.value,


            "strategy":

                self.strategy.strategy.value,


            "opponents_tracked":

                len(self.opponents)

        }



    # ==========================================
    # Debug
    # ==========================================

    def __repr__(self):

        return (

            f"BotPlayer("
            f"{self.name})"

        )


    def __str__(self):

        return (

            f"AI Bot: {self.name}\n"

            f"Difficulty: "
            f"{self.difficulty.difficulty.value}\n"

            f"Strategy: "
            f"{self.strategy.strategy.value}"

        )