from collections import defaultdict

from models.player import Player

class Statistics:
    """
    Tracks Texas Hold'em statistics.

    Responsibilities
    ----------------
    • Tournament statistics
    • Player statistics
    • Action tracking
    • AI analysis metrics

    This class only records data.
    It never changes gameplay.
    """

    def __init__(self):

        # ==================================================
        # Tournament Statistics
        # ==================================================

        self.hands_played = 0

        self.total_pot = 0

        self.biggest_pot = 0

        self.smallest_pot = 0

        self.total_showdowns = 0

        self.total_all_ins = 0

        # ==================================================
        # Player Statistics
        # ==================================================

        self.player_stats = defaultdict(

            lambda: {

                "hands_played": 0,

                "hands_won": 0,

                "chips_won": 0,

                "chips_lost": 0,

                # Poker metrics

                "vpip": 0,

                "pfr": 0,

                # Actions

                "folds": 0,

                "checks": 0,

                "calls": 0,

                "bets": 0,

                "raises": 0,

                "all_ins": 0,

                # Internal hand flags

                "vpip_recorded": False,

                "pfr_recorded": False

            }

        )

    # ==================================================
    # Tournament Tracking
    # ==================================================

    def record_hand(
        self,
        pot_size: int
    ):

        self.hands_played += 1

        self.total_pot += pot_size

        if (

            self.smallest_pot == 0

            or

            pot_size < self.smallest_pot

        ):

            self.smallest_pot = pot_size

        if pot_size > self.biggest_pot:

            self.biggest_pot = pot_size

    # --------------------------------------------------

    def record_showdown(self):

        self.total_showdowns += 1

    # --------------------------------------------------

    def record_all_in(self):

        self.total_all_ins += 1

    # ==================================================
    # Hand Tracking
    # ==================================================

    def record_player_hand(
        self,
        player: Player
    ):
        """
        Called when player enters a hand.
        """

        stats = self.player_stats[player]

        stats["hands_played"] += 1

        # Reset hand flags

        stats["vpip_recorded"] = False

        stats["pfr_recorded"] = False

    # ==================================================
    # Result Tracking
    # ==================================================

    def record_player_win(
        self,
        player: Player,
        chips: int
    ):

        stats = self.player_stats[player]

        stats["hands_won"] += 1

        stats["chips_won"] += chips

    # --------------------------------------------------

    def record_player_loss(
        self,
        player: Player,
        chips: int
    ):

        self.player_stats[player][

            "chips_lost"

        ] += chips

    # ==================================================
    # Action Tracking
    # ==================================================

    def record_fold(
        self,
        player: Player
    ):

        self.player_stats[player][

            "folds"

        ] += 1

    # --------------------------------------------------

    def record_check(
        self,
        player: Player
    ):

        self.player_stats[player][

            "checks"

        ] += 1

    # --------------------------------------------------

    def record_call(
        self,
        player: Player
    ):

        stats = self.player_stats[player]

        stats["calls"] += 1

        self._record_vpip(

            stats

        )

    # --------------------------------------------------

    def record_bet(
        self,
        player: Player
    ):

        stats = self.player_stats[player]

        stats["bets"] += 1

        self._record_vpip(

            stats

        )

    # --------------------------------------------------

    def record_raise(
        self,
        player: Player,
        preflop: bool = False
    ):

        stats = self.player_stats[player]

        stats["raises"] += 1

        self._record_vpip(

            stats

        )

        if preflop:

            self._record_pfr(

                stats

            )

    # --------------------------------------------------

    def record_all_in_player(
        self,
        player: Player
    ):

        self.player_stats[player][

            "all_ins"

        ] += 1

        self.total_all_ins += 1

    # ==================================================
    # Internal Helpers
    # ==================================================

    @staticmethod
    def _record_vpip(
        stats: dict
    ):

        if not stats["vpip_recorded"]:

            stats["vpip"] += 1

            stats["vpip_recorded"] = True

    # --------------------------------------------------

    @staticmethod
    def _record_pfr(
        stats: dict
    ):

        if not stats["pfr_recorded"]:

            stats["pfr"] += 1

            stats["pfr_recorded"] = True
        # ==================================================
    # Statistics Calculations
    # ==================================================

    def average_pot(self) -> float:
        """
        Average pot size.
        """

        if self.hands_played == 0:

            return 0.0

        return (

            self.total_pot

            /

            self.hands_played

        )

    # --------------------------------------------------

    def win_percentage(
        self,
        player: Player
    ) -> float:

        stats = self.player_stats[player]

        hands = stats["hands_played"]

        if hands == 0:

            return 0.0

        return (

            stats["hands_won"]

            /

            hands

        ) * 100

    # --------------------------------------------------

    def vpip_percentage(
        self,
        player: Player
    ) -> float:

        stats = self.player_stats[player]

        hands = stats["hands_played"]

        if hands == 0:

            return 0.0

        return (

            stats["vpip"]

            /

            hands

        ) * 100

    # --------------------------------------------------

    def pfr_percentage(
        self,
        player: Player
    ) -> float:

        stats = self.player_stats[player]

        hands = stats["hands_played"]

        if hands == 0:

            return 0.0

        return (

            stats["pfr"]

            /

            hands

        ) * 100

    # --------------------------------------------------

    def fold_percentage(
        self,
        player: Player
    ) -> float:
        """
        Percentage of hands folded.
        """

        stats = self.player_stats[player]

        hands = stats["hands_played"]

        if hands == 0:

            return 0.0

        return (

            stats["folds"]

            /

            hands

        ) * 100

    # --------------------------------------------------

    def aggression_factor(
        self,
        player: Player
    ) -> float:
        """
        Poker aggression factor.

        Formula:

        (Bets + Raises) / Calls
        """

        stats = self.player_stats[player]

        calls = stats["calls"]

        if calls == 0:

            return float(

                stats["bets"]

                +

                stats["raises"]

            )

        return (

            stats["bets"]

            +

            stats["raises"]

        ) / calls

    # ==================================================
    # Player Report
    # ==================================================

    def player_statistics(
        self,
        player: Player
    ) -> dict:
        """
        Return complete player report.
        """

        stats = self.player_stats[player].copy()

        stats.update(

            {

                "win_percentage":
                    self.win_percentage(player),

                "vpip_percentage":
                    self.vpip_percentage(player),

                "pfr_percentage":
                    self.pfr_percentage(player),

                "fold_percentage":
                    self.fold_percentage(player),

                "aggression_factor":
                    self.aggression_factor(player)

            }

        )

        return stats

    # ==================================================
    # Ranking Helpers
    # ==================================================

    def biggest_winner(
        self
    ):
        """
        Return player with most chips won.
        """

        if not self.player_stats:

            return None

        return max(

            self.player_stats,

            key=lambda player:

            self.player_stats[player]["chips_won"]

        )

    # --------------------------------------------------

    def biggest_loser(
        self
    ):
        """
        Return player with most chips lost.
        """

        if not self.player_stats:

            return None

        return max(

            self.player_stats,

            key=lambda player:

            self.player_stats[player]["chips_lost"]

        )

    # ==================================================
    # Reset
    # ==================================================

    def reset(self):
        """
        Clear all statistics.
        """

        self.hands_played = 0

        self.total_pot = 0

        self.biggest_pot = 0

        self.smallest_pot = 0

        self.total_showdowns = 0

        self.total_all_ins = 0

        self.player_stats.clear()

    # ==================================================
    # Debug
    # ==================================================

    def __repr__(self):

        return (

            "Statistics("

            f"hands={self.hands_played}, "

            f"showdowns={self.total_showdowns}"

            ")"

        )

    # --------------------------------------------------

    def __str__(self):

        return (

            "========== STATISTICS ==========\n"

            f"Hands Played : {self.hands_played}\n"

            f"Average Pot  : {self.average_pot():.2f}\n"

            f"Biggest Pot  : {self.biggest_pot}\n"

            f"Showdowns    : {self.total_showdowns}\n"

            f"All-Ins      : {self.total_all_ins}"

        )