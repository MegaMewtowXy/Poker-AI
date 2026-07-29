from models.action import Action



class DecisionEngine:
    """
    Final AI poker decision engine.

    Responsibilities
    ----------------
    • Combine AI analysis
    • Calculate decision score
    • Select poker action
    • Generate confidence
    • Explain reasoning

    Uses
    ----
    • Hand strength
    • Equity
    • Pot odds
    • Position
    • Opponent information
    • Range information
    • Board information
    • Strategy
    • Difficulty

    Does NOT
    --------
    • Calculate equity
    • Calculate hand strength
    • Calculate bet size
    • Execute actions
    """



    def __init__(
        self,
        difficulty=None,
        strategy=None
    ):

        self.difficulty = difficulty

        self.strategy = strategy



        # ======================================
        # Action Thresholds
        # ======================================

        self.action_thresholds = {

            "fold":
              -20,

            "call":

                20,


            "bet":

                45,


            "raise":

                75

        }





    # ==========================================
    # Safe Parameter Access
    # ==========================================

    def get_strategy_value(
        self,
        method,
        default=0
    ):
        """
        Safely get strategy parameter.
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
        default=1
    ):
        """
        Safely get difficulty parameter.
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
    # Score Calculation
    # ==========================================

    def calculate_score(
        self,
        analysis
    ):
        """
        Convert complete poker analysis
        into aggression score.

        Higher score:
        More aggressive action.
        """



        score = 0

        factors = {}




        # ======================================
        # Hand Strength
        # ======================================

        strength = analysis.get(

            "strength",

            analysis.get(

                "final_strength",

                0

            )

        )



        if strength >= 85:

            value = 40



        elif strength >= 65:

            value = 30



        elif strength >= 45:

            value = 15



        else:

            value = -15




        score += value

        factors["strength"] = value




        # ======================================
        # Equity
        # ======================================

        equity = analysis.get(

            "equity",

            0

        )



        if equity >= 80:

            value = 40



        elif equity >= 65:

            value = 30



        elif equity >= 55:

            value = 15
        elif equity >= 45:
            value = 0


        else:

            value = -15




        score += value

        factors["equity"] = value
            # ======================================
        # Pot Odds
        # ======================================

        pot_odds = analysis.get(

            "pot_odds",

            100

        )



        if equity >= pot_odds:

            value = 5



        else:

            value = -15




        score += value

        factors["pot_odds"] = value




        # ======================================
        # Position
        # ======================================

        position = analysis.get(

            "position",

            {}

        )



        advantage = position.get(

            "advantage",

            0

        )



        value = advantage * 3



        score += value

        factors["position"] = value




        # ======================================
        # Opponent Threat
        # ======================================

        opponent = analysis.get("opponent") or {}




        threat = opponent.get(

            "threat_level",

            5

        )



        value = (

            5 - threat

        ) * 2



        score += value

        factors["opponent"] = value




        # ======================================
        # Range Strength
        # ======================================

        range_info = analysis.get("range") or {}

        



        range_strength = range_info.get(

            "range_strength",

            0

        )



        if range_strength >= 70:

            value = -10



        elif range_strength >= 50:

            value = -5



        else:

            value = 0




        score += value

        factors["range"] = value




        # ======================================
        # Board Analysis
        # ======================================

        board = analysis.get("board") or {}

           



        danger = board.get(

            "danger_level",

            0

        )



        if danger >= 6:

            value = -10



        elif danger >= 4:

            value = -5



        else:

            value = 0




        score += value

        factors["board"] = value

        # Risk profile is produced by BotPlayer and should influence how
        # readily a short stack commits chips.  The modifier is deliberately
        # bounded so it cannot override hand strength or equity.
        risk = analysis.get("risk") or {}
        risk_aggression = risk.get("aggression_modifier", 1.0)
        risk_enabled = risk.get("apply_to_decision", False)
        value = max(-10, min(10, (risk_aggression - 1.0) * 20)) if risk_enabled else 0
        score += value
        factors["risk"] = round(value, 2)




        return score, factors





    # ==========================================
    # Strategy Adjustment
    # ==========================================

    def apply_strategy(
        self,
        score,
        factors
    ):
        """
        Apply playing style influence.
        """



        aggression = self.get_strategy_value(

            "aggression",

            0.5

        )



        risk = self.get_strategy_value(

            "risk_tolerance",

            0.5

        )



        pressure = self.get_strategy_value(

            "pressure_factor",

            0.5

        )



        strategy_bonus = (

            aggression

            +

            risk

            +

            pressure

        ) / 3




        strategy_weight = self.get_difficulty_value(
            "strategy_weight",
            1.0
        )

        value = (

            strategy_bonus

            *

            10

            *

            strategy_weight

        )



        score += value



        factors["strategy"] = round(

            value,

            2

        )



        return score





    # ==========================================
    # Difficulty Adjustment
    # ==========================================

    def apply_difficulty(
        self,
        score,
        factors
    ):
        """
        Apply AI difficulty modifiers.
        """



        aggression = self.get_difficulty_value(

            "aggression_modifier",

            1.0

        )



        value = (

            aggression - 1

        ) * 20



        score += value



        factors["difficulty"] = round(

            value,

            2

        )



        return score





    # ==========================================
    # Bluff Adjustment
    # ==========================================

    def apply_bluff(
        self,
        score,
        analysis,
        factors
    ):
        """
        Modify score using bluff engine.
        """



        bluff = analysis.get("bluff") or {}

           



        should_bluff = bluff.get(

            "should_bluff",

            False

        )



        if not should_bluff:

            return score



        frequency = self.get_strategy_value(

            "bluff_frequency",

            0.1

        )



        multiplier = self.get_difficulty_value(

            "bluff_multiplier",

            1.0

        )



        value = (

            frequency

            *

            multiplier

            *

            10

        )



        score += value



        factors["bluff"] = round(

            value,

            2

        )



        return score
        # ==========================================
    # Mistake Simulation
    # ==========================================

    def apply_error(
        self,
        score
    ):
        """
        Simulates weaker AI mistakes.

        Higher difficulty:
        fewer mistakes.
        """



        mistake_rate = self.get_difficulty_value(

            "mistake_rate",

            0.1

        )



        # Higher mistake rate reduces score.
        # Hard AI should have close to zero penalty.

        penalty = (

            mistake_rate

            *

            10

        )



        return score - penalty





    # ==========================================
    # Score To Action
    # ==========================================

    def score_to_action(
    self,
    score,
    analysis
):
        """
        Convert score into a legal poker action.
        """

        call_amount = analysis.get(
            "call_amount",
            0
        )
        current_bet = analysis.get(
    "current_bet",
    0
)
        if score < self.action_thresholds["fold"]:

            return Action.FOLD

        elif score < self.action_thresholds["call"]:

            return Action.CALL if call_amount > 0 else Action.CHECK

        elif score < self.action_thresholds["bet"]:

              if current_bet > 0:
                    return Action.RAISE

              return Action.BET

        elif score < self.action_thresholds["raise"]:

            return Action.RAISE

        else:

            return Action.ALL_IN



    # ==========================================
    # Action Safety
    # ==========================================

    def validate_action(
        self,
        action,
        analysis
    ):
        """
        Prevent impossible decisions.
        """



        all_in_available = analysis.get(

            "all_in_available",

            True

        )



        if action == Action.ALL_IN and not all_in_available:

            return Action.RAISE



        return action





    # ==========================================
    # Confidence
    # ==========================================

    def confidence(
        self,
        score
    ):
        """
        Convert score into confidence.

        Range:
        0 - 1
        """



        confidence = abs(score) / 100



        return round(

            min(

                confidence,

                1.0

            ),

            2

        )





    # ==========================================
    # Reason Generator
    # ==========================================

    def generate_reason(
        self,
        action,
        factors
    ):
        """
        Explain AI decision.
        """



        positive = []

        negative = []



        for key, value in factors.items():


            if value > 0:

                positive.append(key)



            elif value < 0:

                negative.append(key)




        if action == Action.ALL_IN:

            return "maximum_strength_decision"




        if action == Action.RAISE:


            if positive:

                return (

                    "aggressive_play_based_on_"

                    +

                    "_".join(

                        positive

                    )

                )


            return "pressure_raise"




        if action == Action.BET:

            return "value_or_bluff_bet"




        if action == Action.CALL:


            if negative:

                return (

                    "defensive_call_with_"

                    +

                    "_".join(

                        negative

                    )

                )


            return "pot_odds_call"




        if action == Action.FOLD:

            return "weak_hand_or_bad_conditions"



        return "standard_decision"





    # ==========================================
    # Final Decision
    # ==========================================

    def decide(
        self,
        analysis
    ):
        """
        Generate complete AI decision.

        Returns:

        {
            action,
            score,
            confidence,
            reason,
            factors
        }
        """



        score, factors = self.calculate_score(

            analysis

        )



        score = self.apply_strategy(

            score,

            factors

        )



        score = self.apply_difficulty(

            score,

            factors

        )



        score = self.apply_bluff(

            score,

            analysis,

            factors

        )



        score = self.apply_error(

            score

        )
        
        action = self.score_to_action(

            score,
            analysis

        )



        action = self.validate_action(

            action,

            analysis

        )




        return {


            "action":

                action,


            "score":

                round(

                    score,

                    2

                ),


            "confidence":

                self.confidence(

                    score

                ),


            "reason":

                self.generate_reason(

                    action,

                    factors

                ),


            "factors":

                factors

        }





    # ==========================================
    # Explanation
    # ==========================================

    def explain(
        self,
        analysis
    ):
        """
        Human readable decision debug.
        """



        decision = self.decide(

            analysis

        )



        return {


            "action":

                decision["action"].value,


            "score":

                decision["score"],


            "confidence":

                decision["confidence"],


            "reason":

                decision["reason"],


            "factors":

                decision["factors"]

        }





    # ==========================================
    # Debug
    # ==========================================

    def __repr__(self):

        return "DecisionEngine()"



    def __str__(self):

        return "Poker AI Decision Engine"
