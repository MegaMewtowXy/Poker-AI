from models.hand_result import HandResult
from models.player import Player

from engine.evaluator import HandEvaluator
from engine.pot_manager import PotManager

class Showdown:
    """
    Resolves Texas Hold'em showdown.

    Responsibilities
    ----------------

    • Validate showdown state
    • Evaluate hands
    • Build side pots
    • Resolve every pot
    • Handle ties
    • Return final results

    Does NOT:

    • Deal cards
    • Control betting
    • Manage game flow
    """

    def __init__(self):

        self.evaluator = HandEvaluator()

    # ==================================================
    # Validation
    # ==================================================

    def validate(
        self,
        players: list[Player],
        community_cards
    ):

        if len(players) < 2:

            raise ValueError(
                "At least two players are required."
            )

        if len(community_cards) != 5:

            raise ValueError(
                "Showdown requires exactly five community cards."
            )

    # ==================================================
    # Resolve Showdown
    # ==================================================

    def resolve(
        self,
        players: list[Player],
        community_cards,
        pot_manager: PotManager
    ):

        self.validate(

            players,

            community_cards

        )

        # ------------------------------------------
        # Active players
        # ------------------------------------------

        active_players = [

            player

            for player in players

            if player.is_active()

        ]

        if not active_players:

            return {

                "results": {},

                "pots": [],

                "winners": []

            }

        # ------------------------------------------
        # Everyone folded except one
        # ------------------------------------------

        if len(active_players) == 1:

            winner = active_players[0]

            pot_results = []

            for pot in pot_manager.get_all_pots():

                if pot.amount > 0:

                    pot_manager.award_pot(

                        winner,

                        pot

                    )

                    pot_results.append(

                        {

                            "pot": pot,

                            "eligible": [winner],

                            "winners": [winner]

                        }

                    )

            return {

                "results": {},

                "pots": pot_results,

                "winners": [winner]

            }

        # ------------------------------------------
        # Evaluate hands once
        # ------------------------------------------

        results = self.evaluate_players(

            active_players,

            community_cards

        )

        # ------------------------------------------
        # Build pots
        # ------------------------------------------

        pot_manager.build_side_pots()

        pots = pot_manager.get_all_pots()

        pot_results = []

        all_winners = []

        # ------------------------------------------
        # Resolve every pot
        # ------------------------------------------

        for pot in pots:

            eligible = pot_manager.eligible_players(

                pot,

                active_players

            )

            if not eligible:

                continue

            winners = self.find_best_players(

                eligible,

                results

            )

            self.resolve_pot(

                pot,

                winners,

                pot_manager

            )

            for winner in winners:

                if winner not in all_winners:

                    all_winners.append(

                        winner

                    )

            pot_results.append(

                {

                    "pot": pot,

                    "eligible": eligible,

                    "winners": winners

                }

            )

        return {

            "results": results,

            "pots": pot_results,

            "winners": all_winners

        }

    # ==================================================
    # Evaluation
    # ==================================================

    def evaluate_players(
        self,
        players: list[Player],
        community_cards
    ) -> dict[Player, HandResult]:

        results = {}

        for player in players:

            results[player] = self.evaluator.evaluate(

                player.hand,

                community_cards

            )

        return results
        # ==================================================
    # Winner Determination
    # ==================================================

    def find_best_players(
        self,
        players: list[Player],
        results: dict[Player, HandResult]
    ) -> list[Player]:
        """
        Return all players sharing strongest hand.

        Supports split pots.
        """

        if not players:

            return []

        best_score = min(

            results[player].score

            for player in players

        )

        return [

            player

            for player in players

            if results[player].score == best_score

        ]

    # --------------------------------------------------

    def winning_result(
        self,
        winners: list[Player],
        results: dict[Player, HandResult]
    ) -> HandResult:
        """
        Return winning hand result.
        """

        if not winners:

            return None

        return results[winners[0]]

    # --------------------------------------------------

    def winner_count(
        self,
        winners: list[Player]
    ) -> int:

        return len(winners)

    # --------------------------------------------------

    def has_tie(
        self,
        winners: list[Player]
    ) -> bool:

        return len(winners) > 1

    # ==================================================
    # Showdown Utilities
    # ==================================================

    def showdown_players(
        self,
        players: list[Player]
    ) -> list[Player]:
        """
        Return players reaching showdown.
        """

        return [

            player

            for player in players

            if player.is_active()

        ]

    # --------------------------------------------------

    def hand_results(
        self,
        players: list[Player],
        community_cards
    ):
        """
        Shortcut evaluation function.
        """

        return self.evaluate_players(

            self.showdown_players(players),

            community_cards

        )

    # ==================================================
    # Pot Resolution
    # ==================================================

    def award_pots(
        self,
        results: dict[Player, HandResult],
        pot_manager: PotManager
    ):
        """
        Award all pots.

        Useful when showdown
        is resolved externally.
        """

        active_players = list(

            results.keys()

        )

        resolved = []

        for pot in pot_manager.get_all_pots():

            eligible = pot_manager.eligible_players(

                pot,

                active_players

            )

            if not eligible:

                continue

            winners = self.find_best_players(

                eligible,

                results

            )

            self.resolve_pot(

                pot,

                winners,

                pot_manager

            )

            resolved.append(

                {

                    "pot": pot,

                    "eligible": eligible,

                    "winners": winners

                }

            )

        return resolved

    # --------------------------------------------------

    def resolve_pot(
        self,
        pot,
        winners: list[Player],
        pot_manager: PotManager
    ):
        """
        Resolve one pot.

        Handles:
        - single winner
        - split winner
        """

        if not winners:

            return

        if len(winners) == 1:

            pot_manager.award_pot(

                winners[0],

                pot

            )

        else:

            pot_manager.split_pot(

                winners,

                pot

            )

    # ==================================================
    # Winner Helpers
    # ==================================================

    def total_winners(
        self,
        results: dict[Player, HandResult]
    ):

        return self.find_best_players(

            list(results.keys()),

            results

        )

    # --------------------------------------------------

    def winning_player(
        self,
        results: dict[Player, HandResult]
    ):

        winners = self.total_winners(

            results

        )

        if len(winners) != 1:

            return None

        return winners[0]

    # ==================================================
    # Debug
    # ==================================================

    def __repr__(self):

        return "Showdown()"

    # --------------------------------------------------

    def __str__(self):

        return (

            "========== SHOWDOWN ==========\n"

            "Evaluator : HandEvaluator\n"

            "Pot Resolution : Enabled\n"

            "Side Pots : Enabled\n"

            "Split Pots : Enabled"

        )