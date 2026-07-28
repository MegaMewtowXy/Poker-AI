from simulation.bot_vs_bot import BotVsBotSimulation





def test_bot_vs_bot():


    print(
        "\n========== BOT VS BOT TEST =========="
    )



    # ==========================================
    # Create Simulation
    # ==========================================

    simulation = BotVsBotSimulation(

        hands=10,

        starting_chips=1000,

        seed=42

    )



    starting_total_chips = (

        2

        *

        1000

    )



    print("\nSimulation Profile")



    profile = simulation.profile()



    print(profile)



    assert isinstance(

        profile,

        dict

    )



    assert profile["hands"] == 10



    assert profile["starting_chips"] == 1000



    assert len(

        profile["players"]

    ) == 2




    assert "bots" in profile





    # ==========================================
    # Run Simulation
    # ==========================================

    result = simulation.run()



    print("\nSimulation Result")

    print(result)



    assert isinstance(

        result,

        dict

    )



    assert result["hands_requested"] == 10



    assert "results" in result



    assert "errors" in result



    assert "hands_completed" in result



    assert "hands_failed" in result





    # Simulation may stop early if one bot busts

    assert (

        result["hands_completed"]

        +

        result["hands_failed"]

        <=

        10

    )







    results = result["results"]



    assert len(results) == 2





    # ==========================================
    # Validate Statistics
    # ==========================================


    total_player_hand_records = 0



    final_chip_count = 0



    for bot_name, stats in results.items():


        print(

            f"\n{bot_name}"

        )


        print(stats)



        assert "hands" in stats

        assert "wins" in stats

        assert "losses" in stats

        assert "ties" in stats

        assert "chips" in stats

        assert "win_rate" in stats

        assert "busts" in stats

        assert "busted" in stats



        assert stats["hands"] >= 0


        assert stats["wins"] >= 0


        assert stats["losses"] >= 0


        assert stats["busts"] >= 0



        assert 0 <= stats["win_rate"] <= 1



        total_player_hand_records += stats["hands"]



        final_chip_count += stats["chips"]







    # ==========================================
    # Chip Conservation
    # ==========================================


    assert (

        final_chip_count

        ==

        starting_total_chips

    )





    # ==========================================
    # Error Validation
    # ==========================================


    if result["hands_failed"] > 0:


        print(

            "\nSimulation Errors"

        )


        print(

            result["errors"]

        )




    assert len(

        result["errors"]

    ) == result["hands_failed"]







    # ==========================================
    # Summary Test
    # ==========================================


    summary = simulation.summary()



    print("\nSummary")

    print(summary)



    assert summary["hands_requested"] == 10



    assert "results" in summary



    assert "errors" in summary





    # ==========================================
    # Bot Profiles
    # ==========================================


    profiles = simulation.bot_profiles()



    print("\nBot Profiles")

    print(profiles)



    assert len(profiles) == 2



    for bot in profiles:


        assert "name" in bot


        assert "bot" in bot







    # ==========================================
    # Reset Test
    # ==========================================


    simulation.reset()



    reset_summary = simulation.summary()



    print("\nAfter Reset")

    print(reset_summary)



    for stats in reset_summary["results"].values():


        assert stats["hands"] == 0


        assert stats["wins"] == 0


        assert stats["losses"] == 0


        assert stats["chips"] == simulation.starting_chips


        assert stats["win_rate"] == 0.0


        assert stats["busts"] == 0


        assert stats["busted"] is False







    print(

        "\n========== BOT VS BOT TEST PASSED =========="

    )







if __name__ == "__main__":

    test_bot_vs_bot()