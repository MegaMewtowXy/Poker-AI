class RiskManager:
    """
    Controls AI risk behaviour.

    Responsibilities
    ----------------
    • Analyze stack pressure
    • Calculate risk level
    • Adjust aggression behaviour
    • Handle survival situations

    Considers
    ----------
    • Stack size
    • Big blind depth
    • Strategy personality
    • Game pressure

    Does NOT
    --------
    • Decide actions
    • Control betting
    • Evaluate hands
    """

    def __init__(
        self,
        strategy=None
    ):

        self.strategy = strategy

    # ==========================================
    # Strategy Access
    # ==========================================

    def get_strategy_name(
        self,
        strategy=None
    ):
        """
        Safely get strategy name.
        """

        if strategy:

            return str(

                strategy

            ).lower()

        if self.strategy:

            return str(

                self.strategy

            ).lower()

        return "balanced"

    # ==========================================
    # Stack Conversion
    # ==========================================

    def stack_in_bb(
        self,
        player_stack,
        big_blind
    ):
        """
        Convert chips into big blinds.
        """

        if big_blind <= 0:

            return 0

        return player_stack / big_blind

    # ==========================================
    # Main Analysis
    # ==========================================

    def analyze(
        self,
        player_stack,
        big_blind,
        strategy="balanced"
    ):
        """
        Returns risk profile.
        """

        stack_bb = self.stack_in_bb(

            player_stack,

            big_blind

        )

        # ======================================
        # Stack Pressure
        # ======================================

        if stack_bb <= 10:

            risk_level = 0.9

            aggression = 1.3

            style = "desperate"

        elif stack_bb <= 30:

            risk_level = 0.7

            aggression = 1.15

            style = "semi_aggressive"

        elif stack_bb <= 100:

            risk_level = 0.5

            aggression = 1.0

            style = "balanced"

        else:

            risk_level = 0.3

            aggression = 0.85

            style = "patient"

        # ======================================
        # Strategy Adjustment
        # ======================================

        strategy_name = self.get_strategy_name(

            strategy

        )

        if "loose_aggressive" in strategy_name:

            aggression += 0.15

        elif "tight_passive" in strategy_name:

            aggression -= 0.15

        elif "tight_aggressive" in strategy_name:

            aggression += 0.05

        aggression = max(

            0.5,

            min(

                aggression,

                1.5

            )

        )
        return {

            "stack_bb":

                round(

                    stack_bb,

                    2

                ),

            "risk_level":

                risk_level,

            "aggression_modifier":

                round(

                    aggression,

                    2

                ),

            "recommended_style":

                style

        }

    # ==========================================
    # Stack Pressure Analysis
    # ==========================================

    def stack_pressure(
        self,
        player_stack,
        big_blind
    ):
        """
        Classify stack situation.
        """

        stack_bb = self.stack_in_bb(

            player_stack,

            big_blind

        )

        if stack_bb <= 10:

            return "critical"

        elif stack_bb <= 30:

            return "short"

        elif stack_bb <= 100:

            return "normal"

        else:

            return "deep"

    # ==========================================
    # Survival Mode
    # ==========================================

    def survival_mode(
        self,
        player_stack,
        big_blind
    ):
        """
        Determine if AI should prioritize
        survival.
        """

        stack_bb = self.stack_in_bb(

            player_stack,

            big_blind

        )

        return stack_bb <= 10

    # ==========================================
    # SPR Analysis
    # ==========================================

    def stack_pot_ratio(
        self,
        player_stack,
        pot_size
    ):
        """
        Calculate stack-to-pot ratio.
        """

        if pot_size <= 0:

            return 0

        return round(

            player_stack

            /

            pot_size,

            2

        )

    # ==========================================
    # Pressure Adjustment
    # ==========================================

    def pressure_factor(
        self,
        stack_pressure,
        opponents_remaining=1
    ):
        """
        Adjust risk based on pressure.
        """

        factor = 1.0

        if stack_pressure == "critical":

            factor += 0.25

        elif stack_pressure == "short":

            factor += 0.10

        if opponents_remaining > 5:

            factor -= 0.10

        return round(

            max(

                0.5,

                min(

                    factor,

                    1.5

                )

            ),

            2

        )

    # ==========================================
    # Full Profile
    # ==========================================

    def profile(
        self,
        player_stack,
        big_blind,
        strategy="balanced",
        opponents_remaining=1,
        pot_size=0
    ):
        """
        Complete risk profile.
        """

        risk = self.analyze(

            player_stack,

            big_blind,

            strategy

        )

        pressure = self.stack_pressure(

            player_stack,

            big_blind

        )

        return {

            **risk,

            "stack_pressure":

                pressure,

            "survival_mode":

                self.survival_mode(

                    player_stack,

                    big_blind

                ),

            "spr":

                self.stack_pot_ratio(

                    player_stack,

                    pot_size

                ),

            "pressure_factor":

                self.pressure_factor(

                    pressure,

                    opponents_remaining

                )

        }

    # ==========================================
    # Debug
    # ==========================================

    def __repr__(self):

        return (

            "RiskManager()"

        )

    def __str__(self):

        return (

            "Poker AI Risk Management Engine"

        )