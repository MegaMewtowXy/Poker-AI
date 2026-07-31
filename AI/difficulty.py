from enum import Enum

class Difficulty(Enum):
    """
    AI difficulty levels.

    Controls:
    - Intelligence features
    - Accuracy
    - Simulation depth
    - Mistake rate
    """

    EASY = "easy"

    MEDIUM = "medium"

    HARD = "hard"

    EXPERT = "expert"

class DifficultyConfig:
    """
    Configuration for each AI level.

    Controls:
    - Intelligence features
    - Accuracy
    - Aggression
    - Bluff frequency
    - Simulation depth
    - Strategy influence
    """

    CONFIG = {

        # ======================================
        # Easy AI
        # ======================================

        Difficulty.EASY: {

            "use_probability":

                False,

            "use_opponent_model":

                False,

            "use_bluffing":

                False,

            "use_adaptation":

                False,

            "use_self_training":

                False,

            "equity_simulations":

                100,

            "mistake_rate":

                0.30,

            "bluff_multiplier":

                0.5,

            "aggression_modifier":

                0.8,

            "strategy_weight":

                0.5

        },

        # ======================================
        # Medium AI
        # ======================================

        Difficulty.MEDIUM: {

            "use_probability":

                True,

            "use_opponent_model":

                False,

            "use_bluffing":

                True,

            "use_adaptation":

                False,

            "use_self_training":

                False,

            "equity_simulations":

                500,

            "mistake_rate":

                0.15,

            "bluff_multiplier":

                0.75,

            "aggression_modifier":

                1.0,

            "strategy_weight":

                0.75

        },

        # ======================================
        # Hard AI
        # ======================================

        Difficulty.HARD: {

            "use_probability":

                True,

            "use_opponent_model":

                True,

            "use_bluffing":

                True,

            "use_adaptation":

                True,

            "use_self_training":

                False,

            "equity_simulations":

                2000,

            "mistake_rate":

                0.05,

            "bluff_multiplier":

                1.0,

            "aggression_modifier":

                1.15,

            "strategy_weight":

                1.0

        },

        # ======================================
        # Expert AI
        # ======================================

        Difficulty.EXPERT: {

            "use_probability":

                True,

            "use_opponent_model":

                True,

            "use_bluffing":

                True,

            "use_adaptation":

                True,

            "use_self_training":

                True,

            "equity_simulations":

                5000,

            "mistake_rate":

                0.01,

            "bluff_multiplier":

                1.2,

            "aggression_modifier":

                1.25,

            "strategy_weight":

                1.0

        }

    }

    @classmethod
    def get_config(
        cls,
        difficulty: Difficulty
    ) -> dict:
        """
        Return configuration
        for selected difficulty.
        """

        return cls.CONFIG.get(

            difficulty,

            cls.CONFIG[Difficulty.MEDIUM]

        )

    @classmethod
    def available_difficulties(
        cls
    ):
        """
        Return available AI levels.
        """

        return list(

            cls.CONFIG.keys()

        )
class DifficultyManager:
    """
    Manages AI difficulty settings.

    Responsible for:
    - Providing difficulty configuration
    - Checking enabled AI features
    - Providing AI behaviour modifiers

    Does NOT:
    - Make decisions
    - Control strategy
    - Execute actions
    """

    def __init__(
        self,
        difficulty=Difficulty.MEDIUM
    ):

        self.difficulty = difficulty

    # ==========================================
    # Configuration
    # ==========================================

    def config(
        self
    ) -> dict:
        """
        Get current AI settings.
        """

        return DifficultyConfig.get_config(

            self.difficulty

        )

    # ==========================================
    # Generic Parameter Access
    # ==========================================

    def get_parameter(
        self,
        name,
        default=None
    ):
        """
        Get any difficulty parameter.
        """

        return self.config().get(

            name,

            default

        )

    # ==========================================
    # Feature Checks
    # ==========================================

    def can_use_probability(
        self
    ) -> bool:

        return self.get_parameter(

            "use_probability",

            False

        )

    def can_use_opponent_model(
        self
    ) -> bool:

        return self.get_parameter(

            "use_opponent_model",

            False

        )

    def can_bluff(
        self
    ) -> bool:

        return self.get_parameter(

            "use_bluffing",

            False

        )

    def can_adapt(
        self
    ) -> bool:

        return self.get_parameter(

            "use_adaptation",

            False

        )

    def can_self_train(
        self
    ) -> bool:

        return self.get_parameter(

            "use_self_training",

            False

        )

    # ==========================================
    # AI Parameters
    # ==========================================

    def equity_simulations(
        self
    ) -> int:

        return self.get_parameter(

            "equity_simulations",

            500

        )

    def bluff_multiplier(
        self
    ) -> float:

        return self.get_parameter(

            "bluff_multiplier",

            1.0

        )

    def aggression_modifier(
        self
    ) -> float:

        return self.get_parameter(

            "aggression_modifier",

            1.0

        )

    def strategy_weight(
        self
    ) -> float:
        """
        How much AI trusts strategy module.
        """

        return self.get_parameter(

            "strategy_weight",

            1.0

        )

    def mistake_rate(
        self
    ) -> float:

        return self.get_parameter(

            "mistake_rate",

            0.1

        )

    # ==========================================
    # Difficulty Change
    # ==========================================

    def change_difficulty(
        self,
        difficulty: Difficulty
    ):
        """
        Change AI difficulty.
        """

        if not isinstance(difficulty, Difficulty):
            raise ValueError("difficulty must be a Difficulty value")

        self.difficulty = difficulty

    # ==========================================
    # Profile
    # ==========================================

    def profile(
        self
    ):
        """
        Complete difficulty profile.
        """

        return {

            "difficulty":

                self.difficulty.value,

            "equity_simulations":

                self.equity_simulations(),

            "probability":

                self.can_use_probability(),

            "opponent_model":

                self.can_use_opponent_model(),

            "bluffing":

                self.can_bluff(),

            "adaptation":

                self.can_adapt(),

            "self_training":

                self.can_self_train(),

            "strategy_weight":

                self.strategy_weight(),

            "aggression_modifier":

                self.aggression_modifier(),

            "bluff_multiplier":

                self.bluff_multiplier(),

            "mistake_rate":

                self.mistake_rate()

        }

    # ==========================================
    # Debug
    # ==========================================

    def __str__(self):

        return (

            f"AI Difficulty: "

            f"{self.difficulty.value}"

        )

    def __repr__(self):

        return (

            f"DifficultyManager("

            f"{self.difficulty.value})"

        )
