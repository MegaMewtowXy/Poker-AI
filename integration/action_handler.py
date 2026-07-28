from AI.bot_controller import BotController

from AI.bot_player import BotPlayer

from AI.game_context import GameContext

from models.action import Action





class ActionHandler:
    """
    Final AI action bridge.

    Connects:

    Poker Engine
          |
          ↓
    ActionHandler
          |
          ↓
    BotController
          |
          ↓
    BotPlayer


    Responsibilities
    ----------------
    • Register AI players
    • Create GameContext
    • Request decisions
    • Forward actions


    Does NOT:
        • Decide strategy
        • Calculate poker logic
        • Manage rules
    """





    def __init__(
        self,
        betting_engine
    ):

        self.betting_engine = betting_engine


        self.controllers = {}


        self.history = []





    # ==========================================
    # Register Bot
    # ==========================================

    def register_bot(
        self,
        player,
        bot: BotPlayer
    ):
        """
        Attach AI to engine player.
        """


        self.controllers[player] = BotController(

            bot

        )





    # ==========================================
    # Remove Bot
    # ==========================================

    def remove_bot(
        self,
        player
    ):
        """
        Remove AI controller.
        """


        if player in self.controllers:

            del self.controllers[player]





    # ==========================================
    # Get Controller
    # ==========================================

    def get_controller(
        self,
        player
    ):
        """
        Return bot controller.
        """


        return self.controllers.get(

            player

        )





    # ==========================================
    # Create Context
    # ==========================================

    def create_context(
        self,
        player,
        table,
        position=None,
        street="pre_flop"
    ):
        """
        Convert engine state into AI state.

        Creates GameContext used by:

        • DecisionEngine
        • EquityCalculator
        • BoardAnalyzer
        • Strategy
        """


        return GameContext(


            hole_cards=player.hand,


            community_cards=table.community_cards,


            position=position,


            street=street,


            pot_size=table.pot,


            current_bet=table.current_bet,
            player_current_bet=player.current_bet,

            call_amount=max(
        0,
        table.current_bet - player.current_bet
    ),
            min_raise=table.minimum_raise,



            big_blind=getattr(

                table,

                "big_blind",

                0

            ),



            player_stack=player.chips,


            players_remaining=len(

                table.players

            )

        )
    
    # ==========================================
    # Handle AI Turn
    # ==========================================

    def handle_action(
        self,
        player,
        table,
        position=None,
        street="pre_flop",
        opponent_name=None
    ):
        """
        Request and process AI decision.

        Flow:

        Engine
          |
          v
        ActionHandler
          |
          v
        BotController
          |
          v
        BotPlayer
          |
          v
        DecisionEngine
        """



        controller = self.controllers.get(

            player

        )



        if controller is None:

            raise ValueError(

                "No AI controller registered."

            )





        # ======================================
        # Create AI Context
        # ======================================

        context = self.create_context(

            player,

            table,

            position,

            street

        )





        # ======================================
        # Request Decision
        # ======================================

        decision = controller.get_action(

            context,

            opponent_name

        )





        # ======================================
        # Validate Decision
        # ======================================

        self.validate_decision(

            decision

        )





        # ======================================
        # Store History
        # ======================================

        self.history.append(

            decision

        )





        # ======================================
        # Execute Through Controller
        # ======================================

        controller.execute_action(

            decision,

            player,

            self.betting_engine

        )





        return decision





    # ==========================================
    # Validate Decision
    # ==========================================

    def validate_decision(
        self,
        decision
    ):
        """
        Validate AI decision format.

        Checks:

        • Decision exists
        • Action exists
        • Action is valid enum
        • Bet amount is valid
        """



        if not decision:

            raise ValueError(

                "Empty decision received."

            )





        required_fields = [

            "action",

            "amount"

        ]





        for field in required_fields:


            if field not in decision:


                raise ValueError(

                    f"Missing decision field: {field}"

                )





        if not isinstance(

            decision["action"],

            Action

        ):


            raise ValueError(

                "Invalid action type."

            )





        amount = decision.get(

            "amount",

            0

        )





        if amount < 0:


            raise ValueError(

                "Invalid bet amount."

            )





        return True
    
    # ==========================================
    # Execute Decision
    # ==========================================

    def execute(
        self,
        player,
        decision
    ):
        """
        Execute AI decision.

        Uses betting engine only.

        Does NOT:
        • Decide action
        • Calculate strategy
        • Modify AI logic
        """



        self.validate_decision(

            decision

        )





        action = decision["action"]



        amount = decision.get(

            "amount",

            0

        )





        # ======================================
        # Fold
        # ======================================

        if action == Action.FOLD:


            self.betting_engine.fold(

                player

            )





        # ======================================
        # Check
        # ======================================

        elif action == Action.CHECK:


            self.betting_engine.check(

                player

            )





        # ======================================
        # Call
        # ======================================

        elif action == Action.CALL:


            self.betting_engine.call(

                player

            )





        # ======================================
        # Bet
        # ======================================

        elif action == Action.BET:


            self.betting_engine.bet(

                player,

                amount

            )





        # ======================================
        # Raise
        # ======================================

        elif action == Action.RAISE:


            self.betting_engine.raise_bet(

                player,

                amount

            )





        # ======================================
        # All In
        # ======================================

        elif action == Action.ALL_IN:


            self.betting_engine.all_in(

                player

            )





        else:


            raise ValueError(

                f"Unknown action: {action}"

            )





        return True





    # ==========================================
    # History
    # ==========================================

    def get_history(
        self
    ):
        """
        Return AI action history.
        """


        return self.history.copy()





    # ==========================================
    # Clear History
    # ==========================================

    def clear_history(
        self
    ):
        """
        Clear stored actions.
        """


        self.history.clear()





    # ==========================================
    # Simulation Reset
    # ==========================================

    def reset(
        self
    ):
        """
        Reset handler state.

        Used for:

        • Bot vs Bot simulation
        • Tournament runs
        • Testing
        """


        self.history.clear()





    # ==========================================
    # Profile
    # ==========================================

    def profile(
        self
    ):
        """
        Handler information.
        """



        return {


            "registered_bots":

                len(

                    self.controllers

                ),



            "actions_processed":

                len(

                    self.history

                )

        }





    # ==========================================
    # Debug
    # ==========================================

    def __repr__(
        self
    ):

        return (

            f"ActionHandler("

            f"bots={len(self.controllers)})"

        )