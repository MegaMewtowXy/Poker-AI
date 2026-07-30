from AI.bot_player import BotPlayer

from AI.game_context import GameContext

from models.action import Action

class BotController:
    """
    Final AI game controller.

    Responsibilities
    ----------------
    • Connect game engine with BotPlayer
    • Request decisions
    • Validate decisions
    • Execute actions
    • Maintain decision history

    Does NOT
    --------
    • Decide strategy
    • Calculate poker analysis
    • Evaluate hands
    • Calculate bets
    """

    def __init__(
        self,
        bot: BotPlayer
    ):

        self.bot = bot

        self.last_decision = None

        self.history = []

    # ==========================================
    # Request AI Decision
    # ==========================================

    def get_action(
        self,
        context: GameContext,
        opponent_name=None
    ):
        """
        Ask BotPlayer for decision.
        """

        decision = self.bot.decide(

            context,

            opponent_name

        )

        self.last_decision = decision

        self.history.append(

            decision

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
        Ensure decision format is valid.
        """

        required = [

            "action",

            "amount"

        ]

        for field in required:

            if field not in decision:

                raise ValueError(

                    f"Missing decision field: {field}"

                )

        if not isinstance(

            decision["action"],

            Action

        ):

            raise ValueError(

                "Invalid action type"

            )

        if decision["amount"] < 0:

            raise ValueError(

                "Invalid bet amount"

            )

        return True

    # ==========================================
    # Action Name
    # ==========================================

    def action_name(
        self,
        action: Action
    ) -> str:
        """
        Convert action enum to readable name.
        """

        return action.name.lower()

    # ==========================================
    # Execute Action
    # ==========================================

    def execute_action(
        self,
        decision,
        player,
        betting_manager
    ):
        """
        Execute AI decision through game engine.

        Controller only forwards actions.
        It does NOT decide.
        """

        self.validate_decision(

            decision

        )

        action = decision["action"]

        amount = decision.get(

            "amount",

            0

        )

        if action == Action.FOLD:

            betting_manager.fold(

                player

            )

        elif action == Action.CHECK:

            betting_manager.check(

                player

            )

        elif action == Action.CALL:

            betting_manager.call(

                player

            )

        elif action == Action.BET:

            betting_manager.bet(

                player,

                amount

            )

        elif action == Action.RAISE:

            betting_manager.raise_bet(

                player,

                amount

            )

        elif action == Action.ALL_IN:

            betting_manager.all_in(

                player

            )

        else:

            raise ValueError(

                f"Unsupported action: {action}"

            )

        return True

    # ==========================================
    # History
    # ==========================================

    def get_history(
        self
    ):
        """
        Return decision history.
        """

        return self.history.copy()

    def reset_history(
        self
    ):
        """
        Reset history for simulations.
        """

        self.history.clear()

        self.last_decision = None

    # ==========================================
    # Last Decision
    # ==========================================

    def get_last_decision(
        self
    ):
        """
        Return latest AI decision.
        """

        return self.last_decision

    # ==========================================
    # Profile
    # ==========================================

    def profile(
        self
    ):
        """
        Controller information.
        """

        return {

            "bot":

                self.bot.name,

            "decisions_made":

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

            f"BotController({self.bot.name})"

        )