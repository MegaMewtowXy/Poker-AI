from engine.evaluator import HandEvaluator
from engine.pot_manager import PotManager


class Showdown:
    """
    Handles showdown and pot distribution.
    """

    def __init__(self):

        self.evaluator = HandEvaluator()

    # ==================================================
    # Hand Evaluation
    # ==================================================

    def evaluate_players(
        self,
        players,
        community_cards
    ):
        """
        Evaluate every active player's hand.

        Returns
        -------
        list[(Player, HandResult)]
        """

        results = []

        for player in players:

            if player.folded:
                continue

            result = self.evaluator.evaluate(
                player.hand,
                community_cards
            )

            results.append(
                (player, result)
            )

        return results

    # ==================================================
    # Winner Determination
    # ==================================================

    def determine_winner(
        self,
        evaluated_players
    ):
        """
        Returns the winning player and hand.
        """

        winner = evaluated_players[0]

        for player, result in evaluated_players[1:]:

            if result.score < winner[1].score:

                winner = (player, result)

        return winner

    # ==================================================
    # Pot Distribution
    # ==================================================

    def distribute_main_pot(
        self,
        winner,
        pot_manager: PotManager
    ):
        """
        Give the main pot to the winner.
        """

        winner.win_chips(
            pot_manager.main_pot.amount
        )

    def distribute_side_pots(
        self,
        pot_manager: PotManager
    ):
        """
        Side pots will be implemented later.
        """

        pass

    # ==================================================
    # Resolve Showdown
    # ==================================================

    def resolve(
        self,
        players,
        community_cards,
        pot_manager: PotManager
    ):
        """
        Resolve an entire showdown.

        Returns
        -------
        (winner, hand_result)
        """

        evaluated = self.evaluate_players(
            players,
            community_cards
        )

        print()

        print("Player Results")

        print("----------------------------")

        for player, result in evaluated:

            print(
                f"{player.name:<12}"
                f"{result.hand_name:<20}"
                f"Score: {result.score}"
            )

        print()

        winner, result = self.determine_winner(
            evaluated
        )

        self.distribute_main_pot(
            winner,
            pot_manager
        )

        self.distribute_side_pots(
            pot_manager
        )

        return winner, result