class PotOddsCalculator:
    """
    Calculates poker pot odds.

    Responsibilities
    ----------------
    • Calculate required equity
    • Compare equity vs pot odds
    • Calculate expected value

    Does NOT:
    • Make betting decisions
    • Control gameplay
    """



    # ==================================================
    # Pot Odds
    # ==================================================

    def calculate(
        self,
        pot_size: int,
        call_amount: int
    ) -> float:
        """
        Returns required equity percentage
        to make a profitable call.

        Example:

        Pot = $200
        Call = $50

        Required equity = 20%
        """

        if pot_size < 0:

            raise ValueError(
                "Pot size cannot be negative."
            )


        if call_amount <= 0:

            return 0.0



        total_pot = (

            pot_size

            +

            call_amount

        )


        return round(

            (

                call_amount

                /

                total_pot

            ) * 100,

            2

        )



    # ==================================================
    # Decimal Format
    # ==================================================

    def calculate_ratio(
        self,
        pot_size: int,
        call_amount: int
    ) -> float:
        """
        Returns required equity as decimal.

        Example:

        25% -> 0.25
        """

        return self.calculate(

            pot_size,

            call_amount

        ) / 100



    # ==================================================
    # Call Evaluation
    # ==================================================

    def is_profitable_call(
        self,
        equity: float,
        pot_odds: float
    ) -> bool:
        """
        Compare winning chance against
        required equity.

        Both values should be decimals.

        Example:

        equity = 0.45
        pot_odds = 0.25

        Result:
        True
        """

        return equity >= pot_odds



    # ==================================================
    # Expected Value
    # ==================================================

    def expected_value(
        self,
        equity: float,
        pot_size: int,
        call_amount: int
    ) -> float:
        """
        Calculate call EV.

        Formula:

        EV =
        (equity × final pot)
        - call amount

        Positive EV:
            profitable

        Negative EV:
            losing
        """

        if call_amount <= 0:

            return 0.0



        final_pot = (

            pot_size

            +

            call_amount

        )


        return (

            equity

            *

            final_pot

        ) - call_amount



    # ==================================================
    # Debug
    # ==================================================

    def __repr__(self):

        return "PotOddsCalculator()"



    def __str__(self):

        return (

            "Poker Pot Odds Calculator"

        )