from collections import defaultdict

from models.player import Player


class Statistics:
    """
    Tracks statistics for a Texas Hold'em game.

    Responsibilities
    ----------------
    • Player statistics
    • Hand statistics
    • Tournament statistics

    This class never changes gameplay.
    It only records information.
    """

    def __init__(self):

        # ==========================================
        # Tournament
        # ==========================================

        self.hands_played = 0

        self.total_pot = 0

        self.biggest_pot = 0

        self.smallest_pot = 0

        self.total_showdowns = 0

        self.total_all_ins = 0

        # ==========================================
        # Per Player Statistics
        # ==========================================

        self.player_stats = defaultdict(

            lambda: {

                "hands_played": 0,

                "hands_won": 0,

                "chips_won": 0,

                "chips_lost": 0,

                "vpip": 0,

                "pfr": 0,

                "folds": 0,

                "checks": 0,

                "calls": 0,

                "bets": 0,

                "raises": 0,

                "all_ins": 0

            }

        )

    # ==================================================
    # Tournament
    # ==================================================

    def record_hand(
        self,
        pot_size: int
    ):
        """
        Record a completed hand.
        """

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
    # Player Statistics
    # ==================================================

    def record_player_hand(
        self,
        player: Player
    ):
        """
        Record that the player participated
        in a hand.
        """

        self.player_stats[player][
            "hands_played"
        ] += 1

    # --------------------------------------------------

    def record_player_win(
        self,
        player: Player,
        chips: int
    ):
        """
        Record a winning hand.
        """

        stats = self.player_stats[player]

        stats["hands_won"] += 1

        stats["chips_won"] += chips

    # --------------------------------------------------

    def record_player_loss(
        self,
        player: Player,
        chips: int
    ):
        """
        Record chips lost.
        """

        self.player_stats[player][
            "chips_lost"
        ] += chips

    # ==================================================
    # Player Actions
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

        stats["vpip"] += 1

    # --------------------------------------------------

    def record_bet(
        self,
        player: Player
    ):

        stats = self.player_stats[player]

        stats["bets"] += 1

        stats["vpip"] += 1

    # --------------------------------------------------

    def record_raise(
        self,
        player: Player
    ):

        stats = self.player_stats[player]

        stats["raises"] += 1

        stats["vpip"] += 1

        stats["pfr"] += 1

    # --------------------------------------------------

    def record_all_in(
        self,
        player: Player
    ):

        self.player_stats[player][
            "all_ins"
        ] += 1

        self.total_all_ins += 1
        # ==================================================
    # Statistics
    # ==================================================

    def average_pot(self) -> float:
        """
        Returns the average pot size.
        """

        if self.hands_played == 0:

            return 0.0

        return self.total_pot / self.hands_played

    # --------------------------------------------------

    def win_percentage(
        self,
        player: Player
    ) -> float:
        """
        Returns the player's win percentage.
        """

        stats = self.player_stats[player]

        hands = stats["hands_played"]

        if hands == 0:

            return 0.0

        return (

            stats["hands_won"] / hands

        ) * 100

    # --------------------------------------------------

    def vpip_percentage(
        self,
        player: Player
    ) -> float:
        """
        Voluntarily Put Money In Pot percentage.
        """

        stats = self.player_stats[player]

        hands = stats["hands_played"]

        if hands == 0:

            return 0.0

        return (

            stats["vpip"] / hands

        ) * 100

    # --------------------------------------------------

    def pfr_percentage(
        self,
        player: Player
    ) -> float:
        """
        Pre-Flop Raise percentage.
        """

        stats = self.player_stats[player]

        hands = stats["hands_played"]

        if hands == 0:

            return 0.0

        return (

            stats["pfr"] / hands

        ) * 100

    # --------------------------------------------------

    def player_statistics(
        self,
        player: Player
    ) -> dict:
        """
        Return all recorded statistics
        for a player.
        """

        return dict(

            self.player_stats[player]

        )

    # ==================================================
    # Reset
    # ==================================================

    def reset(self):
        """
        Clear all recorded statistics.
        """

        self.__init__()

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

            f"Hands Played    : {self.hands_played}\n"

            f"Average Pot     : {self.average_pot():.2f}\n"

            f"Biggest Pot     : {self.biggest_pot}\n"

            f"Showdowns       : {self.total_showdowns}\n"

            f"All-Ins         : {self.total_all_ins}"

        )