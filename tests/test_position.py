from AI.position import (
    PositionAnalyzer
)
from models.player_position import PlayerPosition

def test_position():

    print("\n========== POSITION TEST ==========")

    analyzer = PositionAnalyzer()

    early = analyzer.analyze(

        PlayerPosition.UNDER_THE_GUN

    )

    button = analyzer.analyze(

        PlayerPosition.BUTTON

    )

    print("\nUTG")

    print(early)

    print("\nBUTTON")

    print(button)

    assert early["advantage"] < button["advantage"]

    assert button["aggression_modifier"] > early["aggression_modifier"]

    assert button["range_modifier"] > early["range_modifier"]

    print(
        "\n========== POSITION TEST PASSED =========="
    )

if __name__ == "__main__":

    test_position()
