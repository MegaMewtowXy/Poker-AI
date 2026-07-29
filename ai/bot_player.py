from AI.hand_strength import HandStrength

from AI.decision import DecisionEngine

from AI.bet_sizing import BetSizer

from AI.game_context import GameContext

from AI.equity import EquityCalculator

from AI.pot_odds import PotOddsCalculator

from AI.board_analysis import BoardAnalyzer

from AI.position import PositionAnalyzer

from AI.bluff_engine import BluffEngine

from AI.risk_manager import RiskManager

from AI.range_model import RangeModel


from AI.difficulty import (
    Difficulty,
    DifficultyManager
)


from AI.strategy import (
    Strategy,
    StrategyManager
)


from AI.opponent_model import OpponentModel


from models.action import Action





class BotPlayer:
    """
    Final Texas Hold'em AI Player.

    Responsibilities
    ----------------
    • Analyse game state
    • Evaluate hand strength
    • Calculate equity
    • Analyse opponents
    • Estimate bluff opportunities
    • Make decisions
    • Calculate bet sizes

    Does NOT
    --------
    • Manage chips
    • Execute bets
    • Control game loop
    """




    def __init__(
        self,
        name: str,
        difficulty: Difficulty = Difficulty.MEDIUM,
        strategy: Strategy = Strategy.BALANCED
    ):


        self.name = name



        # ======================================
        # AI Personality
        # ======================================

        self.difficulty = DifficultyManager(

            difficulty

        )


        self.strategy = StrategyManager(

            strategy

        )



        # ======================================
        # Poker Intelligence
        # ======================================

        self.hand_strength = HandStrength()


        self.equity = EquityCalculator()


        self.pot_odds = PotOddsCalculator()


        self.board_analyzer = BoardAnalyzer()


        self.position_analyzer = PositionAnalyzer()


        self.risk_manager = RiskManager(

            self.strategy

        )



        # ======================================
        # Decision Modules
        # ======================================

        self.bluff_engine = BluffEngine(

            self.strategy,

            self.difficulty

        )


        self.bet_sizer = BetSizer(

            self.strategy,

            self.difficulty

        )


        self.decision_engine = DecisionEngine(

            self.difficulty,

            self.strategy

        )



        # ======================================
        # Opponent Intelligence
        # ======================================

        self.opponents = {}


        self.opponent_ranges = {}
    
    # ==========================================
    # Opponent Management
    # ==========================================

    def add_opponent(
        self,
        opponent_name
    ):
        """
        Add opponent tracking.
        """


        if opponent_name not in self.opponents:

            self.opponents[opponent_name] = OpponentModel(

                opponent_name

            )



        if opponent_name not in self.opponent_ranges:

            self.opponent_ranges[opponent_name] = RangeModel(

                opponent_name

            )




    def opponent_model(
        self,
        opponent_name
    ):
        """
        Get opponent statistics.
        """

        return self.opponents.get(

            opponent_name

        )




    def opponent_range(
        self,
        opponent_name
    ):
        """
        Get opponent range.
        """

        return self.opponent_ranges.get(

            opponent_name

        )





    # ==========================================
    # Hand Analysis
    # ==========================================

    def analyze_hand(
        self,
        context: GameContext
    ):
        """
        Analyse current hand strength.
        """

        return self.hand_strength.analyze_hand(

            context.hole_cards,

            context.community_cards,

            context.players_remaining,

            context.position,

            context.roles

        )





    # ==========================================
    # Complete Intelligence Builder
    # ==========================================

    def build_analysis(
        self,
        context: GameContext,
        opponent_name=None
    ):
        """
        Build complete AI information package.

        Sent to DecisionEngine.
        """



        # ======================================
        # Hand Strength
        # ======================================

        hand = self.analyze_hand(

            context

        )


        strength = hand.get(

            "final_strength",

            0

        )





        # ======================================
        # Equity
        # ======================================

        if self.difficulty.can_use_probability():

            equity_result = self.equity.calculate(

                context.hole_cards,

                context.community_cards,

                max(

                    context.players_remaining - 1,

                    1

                ),

                simulations=self.difficulty.equity_simulations()

            )

            equity = equity_result.get(

                "equity",

                0

            )

        else:

            # Easy mode intentionally avoids simulation while retaining a
            # usable, percentage-based estimate for the rest of the pipeline.
            equity_result = {"equity": strength, "estimated": True}
            equity = strength





        # ======================================
        # Pot Odds
        # ======================================

        pot_odds = self.pot_odds.calculate(

            context.pot_size,

            context.call_amount

        )




        
        # ======================================
        # Board Analysis
        # ======================================

        board = self.board_analyzer.analyze(

            context.community_cards

        )





        # ======================================
        # Position
        # ======================================

        position = self.position_analyzer.analyze(

            context.position,
            context.roles

        )





        # ======================================
        # Opponent Intelligence
        # ======================================

        opponent_profile = None

        range_profile = None



        if opponent_name:


            self.add_opponent(

                opponent_name

            )



            if self.difficulty.can_use_opponent_model():


                opponent = self.opponent_model(

                    opponent_name

                )


                opponent_range = self.opponent_range(

                    opponent_name

                )



                opponent_profile = opponent.ai_profile()



                if opponent_range:

                    range_profile = opponent_range.profile()



        # ======================================
        # Bluff Analysis
        # ======================================

        bluff = {


            "should_bluff":

                False,


            "frequency":

                0,


            "score":

                0

        }



        if self.difficulty.can_bluff():


            bluff = self.bluff_engine.evaluate(

                context.position,

                board,

                opponent_profile,

                equity,

                range_profile,

                context=context

            )





        # ======================================
        # Risk Analysis
        # ======================================

        risk = self.risk_manager.analyze(

            context.player_stack,

            context.big_blind,

            self.strategy.strategy.value

        )
        risk["apply_to_decision"] = True





        return {


            "strength":

                strength,


            "hand":

                hand,


            "equity":

                equity,


            "equity_details":

                equity_result,


            "pot_odds":

                pot_odds,


            "board":

                board,


            "position":

                position,


            "bluff":

                bluff,


            "risk":

                risk,


            "opponent":

                opponent_profile,


            "range":

                range_profile,
             "call_amount":

        context.call_amount,

    "current_bet":

        context.current_bet,

    "min_raise":

        context.min_raise,

    "pot_size":

        context.pot_size,

    "player_stack":

        context.player_stack 

        }
    
    # ==========================================
    # Final AI Decision
    # ==========================================

    def decide(
        self,
        context: GameContext,
        opponent_name=None
    ):
        """
        Complete AI decision pipeline.

        Returns:

        {
            action,
            amount,
            confidence,
            reason,
            sizing,
            analysis
        }
        """



        # ======================================
        # Build Analysis
        # ======================================

        analysis = self.build_analysis(

            context,

            opponent_name

        )





        # ======================================
        # Decision Engine
        # ======================================

        decision = self.decision_engine.decide(

            analysis

        )



        action = decision["action"]



        amount = 0

        sizing = None





        # ======================================
        # Bet Sizing
        # ======================================

        if action in [

            Action.BET,

            Action.RAISE,

            Action.ALL_IN

        ]:


            sizing = self.bet_sizer.calculate_size(

                action,

                context,

                analysis["strength"],

                analysis["equity"],

                analysis.get(

                    "opponent"

                )

            )



            amount = sizing.get(

                "amount",

                0

            )
            if (
    action == Action.RAISE
    and
    sizing is not None
    and
    sizing.get("reason") == "all_in"
):

                action = Action.ALL_IN

       


        return {


            "action":

                action,


            "amount":

                amount,


            "confidence":

                decision.get(

                    "confidence",

                    0

                ),


            "reason":

                decision.get(

                    "reason",

                    ""

                ),


            "score":

                decision.get(

                    "score",

                    0

                ),


            "sizing":

                sizing,


            "analysis":

                analysis

        }





    # ==========================================
    # Opponent Learning
    # ==========================================

    def record_opponent_action(
        self,
        opponent_name,
        action,
        position=None,
        street=None,
        *args,
        **kwargs
    ):
        """
        Learn opponent behaviour.

        Updates:
        - Opponent statistics
        - Possible hand range
        """



        self.add_opponent(

            opponent_name

        )



        opponent = self.opponent_model(

            opponent_name

        )


        opponent_range = self.opponent_range(

            opponent_name

        )



        if hasattr(action, "value"):
            action_str = str(action.value).lower()
        else:
            action_str = str(action).lower()

        if action_str == "raise":
            opponent.record_raise()
        elif action_str == "bet":
            opponent.record_bet()
        elif action_str == "call":
            opponent.record_call()
        elif action_str == "fold":
            opponent.record_fold()
        elif action_str in ("all_in", "all-in"):
            opponent.record_raise()
        elif action_str == "check":
            opponent.observations += 1

        if opponent_range:
            opponent_range.observe_action(
                action_str,
                position
            )






    # ==========================================
    # New Hand Reset
    # ==========================================

    def new_hand(
        self
    ):
        """
        Called at start of every hand.

        Keeps opponent memory.
        """



        for opponent in self.opponents.values():

            opponent.record_hand()





    # ==========================================
    # Opponent Profiles
    # ==========================================

    def get_opponent_profile(
        self,
        opponent_name
    ):
        """
        Return opponent intelligence.
        """



        opponent = self.opponent_model(

            opponent_name

        )



        opponent_range = self.opponent_range(

            opponent_name

        )



        if opponent is None:

            return None





        return {


            "statistics":

                opponent.ai_profile(),



            "range":

                opponent_range.profile()

                if opponent_range

                else None

        }





    # ==========================================
    # Bot Profile
    # ==========================================

    def profile(
        self
    ):
        """
        Return bot information.
        """



        return {


            "name":

                self.name,



            "difficulty":

                self.difficulty.difficulty.value,



            "strategy":

                self.strategy.strategy.value,



            "opponents_tracked":

                len(

                    self.opponents

                )

        }





    # ==========================================
    # Debug
    # ==========================================

    def __repr__(
        self
    ):

        return (

            f"BotPlayer({self.name})"

        )





    def __str__(
        self
    ):

        return (

            f"AI Bot: {self.name}\n"

            f"Difficulty: "

            f"{self.difficulty.difficulty.value}\n"

            f"Strategy: "

            f"{self.strategy.strategy.value}"

        )
