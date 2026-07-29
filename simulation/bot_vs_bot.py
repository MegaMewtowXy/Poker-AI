from unittest import result

from integration.ai_player import AIPlayer

from AI.bot_player import BotPlayer
from AI.difficulty import Difficulty
from AI.strategy import Strategy

from engine.game import Game

from simulation.logger import GameLogger

import random
import uuid
import traceback




class BotVsBotSimulation:
    """
    AI vs AI poker simulation runner.


    Responsibilities
    ----------------

    Simulation owns:

    - Creating AI players
    - Running multiple hands
    - Tracking results
    - Generating statistics


    Engine owns:

    - Cards
    - Dealer
    - Betting
    - Pot
    - Showdown
    - Poker rules


    AI owns:

    - Decision making
    - Strategy
    - Analysis
    """





    def __init__(
        self,
        hands=100,
        starting_chips=1000,
        seed=None,
        players=None,
        enable_logging=True,
        auto_rebuy=True
    ):


        self.simulation_id = str(

            uuid.uuid4()

        )



        self.hands = hands



        self.starting_chips = starting_chips



        self.enable_logging = enable_logging

        self.auto_rebuy = auto_rebuy



        self.completed_hands = 0


        self.failed_hands = 0


        self.current_hand = 0


        self.errors = []





        if seed is not None:

            random.seed(seed)





        # ======================================
        # Create Players
        # ======================================

        if players is not None:


            self.players = players



        else:


            self.players = [



                AIPlayer(

                    "DeepBot",

                    BotPlayer(

                        "DeepBot",

                        Difficulty.HARD,

                        Strategy.TIGHT_AGGRESSIVE

                    ),

                    starting_chips

                ),





                AIPlayer(

                    "AggroBot",

                    BotPlayer(

                        "AggroBot",

                        Difficulty.MEDIUM,

                        Strategy.LOOSE_AGGRESSIVE

                    ),

                    starting_chips

                )

            ]





        self.validate_players()





        # ======================================
        # Logger
        # ======================================

        self.logger = None



        if self.enable_logging:


            self.logger = GameLogger(

                "data/hand_history"

            )





        self.initialize_statistics()
        # ==========================================
    # Validation
    # ==========================================

    def validate_players(
        self
    ):
        """
        Validate simulation players.
        """



        if len(self.players) < 2:

            raise ValueError(

                "At least 2 players are required."

            )





        for player in self.players:


            if not isinstance(

                player,

                AIPlayer

            ):

                raise ValueError(

                    "BotVsBotSimulation requires AI players only."

                )







    # ==========================================
    # Initialize Statistics
    # ==========================================

    def initialize_statistics(
        self
    ):
        """
        Create statistics containers.
        """



        self.results = {}





        for player in self.players:


            self.results[player.name] = {



                "hands": 0,


                "wins": 0,


                "losses": 0,


                "ties": 0,


                "chips": self.starting_chips,


                "win_rate": 0.0,


                "busts": 0,


                "busted": False


            }







    # ==========================================
    # Run Single Hand
    # ==========================================

    def run_hand(
        self
    ):
        """
        Execute one complete AI hand.
        """



        winner = None





        try:



            game = Game(

                self.players,

                logger=self.logger

            )





            result = game.play_hand()

            


            if isinstance(

                result,

                dict

            ):


                winner = result.get(

                    "winner"

                )



            else:


                winner = result
            





        except Exception as error:



            self.failed_hands += 1





            self.errors.append(



                {


                    "hand":

                        self.current_hand + 1,



                    "error":

                        str(error)



                }



            )





            print(f"\nSimulation error on hand {self.current_hand + 1}")
            traceback.print_exc()

            raise







        finally:


            self.current_hand += 1







        if winner is None:


            return None







        self.completed_hands += 1







        # ======================================
        # Update Results
        # ======================================


        for player in self.players:



            self.results[player.name]["hands"] += 1







        self.results[winner.name]["wins"] += 1







        for player in self.players:



            if player != winner:


                self.results[player.name]["losses"] += 1







        # ======================================
        # Chip Tracking
        # ======================================


        for player in self.players:



            self.results[player.name]["chips"] = (

                player.chips

            )





            if player.chips <= 0:
                if not self.results[player.name]["busted"]:
                    self.results[player.name]["busted"] = True
                self.results[player.name]["busts"] += 1
                if self.auto_rebuy:
                    player.chips = self.starting_chips
                    self.results[player.name]["chips"] = player.chips

        return winner

    # ==========================================
    # Run Simulation
    # ==========================================

    def run(
        self
    ):
        """
        Execute complete AI simulation.
        """

        for hand in range(
            self.hands
        ):
            if self.auto_rebuy:
                for player in self.players:
                    if player.chips <= 0:
                        player.chips = self.starting_chips
            else:
                # Stop if tournament is over
                active_players = [
                    player
                    for player in self.players
                    if player.chips > 0
                ]

                if len(active_players) < 2:
                    break






            self.run_hand()





            if (

                self.hands >= 100

                and

                (hand + 1) %

                max(

                    1,

                    self.hands // 10

                )

                == 0

            ):


                print(

                    f"Progress: {hand + 1}/{self.hands}"

                )







        self.calculate_statistics()





        if self.logger:


            self.logger.save_all_history()





        return self.summary()







    def run_parallel(
        self,
        num_workers=None
    ):
        """
        Execute simulation across multiple threads/cores in parallel.
        """
        from simulation.parallel_runner import ParallelSimulationRunner
        runner = ParallelSimulationRunner(
            hands=self.hands,
            starting_chips=self.starting_chips,
            enable_logging=self.enable_logging,
            num_workers=num_workers
        )
        return runner.run()

    # ==========================================
    # Calculate Statistics
    # ==========================================


    def calculate_statistics(
        self
    ):
        """
        Calculate simulation statistics.
        """



        for player in self.players:


            data = self.results[player.name]





            if data["hands"] > 0:


                data["win_rate"] = round(

                    data["wins"]

                    /

                    data["hands"],

                    3

                )



            else:


                data["win_rate"] = 0.0







    # ==========================================
    # Summary
    # ==========================================

    def summary(
        self
    ):
        """
        Return simulation result.
        """



        return {



            "simulation_id":

                self.simulation_id,



            "hands_requested":

                self.hands,



            "hands_completed":

                self.completed_hands,



            "hands_failed":

                self.failed_hands,



            "players":

                [

                    player.name

                    for player in self.players

                ],



            "results":

                self.results,



            "errors":

                self.errors

        }
    
    # ==========================================
    # Bot Profiles
    # ==========================================

    def bot_profiles(
        self
    ):
        """
        Return AI bot information.
        """



        return [

            player.profile()

            for player in self.players

        ]







    # ==========================================
    # Simulation Profile
    # ==========================================

    def profile(
        self
    ):
        """
        Return simulation configuration.
        """



        return {



            "simulation_id":

                self.simulation_id,



            "hands":

                self.hands,



            "starting_chips":

                self.starting_chips,



            "players":

                [

                    player.name

                    for player in self.players

                ],



            "logging_enabled":

                self.enable_logging,



            "bots":

                self.bot_profiles()

        }







    # ==========================================
    # Reset Simulation
    # ==========================================

    def reset(
        self
    ):
        """
        Reset simulation state.
        """



        self.current_hand = 0


        self.completed_hands = 0


        self.failed_hands = 0



        self.errors.clear()





        for player in self.players:



            player.chips = self.starting_chips



            player.reset_for_round()





        self.initialize_statistics()





        if self.logger:


            self.logger.clear()
    
    # ==========================================
    # Debug String
    # ==========================================

    def __str__(
        self
    ):
        """
        Human readable simulation status.
        """



        return (

            "========== BOT VS BOT SIMULATION ==========\n"

            f"Simulation ID: {self.simulation_id}\n"

            f"Hands Requested: {self.hands}\n"

            f"Hands Completed: {self.completed_hands}\n"

            f"Hands Failed: {self.failed_hands}\n"

            "Players: "

            +

            ", ".join(

                [

                    player.name

                    for player in self.players

                ]

            )

        )







    # ==========================================
    # Debug Representation
    # ==========================================

    def __repr__(
        self
    ):

        return (

            f"BotVsBotSimulation("

            f"hands={self.hands}, "

            f"players={len(self.players)})"

        )