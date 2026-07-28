from enum import Enum


class Difficulty(Enum):
    """
    AI difficulty levels.

    Controls how much information
    the bot uses while making decisions.
    """


    EASY = "easy"

    MEDIUM = "medium"

    HARD = "hard"

    EXPERT = "expert"



class DifficultyConfig:
    """
    Configuration for each AI level.

    Higher difficulty enables
    more advanced AI features.
    """


    CONFIG = {


        Difficulty.EASY: {

            "use_probability": False,

            "use_opponent_model": False,

            "use_bluffing": False,

            "use_adaptation": False,

            "mistake_rate": 0.30

        },


        Difficulty.MEDIUM: {

            "use_probability": True,

            "use_opponent_model": False,

            "use_bluffing": False,

            "use_adaptation": False,

            "mistake_rate": 0.15

        },


        Difficulty.HARD: {

            "use_probability": True,

            "use_opponent_model": True,

            "use_bluffing": True,

            "use_adaptation": True,

            "mistake_rate": 0.05

        },


        Difficulty.EXPERT: {

            "use_probability": True,

            "use_opponent_model": True,

            "use_bluffing": True,

            "use_adaptation": True,

            "use_self_training": True,

            "mistake_rate": 0.01

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



class DifficultyManager:
    """
    Manages AI difficulty settings.
    """


    def __init__(
        self,
        difficulty: Difficulty
    ):

        self.difficulty = difficulty


    # ==========================================
    # Configuration
    # ==========================================

    def config(self) -> dict:
        """
        Get current AI settings.
        """

        return DifficultyConfig.get_config(

            self.difficulty

        )


    # ==========================================
    # Feature Checks
    # ==========================================

    def can_use_probability(self) -> bool:

        return self.config().get(

            "use_probability",

            False

        )


    def can_use_opponent_model(self) -> bool:

        return self.config().get(

            "use_opponent_model",

            False

        )


    def can_bluff(self) -> bool:

        return self.config().get(

            "use_bluffing",

            False

        )


    def can_adapt(self) -> bool:

        return self.config().get(

            "use_adaptation",

            False

        )


    def can_self_train(self) -> bool:

        return self.config().get(

            "use_self_training",

            False

        )


    # ==========================================
    # Utility
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