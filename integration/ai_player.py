from models.player import Player

from AI.bot_player import BotPlayer





class AIPlayer(Player):
    """
    Engine-compatible AI player.

    This class connects the poker engine
    Player model with the AI brain.

    Responsibilities
    ----------------
    • Behave like normal Player for engine
    • Forward decisions to BotPlayer
    • Expose AI profile information


    Does NOT:
        • Calculate hand strength
        • Decide actions itself
        • Manage betting rules
        • Control game flow
    """





    def __init__(
        self,
        name: str,
        bot: BotPlayer,
        chips: int = 1000
    ):

        super().__init__(

            name,

            chips,

            is_ai=True

        )


        self.bot = bot





    # ==========================================
    # AI Decision
    # ==========================================

    def decide(
        self,
        context,
        opponent_name=None
    ):
        """
        Ask AI brain for decision.

        Engine creates context.
        AI decides action.

        Supports opponent modelling.
        """

        return self.bot.decide(

            context,

            opponent_name

        )





    # ==========================================
    # AI Properties
    # ==========================================

    @property
    def difficulty(
        self
    ):
        """
        Return AI difficulty level.
        """

        return self.bot.difficulty.difficulty





    @property
    def strategy(
        self
    ):
        """
        Return AI strategy type.
        """

        return self.bot.strategy.strategy





    # ==========================================
    # Profile
    # ==========================================

    def profile(
        self
    ):
        """
        Return AI information.
        """

        return {


            "name":

                self.name,


            "chips":

                self.chips,


            "difficulty":

                self.difficulty.value
                if hasattr(
                    self.difficulty,
                    "value"
                )
                else self.difficulty,



            "strategy":

                self.strategy.value
                if hasattr(
                    self.strategy,
                    "value"
                )
                else self.strategy,



            "bot":

                self.bot.profile()

        }





    # ==========================================
    # Reset
    # ==========================================

    def reset_for_round(
        self
    ):
        """
        Reset player state.

        Keeps AI memory.
        """

        super().reset_for_round()





    # ==========================================
    # Display
    # ==========================================

    def __str__(
        self
    ):

        return (

            f"{self.name} [AI] | "

            f"Chips: ${self.chips}"

        )





    # ==========================================
    # Debug
    # ==========================================

    def __repr__(
        self
    ):

        return (

            f"AIPlayer("

            f"name='{self.name}'"

            f")"

        )