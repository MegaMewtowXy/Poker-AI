class BluffEngine:
    """
    Final poker bluff evaluation engine.

    Responsibilities
    ----------------
    • Evaluate bluff profitability
    • Calculate bluff frequency
    • Analyse bluff conditions
    • Estimate bluff confidence

    Uses
    ----
    • Position
    • Board texture
    • Equity
    • Opponent profile
    • Opponent range
    • Strategy
    • Difficulty

    Does NOT
    --------
    • Decide final action
    • Execute bluff
    • Control game state
    """



    def __init__(
        self,
        strategy=None,
        difficulty=None
    ):

        self.strategy = strategy

        self.difficulty = difficulty



    # ==========================================
    # Safe Access
    # ==========================================

    def get_strategy_value(
        self,
        method,
        default=0.2
    ):
        """
        Safely access strategy values.
        """

        if self.strategy is None:

            return default



        function = getattr(

            self.strategy,

            method,

            None

        )



        if callable(function):

            return function()



        return default




    def get_difficulty_value(
        self,
        method,
        default=1.0
    ):
        """
        Safely access difficulty values.
        """

        if self.difficulty is None:

            return default



        function = getattr(

            self.difficulty,

            method,

            None

        )



        if callable(function):

            return function()



        return default




    # ==========================================
    # Position Factor
    # ==========================================

    def position_factor(
        self,
        position
    ):
        """
        Late position improves bluff success.
        """

        position = str(

            position

        ).upper()



        if "BUTTON" in position:

            return 3



        if "CO" in position:

            return 2



        if "HIJACK" in position:

            return 1



        if "UTG" in position:

            return -2



        return 0




    # ==========================================
    # Board Factor
    # ==========================================

    def board_factor(
        self,
        board_analysis
    ):
        """
        Evaluate board suitability
        for bluffing.
        """

        if not board_analysis:

            return 0



        score = 0



        texture = board_analysis.get(

            "texture",

            ""

        )



        danger = board_analysis.get(

            "danger_level",

            0

        )




        if texture == "dry":

            score += 3



        elif texture == "wet":

            score -= 2



        elif texture == "semi_wet":

            score += 1




        if danger >= 5:

            score -= 2



        return score




    # ==========================================
    # Opponent Factor
    # ==========================================

    def opponent_factor(
        self,
        opponent_profile
    ):
        """
        Evaluate opponent weakness.
        """

        if not opponent_profile:

            return 0



        opponent_type = opponent_profile.get(

            "type",

            "unknown"

        )



        if opponent_type == "tight_passive":

            return 3



        if opponent_type == "calling_station":

            return -3



        if opponent_type == "loose_aggressive":

            return -1



        if opponent_type == "tight_aggressive":

            return 1



        return 0




    # ==========================================
    # Range Factor
    # ==========================================

    def range_factor(
        self,
        range_profile
    ):
        """
        Weak opponent range means
        better bluff opportunity.
        """

        if not range_profile:

            return 0



        strength = range_profile.get(

            "range_strength",

            50

        )



        if strength >= 75:

            return -3



        if strength >= 55:

            return -1



        if strength <= 35:

            return 3



        return 0




    # ==========================================
    # Equity Factor
    # ==========================================

    def equity_factor(
        self,
        equity
    ):
        """
        Decide whether hand is suitable
        as bluff candidate.
        """

        if equity < 25:

            return 2



        if equity > 60:

            return -3



        return 0
        # ==========================================
    # Stack Pressure Factor
    # ==========================================

    def stack_factor(
        self,
        context=None
    ):
        """
        Deep stacks allow more bluff pressure.

        Short stacks reduce bluff frequency.
        """

        if context is None:

            return 0



        stack = getattr(

            context,

            "player_stack",

            0

        )



        pot = getattr(

            context,

            "pot_size",

            0

        )



        if pot <= 0:

            return 0



        spr = stack / pot



        if spr >= 8:

            return 2



        if spr <= 2:

            return -2



        return 0





    # ==========================================
    # Opponent Confidence Factor
    # ==========================================

    def confidence_factor(
        self,
        opponent_profile
    ):
        """
        Reduce aggressive assumptions
        when opponent data is uncertain.
        """

        if not opponent_profile:

            return 0



        confidence = opponent_profile.get(

            "confidence",

            0

        )



        if confidence >= 0.7:

            return 1



        if confidence <= 0.2:

            return -1



        return 0





    # ==========================================
    # Bluff Type
    # ==========================================

    def bluff_type(
        self,
        equity,
        board_analysis
    ):
        """
        Classify bluff opportunity.
        """



        if equity >= 35:

            return "semi_bluff"



        if board_analysis:

            if board_analysis.get(

                "texture",

                ""

            ) == "dry":

                return "pure_bluff"



        return "pressure_bluff"





    # ==========================================
    # Final Evaluation
    # ==========================================

    def evaluate(
        self,
        position,
        board_analysis,
        opponent_profile,
        equity,
        range_profile=None,
        context=None
    ):
        """
        Complete bluff evaluation.

        Returns:

        {
            should_bluff,
            frequency,
            score,
            confidence,
            bluff_type,
            reasons
        }
        """



        score = 0


        reasons = []




        # Position

        value = self.position_factor(

            position

        )


        score += value



        if value > 0:

            reasons.append(

                "good_position"

            )




        # Board

        value = self.board_factor(

            board_analysis

        )


        score += value



        if value > 0:

            reasons.append(

                "favorable_board"

            )




        # Opponent

        value = self.opponent_factor(

            opponent_profile

        )


        score += value



        if value > 0:

            reasons.append(

                "weak_opponent"

            )




        # Range

        value = self.range_factor(

            range_profile

        )


        score += value



        if value > 0:

            reasons.append(

                "weak_range"

            )




        # Equity

        value = self.equity_factor(

            equity

        )


        score += value




        # Stack

        value = self.stack_factor(

            context

        )


        score += value




        # Confidence

        value = self.confidence_factor(

            opponent_profile

        )


        score += value





        # ======================================
        # Strategy Adjustment
        # ======================================

        bluff_frequency = self.get_strategy_value(

            "bluff_frequency",

            0.2

        )




        # ======================================
        # Difficulty Adjustment
        # ======================================

        multiplier = self.get_difficulty_value(

            "bluff_multiplier",

            1.0

        )



        frequency = (

            bluff_frequency

            *

            multiplier

        )



        frequency += score * 0.05




        frequency = max(

            0,

            min(

                frequency,

                1

            )

        )





        should_bluff = (

            frequency >= 0.25

        )





        confidence = abs(

            score

        ) / 12



        confidence = min(

            confidence,

            1.0

        )





        return {


            "should_bluff":

                should_bluff,


            "frequency":

                round(

                    frequency,

                    2

                ),


            "score":

                score,


            "confidence":

                round(

                    confidence,

                    2

                ),


            "bluff_type":

                self.bluff_type(

                    equity,

                    board_analysis

                ),


            "reasons":

                reasons

        }





    # ==========================================
    # Explain
    # ==========================================

    def explain(
        self,
        result
    ):
        """
        Human-readable explanation.
        """

        return {


            "bluff":

                result.get(

                    "should_bluff",

                    False

                ),



            "type":

                result.get(

                    "bluff_type",

                    "unknown"

                ),



            "frequency":

                result.get(

                    "frequency",

                    0

                ),



            "confidence":

                result.get(

                    "confidence",

                    0

                ),



            "reasons":

                result.get(

                    "reasons",

                    []

                )

        }





    # ==========================================
    # Debug
    # ==========================================

    def __repr__(self):

        return (

            "BluffEngine()"

        )



    def __str__(self):

        return (

            "Poker Bluff Evaluation Engine"

        )