from models.hand_result import HandResult
from models.player import Player

from engine.evaluator import HandEvaluator
from engine.pot_manager import PotManager


class Showdown:
    """
    Resolves the end of a Texas Hold'em hand.

    Responsibilities
    ----------------
    • Evaluate remaining players
    • Build side pots
    • Award every pot
    • Return showdown results

    This class does NOT:
        • Deal cards
        • Control betting
        • Print UI
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
        """
        Validate showdown inputs.
        """

        if len(players) < 2:

            raise ValueError(
                "At least two players are required."
            )

        if len(community_cards) != 5:

            raise ValueError(
                "Showdown requires exactly five community cards."
            )

    # ==================================================
    # Showdown
    # ==================================================

    def resolve(
        self,
        players: list[Player],
        community_cards,
        pot_manager: PotManager
    ):
        """
        Resolve an entire showdown.

        Returns
        -------
        dict[Player, HandResult]
            Every active player's hand result.
        """

        self.validate(
            players,
            community_cards
        )

        active_players = [

            player

            for player in players

            if not player.folded

        ]

        results = self.evaluate_players(
            active_players,
            community_cards
        )

        pot_manager.build_side_pots()

        self.award_pots(
            results,
            pot_manager
        )

        return results
        # ==================================================
    # Evaluation
    # ==================================================

    def evaluate_players(
        self,
        players: list[Player],
        community_cards
    ) -> dict[Player, HandResult]:
        """
        Evaluate every remaining player.
        """

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
        Return every player tied for the
        best hand.
        """

        if not players:

            return []

        best_score = min(

            results[player].score

            for player in players

        )

        winners = [

            player

            for player in players

            if results[player].score == best_score

        ]

        return winners

    # --------------------------------------------------

    def winning_result(
        self,
        winners: list[Player],
        results: dict[Player, HandResult]
    ) -> HandResult:
        """
        Return the winning HandResult.

        Assumes winners is non-empty.
        """

        return results[
            winners[0]
        ]

    # --------------------------------------------------

    def winner_count(
        self,
        winners: list[Player]
    ) -> int:
        """
        Number of winning players.
        """

        return len(winners)

    # --------------------------------------------------

    def has_tie(
        self,
        winners: list[Player]
    ) -> bool:
        """
        Returns True if multiple players
        share the best hand.
        """

        return len(winners) > 1
        # ==================================================
    # Pot Resolution
    # ==================================================

    def award_pots(
        self,
        results: dict[Player, HandResult],
        pot_manager: PotManager
    ):
        """
        Resolve the main pot and every side pot.
        """

        active_players = list(
            results.keys()
        )

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

    # --------------------------------------------------

    def resolve_pot(
        self,
        pot,
        winners: list[Player],
        pot_manager: PotManager
    ):
        """
        Award a single pot.
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

    # --------------------------------------------------

    def total_winners(
        self,
        results: dict[Player, HandResult]
    ) -> list[Player]:
        """
        Return every player tied for
        the overall best hand.
        """

        return self.find_best_players(
            list(results.keys()),
            results
        )

    # --------------------------------------------------

    def winning_player(
        self,
        results: dict[Player, HandResult]
    ) -> Player | None:
        """
        Return the sole winner if one exists.
        Otherwise return None.
        """

        winners = self.total_winners(
            results
        )

        if len(winners) != 1:

            return None

        return winners[0]
        # ==================================================
    # Utility
    # ==================================================

    def showdown_players(
        self,
        players: list[Player]
    ) -> list[Player]:
        """
        Return every player that reaches
        showdown.
        """

        return [

            player

            for player in players

            if not player.folded

        ]

    # --------------------------------------------------

    def hand_results(
        self,
        players: list[Player],
        community_cards
    ) -> dict[Player, HandResult]:
        """
        Convenience wrapper for evaluating
        showdown players.
        """

        return self.evaluate_players(
            self.showdown_players(players),
            community_cards
        )

    # ==================================================
    # Debug
    # ==================================================

    def __repr__(self):

        return "Showdown()"

    # --------------------------------------------------

    def __str__(self):

        return (

            "========== SHOWDOWN ==========\n"

            "Evaluator : HandEvaluator"

        )