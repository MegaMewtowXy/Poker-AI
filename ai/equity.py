from models.card import Card

from engine.evaluator import HandEvaluator
from models.deck import Deck



class EquityCalculator:
    """
    Monte Carlo poker equity calculator.

    Calculates:

    - Win percentage
    - Tie percentage
    - Lose percentage
    - Equity

    Simulation safe:
    ----------------
    Does not modify:
    - Player objects
    - Deck objects
    - Game state
    """



    def __init__(self):

        self.evaluator = HandEvaluator()



    # ==================================================
    # Main Calculation
    # ==================================================

    def calculate(
        self,
        hero_cards: list[Card],
        community_cards: list[Card],
        opponent_count: int = 1,
        simulations: int = 5000,
        deck: Deck = None
    ) -> dict:
        """
        Calculate hero equity.

        opponent_count:
            Number of unknown opponents.

        simulations:
            Number of Monte Carlo trials.
        """

        if opponent_count <= 0:

            raise ValueError(
                "Opponent count must be positive."
            )


        if simulations <= 0:

            raise ValueError(
                "Simulation count must be positive."
            )


        wins = 0

        ties = 0

        losses = 0



        for _ in range(simulations):


            result = self.simulate(

                hero_cards,

                community_cards,

                opponent_count,

                deck

            )


            if result == "win":

                wins += 1


            elif result == "tie":

                ties += 1


            else:

                losses += 1



        total = (

            wins

            +

            ties

            +

            losses

        )


        return {

            "win_percentage":

                round(

                    wins / total * 100,

                    2

                ),


            "tie_percentage":

                round(

                    ties / total * 100,

                    2

                ),


            "lose_percentage":

                round(

                    losses / total * 100,

                    2

                ),


            "equity":

                round(

                    (

                        wins

                        +

                        (

                            ties * 0.5

                        )

                    )

                    /

                    total

                    *

                    100,

                    2

                )

        }



    # ==================================================
    # Simulation
    # ==================================================

    def simulate(
        self,
        hero_cards: list[Card],
        community_cards: list[Card],
        opponent_count: int,
        deck: Deck = None
    ) -> str:
        """
        Run one simulation.

        Uses temporary state only.
        """

        if deck is None:

            deck = Deck()



        simulation_deck = deck.clone()

        simulation_deck.shuffle()

        # ----------------------------------------------
        # Remove known cards
        # ----------------------------------------------

        known_cards = (

            hero_cards

            +

            community_cards

        )


        simulation_deck.remove_cards(

            known_cards

        )



        # ----------------------------------------------
        # Deal opponents
        # ----------------------------------------------

        opponents = []


        for _ in range(opponent_count):


            opponents.append(

                simulation_deck.deal_many(

                    2

                )

            )



        # ----------------------------------------------
        # Complete board
        # ----------------------------------------------

        board = community_cards.copy()



        missing = (

            5

            -

            len(board)

        )


        if missing > 0:

            board.extend(

                simulation_deck.deal_many(

                    missing

                )

            )



        # ----------------------------------------------
        # Evaluate hero
        # ----------------------------------------------

        hero_result = self.evaluator.evaluate(

            hero_cards,

            board

        )


        hero_score = hero_result.score



        tied = False



        # ----------------------------------------------
        # Compare all opponents
        # ----------------------------------------------

        for opponent in opponents:


            opponent_result = self.evaluator.evaluate(

                opponent,

                board

            )


            opponent_score = opponent_result.score



            # Lower score wins in Treys

            if opponent_score < hero_score:

                return "lose"



            if opponent_score == hero_score:

                tied = True



        if tied:

            return "tie"



        return "win"



    # ==================================================
    # Utility
    # ==================================================

    def __repr__(self):

        return "EquityCalculator()"



    # --------------------------------------------------

    def __str__(self):

        return (

            "Texas Hold'em "

            "Equity Calculator"

        )