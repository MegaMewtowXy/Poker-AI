from AI.pot_odds import PotOddsCalculator

def test_pot_odds():

    print("\n========== POT ODDS TEST ==========")

    calculator = PotOddsCalculator()

    odds = calculator.calculate(

        500,

        100

    )

    print("Pot Odds:")

    print(odds)

    result = calculator.is_profitable_call(

        40,

        odds

    )

    print("Profitable Call:")

    print(result)

    assert odds == 16.67

    assert result == True

    print(
        "\n========== POT ODDS TEST PASSED =========="
    )

if __name__ == "__main__":

    test_pot_odds()