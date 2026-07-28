from matplotlib.style import context

from models.action import Action



class BetSizer:
    """
    Final poker bet sizing engine.

    Responsibilities
    ----------------
    • Calculate bet amounts
    • Calculate raise sizes
    • Calculate 3-bet sizes
    • Adjust sizing using:
        - Strength
        - Equity
        - Strategy
        - Difficulty
        - Street
        - Stack size
        - Pot size
        - Opponent profile

    Does NOT
    --------
    • Decide action
    • Execute betting
    • Manage chips
    """



    def __init__(
        self,
        strategy=None,
        difficulty=None
    ):

        self.strategy = strategy

        self.difficulty = difficulty




    # ==========================================
    # Safe Parameter Access
    # ==========================================

    def get_strategy_value(
        self,
        method,
        default=1.0
    ):
        """
        Safely get strategy values.
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




    # ------------------------------------------


    def get_difficulty_value(
        self,
        method,
        default=1.0
    ):
        """
        Safely get difficulty values.
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
    # Stack / Pot Information
    # ==========================================

    def stack_to_pot_ratio(
        self,
        context
    ):
        """
        Calculate SPR.

        Lower SPR:
        More aggressive sizing.

        Higher SPR:
        Smaller sizing.
        """

        if context.pot_size <= 0:

            return 0



        return round(

            context.player_stack

            /

            context.pot_size,

            2

        )




    # ==========================================
    # Normal Bet
    # ==========================================

    def bet_size(
        self,
        context,
        strength,
        equity=None
    ):
        """
        Calculate opening/value bet size.
        """


        if equity is None:

            equity = strength



        pot = context.pot_size




        # ======================================
        # Base Percentage
        # ======================================

        if equity >= 75:


            percentage = 1.0

            reason = "strong_value_bet"



        elif equity >= 55:


            percentage = 0.75

            reason = "medium_value_bet"



        elif equity >= 35:


            percentage = 0.50

            reason = "small_value_bet"



        else:


            percentage = 0.40

            reason = "bluff_bet"




        # ======================================
        # Strategy Adjustment
        # ======================================

        aggression = self.get_strategy_value(

            "aggression",

            0.5

        )



        percentage *= (

            0.75

            +

            aggression

        )




        # ======================================
        # Difficulty Adjustment
        # ======================================

        difficulty_modifier = self.get_difficulty_value(

            "aggression_modifier",

            1.0

        )



        percentage *= difficulty_modifier




        # ======================================
        # Street Adjustment
        # ======================================

        if hasattr(

            context,

            "street"

        ):

            percentage *= self.street_modifier(

                context.street

            )




        amount = int(

            pot

            *

            percentage

        )



        if amount > context.player_stack:
            amount = context.player_stack




        return {


            "amount":

                amount,


            "reason":

                reason,


            "percentage":

                round(

                    percentage,

                    2

                )

        }
        # ==========================================
    # Raise Size
    # ==========================================

    def raise_size(
    self,
    context,
    strength,
    equity=None
):
            """
            Calculate a legal raise-to amount.

            Returns the TOTAL amount the player's
            bet should become after raising.
            """

            if equity is None:
                equity = strength

            # ======================================
            # Base Raise Multiplier
            # ======================================

            if equity >= 75:

                multiplier = 3.5
                reason = "strong_value_raise"

            elif equity >= 55:

                multiplier = 2.5
                reason = "standard_raise"

            elif equity >= 35:

                multiplier = 2.0
                reason = "pressure_raise"

            else:

                multiplier = 1.5
                reason = "bluff_raise"

            # ======================================
            # Strategy
            # ======================================

            aggression = self.get_strategy_value(
                "aggression",
                0.5
            )

            multiplier *= (
                0.75
                +
                aggression
            )

            # ======================================
            # Difficulty
            # ======================================

            multiplier *= self.get_difficulty_value(
                "aggression_modifier",
                1.0
            )

            # ======================================
            # Calculate Raise Increment
            # ======================================

            raise_increment = max(
                context.min_raise,
                int(context.call_amount * multiplier)
            )

            # Smallest legal raise-to amount
            minimum_raise_to = (
                context.current_bet
                +
                context.min_raise
            )

            amount = (
                context.current_bet
                +
                raise_increment
            )

            if amount < minimum_raise_to:
                amount = minimum_raise_to

            # Chips already committed this street
            player_bet = context.player_current_bet

            # Maximum legal raise-to
            max_raise_to = (
                player_bet
                +
                context.player_stack
            )

            if amount > max_raise_to:
                amount = max_raise_to
            # Prevent illegal raise
            if max_raise_to <= context.current_bet:
                return {

                    "amount": max_raise_to,

                    "reason": "all_in",

                    "multiplier": round(multiplier, 2)

                }
            return {

                "amount": amount,

                "reason": reason,

                "multiplier": round(
                    multiplier,
                    2
                )

            }

    # ==========================================
    # 3 Bet Size
    # ==========================================

    def three_bet_size(
        self,
        context,
        equity
    ):
        """
        Calculate 3-bet sizing.

        Stronger than normal raises.
        """



        if equity >= 75:


            multiplier = 4.0

            reason = "premium_3bet"



        elif equity >= 55:


            multiplier = 3.0

            reason = "standard_3bet"



        else:


            multiplier = 2.5

            reason = "light_3bet"





        multiplier *= self.get_strategy_value(

            "aggression",

            0.5

        )




        amount = int(

            context.current_bet

            *

            multiplier

        )




        amount = self.clamp(

            amount,

            context.player_stack

        )




        return {


            "amount":

                amount,


            "reason":

                reason,


            "multiplier":

                round(

                    multiplier,

                    2

                )

        }





    # ==========================================
    # All In
    # ==========================================

    def all_in_amount(
        self,
        context
    ):
        """
        Return complete stack commitment.
        """



        return {


            "amount":

                context.player_stack,


            "reason":

                "all_in"

        }





    # ==========================================
    # Street Adjustment
    # ==========================================

    def street_modifier(
        self,
        street
    ):
        """
        Adjust bet sizing by poker street.

        Preflop:
        Standard sizing

        Flop:
        Smaller continuation bets

        Turn:
        Larger pressure bets

        River:
        Maximum value extraction
        """



        modifiers = {


            "preflop":

                1.0,


            "flop":

                0.65,


            "turn":

                0.85,


            "river":

                1.0

        }




        return modifiers.get(

            str(street).lower(),

            1.0

        )





    # ==========================================
    # Opponent Adjustment
    # ==========================================

    def opponent_modifier(
        self,
        opponent=None
    ):
        """
        Adjust sizing based on opponent.

        Loose opponents:
        Bigger value bets

        Tight opponents:
        Smaller bluff sizing
        """



        if opponent is None:

            return 1.0




        threat = opponent.get(

            "threat_level",

            5

        )



        opponent_type = opponent.get(

            "type",

            ""

        )




        # Calling stations

        if opponent_type == "calling_station":

            return 1.25




        # Aggressive opponents

        if opponent_type == "loose_aggressive":

            return 1.15




        # Tight dangerous players

        if threat >= 8:

            return 0.85




        return 1.0





    # ==========================================
    # Pot Pressure Modifier
    # ==========================================

    def pot_pressure_modifier(
        self,
        context
    ):
        """
        Adjust sizing according to stack pressure.

        Short stack:
        Commit more

        Deep stack:
        Avoid unnecessary inflation
        """



        spr = self.stack_to_pot_ratio(

            context

        )



        if spr <= 2:

            return 1.2




        elif spr >= 8:

            return 0.85




        return 1.0
        # ==========================================
    # Unified Bet Calculation
    # ==========================================

    def calculate_size(
    self,
    action,
    context,
    strength,
    equity=None,
    opponent=None
):
            """
            Final bet sizing interface.
            """

            if action == Action.BET:

                result = self.bet_size(
                    context,
                    strength,
                    equity
                )

            elif action == Action.RAISE:

                result = self.raise_size(
                    context,
                    strength,
                    equity
                )
                if result["reason"] == "all_in":

                    return self.all_in_amount(context)

            elif action == Action.ALL_IN:

                result = self.all_in_amount(
                    context
                )

            else:

                return {

                    "amount": 0,

                    "reason": "no_bet_action"

                }

            # ======================================
            # BETS ONLY
            #
            # Never modify a legal raise amount.
            # ======================================

            if action != Action.RAISE:

                if opponent:

                    modifier = self.opponent_modifier(
                        opponent
                    )

                    result["amount"] = int(
                        result["amount"]
                        *
                        modifier
                    )

                pressure = self.pot_pressure_modifier(
                    context
                )

                result["amount"] = int(
                    result["amount"]
                    *
                    pressure
                )

                result["amount"] = self.clamp(
                    result["amount"],
                    context.player_stack
                )

            return result



    # ==========================================
    # Validate Bet
    # ==========================================

    def validate_bet(
        self,
        amount,
        stack
    ):
        """
        Ensure bet amount is legal.
        """



        if amount < 0:

            return 0



        if amount > stack:

            return stack



        return int(amount)





    # ==========================================
    # Profile
    # ==========================================

    def profile(
        self
    ):
        """
        Return sizing engine information.
        """



        return {


            "strategy":

                str(self.strategy),


            "difficulty":

                str(self.difficulty),


            "engine":

                "advanced_bet_sizing"

        }





    # ==========================================
    # Safety
    # ==========================================

    def clamp(
        self,
        amount,
        stack
    ):
        """
        Prevent illegal chip amounts.
        """



        if amount < 0:

            return 0



        if amount > stack:

            return int(stack)



        return int(amount)





    # ==========================================
    # Debug
    # ==========================================

    def __repr__(self):

        return (

            "BetSizer()"

        )



    def __str__(self):

        return (

            "Advanced Poker Bet Sizing Engine"

        )