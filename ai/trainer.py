import random
import json
import os

class Trainer:
    """
    Self reinforcement trainer.

    Responsibilities
    ----------------
    • Store AI experiences
    • Calculate rewards
    • Adjust strategy weights

    This is NOT:
        • Neural network training
        • GPU based learning
    """


    def __init__(self):

        self.experiences = []


        # Adjustable AI parameters

        self.weights = {

            "aggression": 0.5,

            "bluff_frequency": 0.2,

            "risk_tolerance": 0.5

        }



    # ==========================================
    # Experience Recording
    # ==========================================

    def record_experience(
        self,
        state: dict,
        action: str,
        reward: float
    ):
        """
        Store a completed decision.
        """


        self.experiences.append(

            {

                "state": state,

                "action": action,

                "reward": reward

            }

        )



    # ==========================================
    # Reward Calculation
    # ==========================================

    def calculate_reward(
        self,
        chips_change: int
    ) -> float:
        """
        Convert chip result into reward.
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
        Update strategy weights
        based on experience.
        """


        if not self.experiences:

            return



        for experience in self.experiences:


            reward = experience["reward"]

            action = experience["action"]



            # Positive outcome

            if reward > 0:


                if action in [

                    "bet",

                    "raise"

                ]:

                    self.weights["aggression"] += 0.01



                if action == "bluff":

                    self.weights["bluff_frequency"] += 0.01



            # Negative outcome

            elif reward < 0:


                if action in [

                    "bet",

                    "raise"

                ]:

                    self.weights["aggression"] -= 0.01



                if action == "bluff":

                    self.weights["bluff_frequency"] -= 0.01



        self.normalize_weights()



    # ==========================================
    # Weight Control
    # ==========================================

    def normalize_weights(
        self
    ):
        """
        Keep weights between 0 and 1.
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
    # Access
    # ==========================================

    def get_weights(
        self
    ) -> dict:
        """
        Return current learned parameters.
        """

        return self.weights.copy()
        # ==========================================
    # Save Training Data
    # ==========================================

    def save(
        self,
        path="data/training_data/trainer.json"
    ):
        """
        Save experiences and weights.
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

            "weights":

                self.weights,


            "experiences":

                self.experiences

        }


        with open(
            path,
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )



    # ==========================================
    # Load Training Data
    # ==========================================

    def load(
        self,
        path="data/training_data/trainer.json"
    ):
        """
        Load previous training.
        """

        if not os.path.exists(path):

            return



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


        self.experiences = data.get(

            "experiences",

            []

        )



    # ==========================================
    # Statistics
    # ==========================================

    def statistics(
        self
    ):
        """
        Training summary.
        """

        total = len(

            self.experiences

        )


        if total == 0:

            return {

                "experiences": 0,

                "average_reward": 0

            }



        rewards = [

            exp["reward"]

            for exp in self.experiences

        ]


        return {

            "experiences":

                total,


            "average_reward":

                round(

                    sum(rewards)

                    /

                    total,

                    3

                ),


            "weights":

                self.weights.copy()

        }



    # ==========================================
    # Reset
    # ==========================================

    def reset(
        self
    ):
        """
        Clear training memory.
        """

        self.experiences.clear()


        self.weights = {

            "aggression": 0.5,

            "bluff_frequency": 0.2,

            "risk_tolerance": 0.5

        }



    # ==========================================
    # Debug
    # ==========================================

    def __repr__(self):

        return "Trainer()" 