from models.card import Card
from models.player import Player

from engine.evaluator import HandEvaluator

class Probability:
    """
    Poker probability and mathematical analysis.

    Responsibilities
    ----------------
    • Pot odds
    • Implied odds
    • Outs calculation
    • Drawing probability
    • Hand evaluation
    • Monte Carlo equity
    • EV calculations

    Simulation safety:
    ------------------
    This class never modifies:
    - Player state
    - Opponent state
    - Deck state
    - Table state
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

        if call_amount <= 0:

            return 0.0

        if pot_size < 0:

            raise ValueError(
                "Pot size cannot be negative."
            )

        return call_amount / (

            pot_size + call_amount

        )

    # --------------------------------------------------

    @staticmethod
    def pot_odds_percentage(
        call_amount: int,
        pot_size: int
    ) -> float:

        return Probability.pot_odds(

            call_amount,

            pot_size

        ) * 100

    # ==================================================
    # Implied Odds
    # ==================================================

    @staticmethod
    def implied_odds(
        call_amount: int,
        current_pot: int,
        expected_future_chips: int
    ) -> float:

        if call_amount <= 0:

            return 0.0

        return (

            current_pot

            +

            expected_future_chips

        ) / call_amount

    # ==================================================
    # Hand Evaluation
    # ==================================================

    def hand_strength(
        self,
        hole_cards: list[Card],
        community_cards: list[Card]
    ):

        return self.evaluator.evaluate(

            hole_cards,

            community_cards

        )

    # ==================================================
    # Outs
    # ==================================================

    @staticmethod
    def calculate_outs(
        winning_cards: int,
        unseen_cards: int = 47
    ) -> int:

        if winning_cards < 0:

            return 0

        return min(

            winning_cards,

            unseen_cards

        )

    # --------------------------------------------------

    @staticmethod
    def one_card_draw_probability(
        outs: int,
        unseen_cards: int
    ) -> float:

        if unseen_cards <= 0:

            return 0.0

        outs = Probability.calculate_outs(

            outs,

            unseen_cards

        )

        return outs / unseen_cards

    # --------------------------------------------------

    @staticmethod
    def two_card_draw_probability(
        outs: int,
        unseen_cards: int
    ) -> float:

        if unseen_cards <= 1:

            return 0.0

        outs = Probability.calculate_outs(

            outs,

            unseen_cards

        )

        miss_one = (

            unseen_cards - outs

        ) / unseen_cards

        miss_two = (

            unseen_cards - outs - 1

        ) / (

            unseen_cards - 1

        )

        return 1 - (

            miss_one * miss_two

        )

    # ==================================================
    # Draw Helpers
    # ==================================================

    @staticmethod
    def flush_draw_outs(
        suit_cards: int
    ) -> int:

        return max(

            0,

            13 - suit_cards

        )

    # --------------------------------------------------

    @staticmethod
    def straight_draw_outs(
        possible_cards: int
    ) -> int:

        return max(

            0,

            possible_cards

        )

    # ==================================================
    # Probability Helpers
    # ==================================================

    @staticmethod
    def normalize_probability(
        value: float
    ) -> float:

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

        return Probability.normalize_probability(

            probability

        ) * 100
        # ==================================================
    # Monte Carlo Equity
    # ==================================================

    def monte_carlo_equity(
        self,
        player: Player,
        opponents: list[Player],
        community_cards: list[Card],
        deck,
        simulations: int = 10000
    ) -> dict:
        """
        Estimate hand equity using Monte Carlo.

        Returns:

        {
            win,
            tie,
            lose,
            equity
        }

        Does not modify:
        - Player objects
        - Opponent objects
        - Original deck
        """

        if simulations <= 0:

            raise ValueError(
                "Simulations must be positive."
            )

        if not opponents:

            raise ValueError(
                "At least one opponent is required."
            )

        wins = 0

        ties = 0

        losses = 0

        for _ in range(simulations):

            result = self._simulate_once(

                player,

                opponents,

                community_cards,

                deck

            )

            if result == "win":

                wins += 1

            elif result == "tie":

                ties += 1

            else:

                losses += 1

        total = simulations

        return {

            "win": wins / total,

            "tie": ties / total,

            "lose": losses / total,

            "equity": (

                wins

                +

                ties

                *

                0.5

            ) / total

        }

    # ==================================================
    # Single Simulation
    # ==================================================

    def _simulate_once(
        self,
        player: Player,
        opponents: list[Player],
        community_cards: list[Card],
        deck
    ) -> str:
        """
        Run one simulation.

        Uses copies only.
        """

        simulation_deck = deck.clone()

        # ----------------------------------------------
        # Remove known cards
        # ----------------------------------------------

        known_cards = []

        known_cards.extend(

            player.hand

        )

        known_cards.extend(

            community_cards

        )

        for opponent in opponents:

            known_cards.extend(

                opponent.hand

            )

        simulation_deck.remove_cards(

            known_cards

        )

        # ----------------------------------------------
        # Create simulated opponents
        # ----------------------------------------------

        simulated_opponents = []

        for _ in opponents:

            simulated_opponents.append(

                simulation_deck.deal_many(

                    2

                )

            )

        # ----------------------------------------------
        # Complete board
        # ----------------------------------------------

        simulated_board = community_cards.copy()

        missing_cards = (

            5

            -

            len(simulated_board)

        )

        if missing_cards > 0:

            simulated_board.extend(

                simulation_deck.deal_many(

                    missing_cards

                )

            )

        # ----------------------------------------------
        # Evaluate hero
        # ----------------------------------------------

        hero_result = self.evaluator.evaluate(

            player.hand,

            simulated_board

        )

        hero_score = hero_result.score

        # ----------------------------------------------
        # Compare opponents
        # ----------------------------------------------

        hero_wins = True

        hero_ties = 0

        for opponent_hand in simulated_opponents:

            opponent_result = self.evaluator.evaluate(

                opponent_hand,

                simulated_board

            )

            opponent_score = opponent_result.score

            if hero_score > opponent_score:

                hero_wins = False

                return "lose"

            elif hero_score == opponent_score:

                hero_ties += 1

        # Beat everyone

        if hero_wins and hero_ties == 0:

            return "win"

        # Tie with all remaining players

        return "tie"

    # ==================================================
    # Expected Value
    # ==================================================

    @staticmethod
    def expected_value(
        win_probability: float,
        lose_probability: float,
        pot_reward: int,
        investment: int
    ) -> float:

        return (

            win_probability

            *

            pot_reward

        ) - (

            lose_probability

            *

            investment

        )

    # --------------------------------------------------

    @staticmethod
    def call_ev(
        equity: float,
        pot_size: int,
        call_amount: int
    ) -> float:

        return (

            equity

            *

            (

                pot_size

                +

                call_amount

            )

        ) - call_amount

    # ==================================================
    # AI Decision Helpers
    # ==================================================

    @staticmethod
    def should_call(
        equity: float,
        pot_odds: float
    ) -> bool:

        return equity >= pot_odds

    # --------------------------------------------------

    @staticmethod
    def hand_category_score(
        hand_result
    ) -> float:

        if hand_result is None:

            return 0.0

        rank = hand_result.rank

        score = (

            10 - rank

        ) / 10

        return Probability.normalize_probability(

            score

        )

    # ==================================================
    # Debug
    # ==================================================

    def __repr__(self):

        return "Probability()"

    # --------------------------------------------------

    def __str__(self):

        return (

            "Texas Hold'em "

            "Probability Engine"

        )