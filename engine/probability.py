from math import comb

from models.card import Card
from models.player import Player

from engine.evaluator import HandEvaluator


class Probability:
    """
    Poker probability and mathematical analysis.

    Responsibilities
    ----------------
    • Pot odds
    • Drawing odds
    • Equity estimation
    • Win probability
    • Monte Carlo simulation
    • Expected value

    This class never modifies game state.
    It performs mathematical calculations only.
    """

    def __init__(self):

        self.evaluator = HandEvaluator()

    # ==================================================
    # Pot Odds
    # ==================================================

    @staticmethod
    def pot_odds(
        call_amount: int,
        pot_size: int
    ) -> float:
        """
        Returns the pot odds.

        Formula:
            call / (pot + call)
        """

        if call_amount <= 0:

            return 0.0

        return call_amount / (
            pot_size + call_amount
        )

    # --------------------------------------------------

    @staticmethod
    def pot_odds_percentage(
        call_amount: int,
        pot_size: int
    ) -> float:
        """
        Pot odds expressed as a percentage.
        """

        return (

            Probability.pot_odds(

                call_amount,

                pot_size

            )

            * 100

        )

    # ==================================================
    # Implied Odds
    # ==================================================

    @staticmethod
    def implied_odds(
        call_amount: int,
        current_pot: int,
        expected_future_chips: int
    ) -> float:
        """
        Returns implied odds.
        """

        if call_amount <= 0:

            return 0.0

        return (

            current_pot

            + expected_future_chips

        ) / call_amount

    # ==================================================
    # Hand Strength
    # ==================================================

    def hand_strength(
        self,
        hole_cards: list[Card],
        community_cards: list[Card]
    ):
        """
        Evaluate the current hand.
        """

        return self.evaluator.evaluate(

            hole_cards,

            community_cards

        )
        # ==================================================
    # Outs
    # ==================================================

    @staticmethod
    def outs(
        unseen_cards: int,
        winning_cards: int
    ) -> int:
        """
        Return number of outs.

        Example:
        9 flush outs remaining.
        """

        if winning_cards < 0:

            return 0

        if winning_cards > unseen_cards:

            return unseen_cards

        return winning_cards

    # ==================================================
    # Drawing Probability
    # ==================================================

    @staticmethod
    def one_card_draw_probability(
        outs: int,
        unseen_cards: int
    ) -> float:
        """
        Probability of hitting an out
        on the next card.
        """

        if unseen_cards <= 0:

            return 0.0

        return outs / unseen_cards

    # --------------------------------------------------

    @staticmethod
    def one_card_draw_percentage(
        outs: int,
        unseen_cards: int
    ) -> float:

        return (

            Probability.one_card_draw_probability(

                outs,

                unseen_cards

            )

            * 100

        )

    # --------------------------------------------------

    @staticmethod
    def two_card_draw_probability(
        outs: int,
        unseen_cards: int
    ) -> float:
        """
        Probability of hitting at least one
        out by the river.

        Used when two cards remain.
        """

        if unseen_cards <= 0:

            return 0.0

        misses_first = (

            unseen_cards - outs

        ) / unseen_cards

        misses_second = (

            unseen_cards - outs - 1

        ) / (

            unseen_cards - 1

        )

        return 1 - (

            misses_first * misses_second

        )

    # ==================================================
    # Common Poker Draws
    # ==================================================

    @staticmethod
    def flush_draw_outs(
        known_cards: int,
        suit_cards: int
    ) -> int:
        """
        Calculate flush draw outs.

        Standard:
        13 cards in suit.
        """

        return max(

            0,

            13 - suit_cards

        )

    # --------------------------------------------------

    @staticmethod
    def straight_draw_outs(
        possible_cards: int
    ) -> int:
        """
        Placeholder for straight draw
        detection.

        Full straight detection will be
        handled after integrating with
        Evaluator patterns.
        """

        return max(

            0,

            possible_cards

        )
        # ==================================================
    # Equity
    # ==================================================

    def equity(
        self,
        player: Player,
        opponents: list[Player],
        community_cards: list[Card]
    ) -> float:
        """
        Estimate player's equity.

        Returns a value between:
        0.0 and 1.0

        Example:
        0.65 means approximately 65% equity.
        """

        if not opponents:

            return 1.0

        player_result = self.evaluator.evaluate(

            player.hand,

            community_cards

        )

        opponent_results = [

            self.evaluator.evaluate(

                opponent.hand,

                community_cards

            )

            for opponent in opponents

        ]

        wins = 0

        ties = 0

        total = len(opponent_results)

        for result in opponent_results:

            if player_result.score < result.score:

                wins += 1

            elif player_result.score == result.score:

                ties += 1

        return (

            wins + (ties * 0.5)

        ) / total

    # ==================================================
    # Win Probability
    # ==================================================

    def win_probability(
        self,
        player: Player,
        opponents: list[Player],
        community_cards: list[Card]
    ) -> float:
        """
        Return estimated chance of winning.
        """

        return self.equity(

            player,

            opponents,

            community_cards

        )

    # ==================================================
    # Hand Comparison
    # ==================================================

    def compare_players(
        self,
        players: list[Player],
        community_cards: list[Card]
    ) -> dict:
        """
        Compare all players.

        Returns a mapping:

        Player -> HandResult
        """

        results = {}

        for player in players:

            results[player] = (

                self.evaluator.evaluate(

                    player.hand,

                    community_cards

                )

            )

        return results

    # --------------------------------------------------

    def strongest_player(
        self,
        players: list[Player],
        community_cards: list[Card]
    ) -> Player | None:
        """
        Return the strongest hand among
        provided players.
        """

        if not players:

            return None

        results = self.compare_players(

            players,

            community_cards

        )

        winner = min(

            results,

            key=lambda player:

            results[player].score

        )

        return winner
        # ==================================================
    # Monte Carlo Simulation
    # ==================================================

    def monte_carlo(
        self,
        player: Player,
        opponents: list[Player],
        community_cards: list[Card],
        deck,
        simulations: int = 1000
    ) -> float:
        """
        Estimate win probability using
        Monte Carlo simulation.

        Returns:
            Probability between 0 and 1
        """

        if simulations <= 0:

            return 0.0

        wins = 0

        ties = 0

        for _ in range(simulations):

            simulation_deck = deck.copy()

            simulation_players = [

                opponent

                for opponent in opponents

            ]

            remaining_cards = (
                simulation_deck.remaining_cards()
            )

            # --------------------------------------
            # Assign random opponent cards
            # --------------------------------------

            for opponent in simulation_players:

                opponent_cards = [

                    remaining_cards.pop()

                    for _ in range(2)

                ]

                opponent.hand = opponent_cards


            # --------------------------------------
            # Complete community cards
            # --------------------------------------

            simulated_board = list(
                community_cards
            )

            while len(simulated_board) < 5:

                simulated_board.append(

                    remaining_cards.pop()

                )


            # --------------------------------------
            # Evaluate hands
            # --------------------------------------

            player_result = self.evaluator.evaluate(

                player.hand,

                simulated_board

            )

            opponent_results = [

                self.evaluator.evaluate(

                    opponent.hand,

                    simulated_board

                )

                for opponent in simulation_players

            ]


            best_opponent = min(

                opponent_results,

                key=lambda result:

                result.score

            )


            if player_result.score < best_opponent.score:

                wins += 1


            elif player_result.score == best_opponent.score:

                ties += 1


        return (

            wins + (ties * 0.5)

        ) / simulations

    # ==================================================
    # Simulation Helpers
    # ==================================================

    @staticmethod
    def required_board_cards(
        community_cards: list[Card]
    ) -> int:
        """
        Number of community cards still
        required to complete the board.
        """

        return max(

            0,

            5 - len(community_cards)

        )

    # --------------------------------------------------

    @staticmethod
    def remaining_cards(
        known_cards: int
    ) -> int:
        """
        Number of unknown cards remaining
        in a standard deck.
        """

        return max(

            0,

            52 - known_cards

        )
        # ==================================================
    # Expected Value
    # ==================================================

    @staticmethod
    def expected_value(
        win_probability: float,
        win_amount: int,
        lose_amount: int
    ) -> float:
        """
        Calculate expected value.

        Formula:

        EV =
        (Win Probability × Win Amount)
        -
        (Lose Probability × Lose Amount)
        """

        lose_probability = (

            1 - win_probability

        )

        return (

            win_probability * win_amount

        ) - (

            lose_probability * lose_amount

        )

    # --------------------------------------------------

    @staticmethod
    def call_ev(
        equity: float,
        pot_size: int,
        call_amount: int
    ) -> float:
        """
        Calculate EV of calling a bet.
        """

        if call_amount <= 0:

            return pot_size

        return (

            equity *

            (pot_size + call_amount)

        ) - call_amount

    # ==================================================
    # Utility Helpers
    # ==================================================

    @staticmethod
    def normalize_probability(
        value: float
    ) -> float:
        """
        Keep probability between
        0 and 1.
        """

        return max(

            0.0,

            min(

                1.0,

                value

            )

        )

    # --------------------------------------------------

    @staticmethod
    def percentage(
        probability: float
    ) -> float:
        """
        Convert probability to percentage.
        """

        return (

            Probability.normalize_probability(

                probability

            )

            * 100

        )

    # ==================================================
    # Debug
    # ==================================================

    def __repr__(self):

        return (

            "Probability("

            "HandEvaluator)"

        )

    # --------------------------------------------------

    def __str__(self):

        return (

            "========== PROBABILITY ==========\n"

            "Supports:\n"

            "- Pot Odds\n"

            "- Equity\n"

            "- Outs\n"

            "- Monte Carlo\n"

            "- Expected Value"

        )