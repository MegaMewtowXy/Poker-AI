from enum import Enum


class OpponentType(Enum):
    """
    Classification of opponent playing style.
    """

    UNKNOWN = "unknown"

    TIGHT_PASSIVE = "tight_passive"

    TIGHT_AGGRESSIVE = "tight_aggressive"

    LOOSE_PASSIVE = "loose_passive"

    LOOSE_AGGRESSIVE = "loose_aggressive"



class OpponentModel:
    """
    Learns opponent behaviour.

    Responsibilities
    ----------------
    • Track opponent actions
    • Calculate statistics
    • Classify playing style

    This class does NOT:
        • Make betting decisions
        • Control the game
    """


    def __init__(
        self,
        opponent_name: str
    ):

        self.name = opponent_name


        # ======================================
        # Basic Counters
        # ======================================

        self.hands_played = 0

        self.hands_entered = 0

        self.preflop_raises = 0

        self.total_bets = 0

        self.total_calls = 0

        self.total_folds = 0



    # ==========================================
    # Recording Actions
    # ==========================================

    def record_hand(
        self
    ):
        """
        Record that opponent played a hand.
        """

        self.hands_played += 1



    def record_entry(
        self
    ):
        """
        Opponent entered the pot.
        """

        self.hands_entered += 1



    def record_raise(
        self
    ):
        """
        Record raise action.
        """

        self.preflop_raises += 1



    def record_bet(
        self
    ):
        """
        Record betting aggression.
        """

        self.total_bets += 1



    def record_call(
        self
    ):
        """
        Record call.
        """

        self.total_calls += 1



    def record_fold(
        self
    ):
        """
        Record fold.
        """

        self.total_folds += 1
        # ==========================================
    # Statistics
    # ==========================================

    def vpip(self) -> float:
        """
        Voluntarily Put Money In Pot percentage.
        """

        if self.hands_played == 0:

            return 0.0


        return (

            self.hands_entered

            /

            self.hands_played

        ) * 100



    # --------------------------------------------------


    def pfr(self) -> float:
        """
        Preflop Raise percentage.
        """

        if self.hands_played == 0:

            return 0.0


        return (

            self.preflop_raises

            /

            self.hands_played

        ) * 100



    # --------------------------------------------------


    def aggression_factor(self) -> float:
        """
        Betting aggression.

        Formula:

        (Bets + Raises) / Calls
        """

        if self.total_calls == 0:

            return float(
                self.total_bets
            )


        return (

            self.total_bets

            /

            self.total_calls

        )



    # --------------------------------------------------


    def fold_percentage(self) -> float:
        """
        How often opponent folds.
        """

        total_actions = (

            self.total_folds

            +

            self.total_calls

            +

            self.total_bets

        )


        if total_actions == 0:

            return 0.0


        return (

            self.total_folds

            /

            total_actions

        ) * 100



    # ==========================================
    # Profile
    # ==========================================

    def profile(self) -> dict:
        """
        Return complete opponent statistics.
        """

        return {

            "name":

                self.name,


            "hands_played":

                self.hands_played,


            "VPIP":

                round(
                    self.vpip(),
                    2
                ),


            "PFR":

                round(
                    self.pfr(),
                    2
                ),


            "aggression":

                round(
                    self.aggression_factor(),
                    2
                ),


            "fold_percentage":

                round(
                    self.fold_percentage(),
                    2
                )

        }
        # ==========================================
    # Opponent Classification
    # ==========================================

    def classify(
        self
    ) -> OpponentType:
        """
        Classify opponent playing style.
        """


        vpip = self.vpip()

        aggression = self.aggression_factor()



        # Not enough information

        if self.hands_played < 10:

            return OpponentType.UNKNOWN



        # Loose players

        if vpip >= 40:


            if aggression >= 2:

                return OpponentType.LOOSE_AGGRESSIVE


            return OpponentType.LOOSE_PASSIVE



        # Tight players

        else:


            if aggression >= 2:

                return OpponentType.TIGHT_AGGRESSIVE


            return OpponentType.TIGHT_PASSIVE



    # ==========================================
    # AI Information
    # ==========================================

    def threat_level(
        self
    ) -> int:
        """
        Estimate opponent danger.

        Range:
        0 - 10
        """


        threat = 5


        opponent_type = self.classify()



        if opponent_type == OpponentType.LOOSE_AGGRESSIVE:

            threat += 3



        elif opponent_type == OpponentType.TIGHT_AGGRESSIVE:

            threat += 2



        elif opponent_type == OpponentType.LOOSE_PASSIVE:

            threat -= 1



        elif opponent_type == OpponentType.TIGHT_PASSIVE:

            threat -= 2



        return max(

            0,

            min(

                10,

                threat

            )

        )



    # ==========================================
    # Final Opponent Profile
    # ==========================================

    def ai_profile(
        self
    ) -> dict:
        """
        Complete information for AI decisions.
        """


        return {

            **self.profile(),


            "type":

                self.classify().value,


            "threat_level":

                self.threat_level()

        }



    # ==========================================
    # Debug
    # ==========================================

    def __repr__(self):

        return (

            f"OpponentModel("
            f"{self.name})"

        )