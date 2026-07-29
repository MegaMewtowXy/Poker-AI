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



    def __init__(self, seed: int | None = None):

        self.evaluator = HandEvaluator()
        self.seed = seed
        self._simulation_index = 0



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

        if len(hero_cards) != 2:
            raise ValueError("Hero must have exactly two hole cards.")

        if len(community_cards) > 5:
            raise ValueError("Community cards cannot exceed five cards.")

        known_cards = hero_cards + community_cards
        if len(set(known_cards)) != len(known_cards):
            raise ValueError("Known cards cannot contain duplicates.")

        if opponent_count <= 0:

            raise ValueError(
                "Opponent count must be positive."
            )


        if simulations <= 0:

            raise ValueError(
                "Simulation count must be positive."
            )


        available_cards = 52 - len(known_cards)
        cards_needed = opponent_count * 2 + (5 - len(community_cards))
        if cards_needed > available_cards:
            raise ValueError("Not enough cards available for the requested simulation.")

        wins = 0

        ties = 0

        tie_equity = 0.0

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

                tie_equity += 1 / self._last_tied_players


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

                            tie_equity

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

        shuffle_seed = None
        if self.seed is not None:
            shuffle_seed = self.seed + self._simulation_index
            self._simulation_index += 1
        simulation_deck.shuffle(shuffle_seed)

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



        tied_players = 1



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

                self._last_tied_players = 0
                return "lose"



            if opponent_score == hero_score:

                tied_players += 1



        if tied_players > 1:

            self._last_tied_players = tied_players

            return "tie"


        self._last_tied_players = 1
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
