from AI.bot_player import BotPlayer
from models.action import Action


class BotController:
    """
    Connects AI decisions with game engine actions.

    Responsibilities
    ----------------
    • Ask bot for decisions
    • Convert AI actions into engine actions

    Does NOT:
        • Manage game rules
        • Modify chips directly
        • Handle betting logic
    """


    def __init__(
        self,
        bot: BotPlayer
    ):

        self.bot = bot


    # ==========================================
    # Decision Request
    # ==========================================

    def get_action(
        self,
        hole_cards,
        community_cards,
        opponent_count,
        position=None,
        opponent_name=None
    ):
        """
        Ask AI what action to take.
        """

        result = self.bot.decide(

            hole_cards,

            community_cards,

            opponent_count,

            position,

            opponent_name

        )


        return result["action"]



    # ==========================================
    # Action Conversion
    # ==========================================

    def action_name(
        self,
        action: Action
    ) -> str:
        """
        Convert enum action to engine-readable text.
        """

        return action.value
        # ==========================================
    # Execute Action
    # ==========================================

    def execute_action(
        self,
        action: Action,
        player,
        betting_manager,
        amount=0
    ):
        """
        Execute AI chosen action
        through the engine.

        Engine remains responsible
        for validation.
        """


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

                f"Unknown action: {action}"

            )