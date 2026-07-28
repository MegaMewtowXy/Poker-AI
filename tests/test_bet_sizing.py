from AI.bet_sizing import BetSizer

from models.action import Action



class MockContext:

    def __init__(
        self,
        pot_size,
        stack,
        current_bet=50,
        street="flop"
    ):

        self.pot_size = pot_size

        self.player_stack = stack

        self.current_bet = current_bet

        self.street = street





def test_bet_sizing():


    print("\n========== BET SIZING TEST ==========")



    sizer = BetSizer()




    # ==========================================
    # Weak Bet
    # ==========================================

    context = MockContext(

        pot_size=200,

        stack=1000

    )



    weak = sizer.bet_size(

        context,

        40

    )


    print(

        "\nWeak bet:",

        weak

    )



    assert weak["amount"] > 0

    assert weak["reason"] == "small_value_bet"




    # ==========================================
    # Strong Bet
    # ==========================================

    strong = sizer.bet_size(

        context,

        90

    )


    print(

        "\nStrong bet:",

        strong

    )



    assert strong["amount"] > weak["amount"]

    assert strong["reason"] == "strong_value_bet"




    # ==========================================
    # Raise
    # ==========================================

    raise_context = MockContext(

        pot_size=300,

        stack=1000,

        current_bet=50

    )



    raise_amount = sizer.raise_size(

        raise_context,

        80

    )



    print(

        "\nRaise:",

        raise_amount

    )



    assert raise_amount["amount"] >= 100

    assert raise_amount["reason"] == "strong_value_raise"




    # ==========================================
    # All In
    # ==========================================

    all_in = sizer.all_in_amount(

        context

    )



    print(

        "\nAll In:",

        all_in

    )



    assert all_in["amount"] == 1000




    print(

        "\n========== BET SIZING TEST PASSED =========="

    )





if __name__ == "__main__":

    test_bet_sizing()