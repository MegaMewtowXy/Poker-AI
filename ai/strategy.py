from enum import Enum





class Strategy(Enum):
    """
    Poker AI playing personalities.

    Controls:
    - aggression
    - bluff frequency
    - risk tolerance
    - range width
    - pressure style
    """



    TIGHT_AGGRESSIVE = "tight_aggressive"

    LOOSE_AGGRESSIVE = "loose_aggressive"

    TIGHT_PASSIVE = "tight_passive"

    BALANCED = "balanced"

    ADAPTIVE = "adaptive"







class StrategyConfig:
    """
    Configuration for AI personalities.
    """



    CONFIG = {




        Strategy.TIGHT_AGGRESSIVE: {


            "range_width": 0.20,

            "aggression": 0.85,

            "bluff_frequency": 0.15,

            "risk_tolerance": 0.60,

            "pressure_factor": 0.80,

            "adaptability": 0.50,


            "description":

                "Selective starting range with strong aggression"

        },





        Strategy.LOOSE_AGGRESSIVE: {


            "range_width": 0.45,

            "aggression": 0.95,

            "bluff_frequency": 0.30,

            "risk_tolerance": 0.85,

            "pressure_factor": 1.00,

            "adaptability": 0.70,


            "description":

                "Wide range, high pressure and frequent aggression"

        },





        Strategy.TIGHT_PASSIVE: {


            "range_width": 0.18,

            "aggression": 0.30,

            "bluff_frequency": 0.05,

            "risk_tolerance": 0.25,

            "pressure_factor": 0.30,

            "adaptability": 0.30,


            "description":

                "Selective defensive playing style"

        },





        Strategy.BALANCED: {


            "range_width": 0.30,

            "aggression": 0.55,

            "bluff_frequency": 0.20,

            "risk_tolerance": 0.50,

            "pressure_factor": 0.55,

            "adaptability": 0.80,


            "description":

                "Balanced strategy adapting to situations"

        },





        Strategy.ADAPTIVE: {


            "range_width": 0.35,

            "aggression": 0.60,

            "bluff_frequency": 0.25,

            "risk_tolerance": 0.55,

            "pressure_factor": 0.60,

            "adaptability": 1.00,


            "description":

                "Changes behaviour based on opponents"

        }

    }





    @classmethod
    def get_config(
        cls,
        strategy: Strategy
    ) -> dict:
        """
        Return strategy configuration.
        """

        return cls.CONFIG.get(

            strategy,

            cls.CONFIG[Strategy.BALANCED]

        )





    @classmethod
    def available_strategies(
        cls
    ):

        return list(

            cls.CONFIG.keys()

        )









class StrategyManager:
    """
    Handles AI playing personality.

    Responsibilities
    ----------------
    • Provide aggression level
    • Provide bluff frequency
    • Provide risk tolerance
    • Provide range width
    • Provide pressure behaviour
    • Provide adaptability
    • Accept runtime learning adjustments

    Does NOT:
        • Make decisions
        • Control betting
    """





    def __init__(
        self,
        strategy: Strategy = Strategy.BALANCED
    ):

        self.strategy = strategy


        # Runtime changes from Trainer
        # without modifying base strategy

        self.overrides = {}







    # ==========================================
    # Configuration
    # ==========================================

    def config(
        self
    ):

        return StrategyConfig.get_config(

            self.strategy

        )







    # ==========================================
    # Generic Parameter
    # ==========================================

    def get_parameter(
        self,
        name,
        default=0.0
    ):
        """
        Get strategy parameter.

        Runtime learned values have priority.
        """



        if name in self.overrides:

            return self.overrides[name]



        return self.config().get(

            name,

            default

        )







    # ==========================================
    # Trainer Integration
    # ==========================================

    def set_parameter(
        self,
        name,
        value
    ):
        """
        Apply learned parameter.

        Used by Trainer.

        Does not modify original
        StrategyConfig.
        """



        if name not in self.config():
            raise ValueError(f"Unknown strategy parameter: {name}")

        if not isinstance(value, (int, float)):
            raise ValueError(f"Strategy parameter {name} must be numeric")

        # All current tunable strategy parameters are normalized values.
        self.overrides[name] = max(0.0, min(1.0, float(value)))


        return True





    def reset_overrides(
        self
    ):
        """
        Remove learned adjustments.
        """

        self.overrides.clear()







    # ==========================================
    # Behaviour Parameters
    # ==========================================

    def aggression(
        self
    ):

        return self.get_parameter(

            "aggression",

            0.5

        )





    def bluff_frequency(
        self
    ):

        return self.get_parameter(

            "bluff_frequency",

            0.1

        )





    def risk_tolerance(
        self
    ):

        return self.get_parameter(

            "risk_tolerance",

            0.5

        )





    def range_width(
        self
    ):

        return self.get_parameter(

            "range_width",

            0.30

        )





    def pressure_factor(
        self
    ):

        return self.get_parameter(

            "pressure_factor",

            0.5

        )





    def adaptability(
        self
    ):

        return self.get_parameter(

            "adaptability",

            0.5

        )







    # ==========================================
    # Strategy Switching
    # ==========================================

    def change_strategy(
        self,
        strategy: Strategy
    ):

        self.strategy = strategy


        self.reset_overrides()







    # ==========================================
    # Profile
    # ==========================================

    def profile(
        self
    ):

        config = self.config()


        return {


            "strategy":

                self.strategy.value,



            "range_width":

                self.range_width(),



            "aggression":

                self.aggression(),



            "bluff_frequency":

                self.bluff_frequency(),



            "risk_tolerance":

                self.risk_tolerance(),



            "pressure_factor":

                self.pressure_factor(),



            "adaptability":

                self.adaptability(),



            "overrides":

                self.overrides.copy(),



            "description":

                config.get(

                    "description",

                    ""

                )

        }







    # ==========================================
    # Debug
    # ==========================================

    def __str__(self):

        return (

            f"AI Strategy: "

            f"{self.strategy.value}"

        )





    def __repr__(self):

        return (

            f"StrategyManager("

            f"{self.strategy.value})"

        )
