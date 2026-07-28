from enum import Enum


class Action(Enum):
    """
    Possible poker actions.
    """

    FOLD = "fold"

    CHECK = "check"

    CALL = "call"

    BET = "bet"

    RAISE = "raise"

    ALL_IN = "all_in"



class DecisionEngine:
    """
    AI decision maker.

    Uses:
    • Hand strength
    • Difficulty
    • Strategy
    • Opponent information

    Does NOT:
    • Execute actions
    • Control betting
    """


    def __init__(
        self,
        hand_strength,
        difficulty,
        strategy
    ):

        self.hand_strength = hand_strength

        self.difficulty = difficulty

        self.strategy = strategy



    # ==========================================
    # Basic Decision Rules
    # ==========================================

    def basic_action(
        self,
        strength: int
    ) -> Action:
        """
        Simple rule-based baseline.

        Used by easy AI.
        """


        if strength < 25:

            return Action.FOLD



        if strength < 50:

            return Action.CALL



        if strength < 75:

            return Action.BET



        return Action.RAISE
        # ==========================================
    # Strategy Adjustment
    # ==========================================

    def apply_strategy(
        self,
        action: Action,
        strength: int
    ) -> Action:
        """
        Modify action based on playing style.
        """


        aggression = self.strategy.aggression()

        risk = self.strategy.risk_tolerance()



        # Aggressive players raise more

        if (

            aggression >= 0.8

            and

            strength >= 55

        ):

            return Action.RAISE



        # Passive players avoid big actions

        if (

            aggression <= 0.35

            and

            strength < 75

        ):


            if strength >= 35:

                return Action.CALL


            return Action.FOLD



        # Risk taking players continue more

        if (

            risk >= 0.75

            and

            strength >= 40

        ):

            return Action.CALL



        return action



    # ==========================================
    # Bluffing
    # ==========================================

    def should_bluff(
        self
    ) -> bool:
        """
        Decide whether AI attempts a bluff.
        """

        import random


        frequency = (

            self.strategy.bluff_frequency()

        )


        return random.random() < frequency
        # ==========================================
    # Opponent Adjustment
    # ==========================================

    def opponent_adjustment(
        self,
        action: Action,
        opponent_model=None
    ) -> Action:
        """
        Adjust action based on opponent style.
        """


        if opponent_model is None:

            return action



        opponent_type = (

            opponent_model.classify()

            .value

        )


        # Against aggressive players,
        # allow more calls and traps

        if opponent_type == "loose_aggressive":


            if action == Action.FOLD:

                return Action.CALL



        # Against tight players,
        # increase pressure

        if opponent_type == "tight_passive":


            if action == Action.CALL:

                return Action.BET



        return action



    # ==========================================
    # Final Decision
    # ==========================================

    def decide(
        self,
        strength: int,
        opponent_model=None
    ) -> Action:
        """
        Complete AI decision.

        Returns:
        FOLD
        CHECK
        CALL
        BET
        RAISE
        """


        action = self.basic_action(

            strength

        )


        action = self.apply_strategy(

            action,

            strength

        )


        # Bluff attempt

        if (

            strength < 35

            and

            self.should_bluff()

        ):

            action = Action.BET



        # Opponent adaptation

        if self.difficulty.can_use_opponent_model():

            action = self.opponent_adjustment(

                action,

                opponent_model

            )


        return action



    # ==========================================
    # Debug
    # ==========================================

    def __repr__(self):

        return "DecisionEngine()"