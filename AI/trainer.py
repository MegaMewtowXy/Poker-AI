import json

import os
import tempfile

from datetime import datetime

class Trainer:
    """
    Rule-based reinforcement trainer.

    Responsibilities
    ----------------
    • Store AI experiences
    • Calculate rewards
    • Learn strategy adjustments
    • Maintain training statistics
    • Save/load training memory
    • Apply learned parameters

    Does NOT
    --------
    • Neural network training
    • GPU learning
    • Replace poker strategy
    • Make decisions
    """

    def __init__(
        self,
        learning_rate=0.01
    ):

        self.learning_rate = learning_rate

        # ======================================
        # Learned Parameters
        # ======================================

        self.weights = {

            "aggression":

                0.5,

            "bluff_frequency":

                0.2,

            "risk_tolerance":

                0.5

        }

        # ======================================
        # Experience Memory
        # ======================================

        self.experiences = []
        self._processed_experiences = 0

        # ======================================
        # Statistics
        # ======================================

        self.stats = {

            "games":

                0,

            "wins":

                0,

            "losses":

                0,

            "total_reward":

                0.0

        }

        self.created = str(

            datetime.now()

        )

    # ==========================================
    # Record Experience
    # ==========================================

    def record_experience(
        self,
        state: dict,
        action: str,
        reward: float,
        confidence=0,
        equity=None,
        result=None
    ):
        """
        Store one AI decision experience.
        """

        experience = {

            "state":

                state,

            "action":

                action,

            "reward":

                reward,

            "confidence":

                confidence,

            "equity":

                equity,

            "result":

                result

        }

        self.experiences.append(

            experience

        )

        self.stats["total_reward"] += reward
    
    # ==========================================
    # Reward Calculation
    # ==========================================

    def calculate_reward(
        self,
        chips_change: int
    ) -> float:
        """
        Convert chip result into reward.

        Range:
        -1.0 to +1.0
        """

        if chips_change > 0:

            return min(

                1.0,

                chips_change / 1000

            )

        if chips_change < 0:

            return max(

                -1.0,

                chips_change / 1000

            )

        return 0.0

    # ==========================================
    # Learning
    # ==========================================

    def learn(
        self
    ):
        """
        Adjust AI behaviour
        based on previous experiences.
        """

        pending_experiences = self.experiences[self._processed_experiences:]

        if not pending_experiences:

            return

        for experience in pending_experiences:

            reward = experience.get(

                "reward",

                0

            )

            action = experience.get(

                "action",

                ""

            ).lower()

            adjustment = (

                self.learning_rate

                *

                abs(reward)

            )

            # ==================================
            # Positive Reinforcement
            # ==================================

            if reward > 0:

                self.stats["wins"] += 1

                if action in [

                    "bet",

                    "raise",

                    "all_in"

                ]:

                    self.weights["aggression"] += adjustment

                if action == "bluff":

                    self.weights["bluff_frequency"] += adjustment

                if action in [

                    "call",

                    "check"

                ]:

                    self.weights["risk_tolerance"] += adjustment

            # ==================================
            # Negative Reinforcement
            # ==================================

            elif reward < 0:

                self.stats["losses"] += 1

                if action in [

                    "bet",

                    "raise",

                    "all_in"

                ]:

                    self.weights["aggression"] -= adjustment

                if action == "bluff":

                    self.weights["bluff_frequency"] -= adjustment

                if action in [

                    "call",

                    "check"

                ]:

                    self.weights["risk_tolerance"] -= adjustment

        self.normalize_weights()
        self._processed_experiences = len(self.experiences)

    # ==========================================
    # Weight Normalization
    # ==========================================

    def normalize_weights(
        self
    ):
        """
        Keep learned values stable.
        """

        for key in self.weights:

            self.weights[key] = max(

                0.0,

                min(

                    1.0,

                    self.weights[key]

                )

            )

    # ==========================================
    # Apply Learned Weights
    # ==========================================

    def apply_to_strategy(
        self,
        strategy_manager
    ):
        """
        Apply learned parameters to
        StrategyManager.

        Trainer modifies personality
        parameters only.
        It does not make decisions.
        """

        if strategy_manager is None:

            return False

        if hasattr(

            strategy_manager,

            "set_parameter"

        ):

            strategy_manager.set_parameter(

                "aggression",

                self.weights["aggression"]

            )

            strategy_manager.set_parameter(

                "bluff_frequency",

                self.weights["bluff_frequency"]

            )

            strategy_manager.set_parameter(

                "risk_tolerance",

                self.weights["risk_tolerance"]

            )

            return True

        return False

    # ==========================================
    # Get Learned Weights
    # ==========================================

    def get_weights(
        self
    ):
        """
        Return learned AI parameters.
        """

        return self.weights.copy()

    # ==========================================
    # Training Summary
    # ==========================================

    def statistics(
        self
    ):
        """
        Return training performance.
        """

        total = len(

            self.experiences

        )

        average_reward = 0

        if total > 0:

            average_reward = (

                self.stats["total_reward"]

                /

                total

            )

        return {

            "experiences":

                total,

            "games":

                self.stats["games"],

            "wins":

                self.stats["wins"],

            "losses":

                self.stats["losses"],

            "average_reward":

                round(

                    average_reward,

                    3

                ),

            "weights":

                self.weights.copy()

        }
    
    # ==========================================
    # Save Training Data
    # ==========================================

    def save(
        self,
        path="data/training_data/trainer.json"
    ):
        """
        Save trainer memory.
        """

        directory = os.path.dirname(

            path

        )

        if directory:

            os.makedirs(

                directory,

                exist_ok=True

            )

        data = {

            "version":

                1,

            "created":

                self.created,

            "weights":

                self.weights,

            "statistics":

                self.stats,

            "experiences":

                self.experiences

        }

        # Write then replace so an interrupted save cannot corrupt the
        # previous training file.
        file_descriptor, temporary_path = tempfile.mkstemp(
            dir=directory or None,
            prefix="trainer_",
            suffix=".json"
        )
        try:
            with os.fdopen(file_descriptor, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, default=str)
            os.replace(temporary_path, path)
        except Exception:
            if os.path.exists(temporary_path):
                os.unlink(temporary_path)
            raise

    # ==========================================
    # Load Training Data
    # ==========================================

    def load(
        self,
        path="data/training_data/trainer.json"
    ):
        """
        Load previous learning.
        """

        if not os.path.exists(

            path

        ):

            return False

        with open(

            path,

            "r"

        ) as file:

            data = json.load(

                file

            )

        self.weights = data.get(

            "weights",

            self.weights

        )

        self.stats = data.get(

            "statistics",

            self.stats

        )

        self.experiences = data.get(

            "experiences",

            []

        )
        # Saved experiences may not have been applied in a previous process.
        self._processed_experiences = 0

        self.created = data.get(

            "created",

            str(datetime.now())

        )

        self.normalize_weights()

        return True

    # ==========================================
    # Reset Training
    # ==========================================

    def reset(
        self
    ):
        """
        Clear all learned behaviour.
        """

        self.experiences.clear()
        self._processed_experiences = 0

        self.weights = {

            "aggression":

                0.5,

            "bluff_frequency":

                0.2,

            "risk_tolerance":

                0.5

        }

        self.stats = {

            "games":

                0,

            "wins":

                0,

            "losses":

                0,

            "total_reward":

                0.0

        }

        self.created = str(

            datetime.now()

        )

    # ==========================================
    # Profile
    # ==========================================

    def profile(
        self
    ):
        """
        Trainer information.
        """

        return {

            "experiences":

                len(

                    self.experiences

                ),

            "learning_rate":

                self.learning_rate,

            "weights":

                self.weights.copy(),

            "statistics":

                self.statistics()

        }

    # ==========================================
    # Debug
    # ==========================================

    def __repr__(
        self
    ):

        return (

            "Trainer()"

        )

    def __str__(
        self
    ):

        return (

            "Rule Based Poker AI Trainer"

        )
