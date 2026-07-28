from enum import Enum


class Strategy(Enum):
    """
    Poker playing styles.
    """


    TIGHT_AGGRESSIVE = "tight_aggressive"

    LOOSE_AGGRESSIVE = "loose_aggressive"

    TIGHT_PASSIVE = "tight_passive"

    BALANCED = "balanced"



class StrategyConfig:
    """
    Configuration for each playing style.
    """


    CONFIG = {


        Strategy.TIGHT_AGGRESSIVE: {

            "starting_hand_range": 0.20,

            "aggression": 0.85,

            "bluff_frequency": 0.15,

            "risk_tolerance": 0.60

        },


        Strategy.LOOSE_AGGRESSIVE: {

            "starting_hand_range": 0.45,

            "aggression": 0.95,

            "bluff_frequency": 0.30,

            "risk_tolerance": 0.85

        },


        Strategy.TIGHT_PASSIVE: {

            "starting_hand_range": 0.18,

            "aggression": 0.30,

            "bluff_frequency": 0.05,

            "risk_tolerance": 0.25

        },


        Strategy.BALANCED: {

            "starting_hand_range": 0.30,

            "aggression": 0.55,

            "bluff_frequency": 0.20,

            "risk_tolerance": 0.50

        }

    }


    @classmethod
    def get_config(
        cls,
        strategy: Strategy
    ) -> dict:
        """
        Return strategy parameters.
        """

        return cls.CONFIG.get(

            strategy,

            cls.CONFIG[Strategy.BALANCED]

        )



class StrategyManager:
    """
    Handles AI playing style.
    """


    def __init__(
        self,
        strategy: Strategy
    ):

        self.strategy = strategy


    # ==========================================
    # Configuration
    # ==========================================

    def config(self) -> dict:
        """
        Get current strategy settings.
        """

        return StrategyConfig.get_config(

            self.strategy

        )


    # ==========================================
    # Behaviour
    # ==========================================

    def aggression(
        self
    ) -> float:

        return self.config().get(

            "aggression",

            0.5

        )


    def bluff_frequency(
        self
    ) -> float:

        return self.config().get(

            "bluff_frequency",

            0.1

        )


    def risk_tolerance(
        self
    ) -> float:

        return self.config().get(

            "risk_tolerance",

            0.5

        )


    def starting_hand_range(
        self
    ) -> float:

        return self.config().get(

            "starting_hand_range",

            0.30

        )


    # ==========================================
    # Utility
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