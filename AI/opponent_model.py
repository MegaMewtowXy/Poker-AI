from enum import Enum

class OpponentType(Enum):
    """
    Opponent playing styles.
    """

    UNKNOWN = "unknown"

    TIGHT_PASSIVE = "tight_passive"

    TIGHT_AGGRESSIVE = "tight_aggressive"

    LOOSE_PASSIVE = "loose_passive"

    LOOSE_AGGRESSIVE = "loose_aggressive"

    CALLING_STATION = "calling_station"

class OpponentModel:
    """
    Learns opponent behaviour.

    Tracks:
    - Playing frequency
    - Aggression
    - Folding habits
    - Raising patterns
    - Showdown behaviour

    Does NOT:
    - Make decisions
    - Control betting
    """

    def __init__(
        self,
        opponent_name: str
    ):

        self.name = opponent_name

        # ======================================
        # Hand Statistics
        # ======================================

        self.hands_played = 0

        self.hands_entered = 0

        self.preflop_raises = 0

        # ======================================
        # Action Statistics
        # ======================================

        self.total_bets = 0

        self.total_calls = 0

        self.total_folds = 0

        self.total_raises = 0

        # ======================================
        # Advanced Statistics
        # ======================================

        self.three_bets = 0

        self.fold_to_raise = 0

        self.showdowns = 0

        self.total_raise_amount = 0

        # ======================================
        # Tracking
        # ======================================

        self.observations = 0

        # Multi-Street Action Tracking
        self.street_actions = {
            "flop": {"bets": 0, "calls": 0, "folds": 0, "raises": 0},
            "turn": {"bets": 0, "calls": 0, "folds": 0, "raises": 0},
            "river": {"bets": 0, "calls": 0, "folds": 0, "raises": 0}
        }

    # ==========================================
    # Recording Actions
    # ==========================================

    def record_hand(
        self
    ):
        """
        Record observed hand.
        """

        self.hands_played += 1

    def record_entry(
        self
    ):
        """
        Opponent voluntarily entered pot.
        """

        self.hands_entered += 1

    def record_raise(
        self,
        amount=0
    ):
        """
        Record raise.
        """

        self.total_raises += 1

        self.total_raise_amount += amount

        self.observations += 1

    def record_preflop_raise(
        self
    ):
        """
        Record pre-flop raise.
        """

        self.preflop_raises += 1

    def record_three_bet(
        self
    ):
        """
        Record 3-bet.
        """

        self.three_bets += 1

    def record_bet(
        self
    ):
        """
        Record bet.
        """

        self.total_bets += 1

        self.observations += 1

    def record_call(
        self
    ):
        """
        Record call.
        """

        self.total_calls += 1

        self.observations += 1

    def record_fold(
        self
    ):
        """
        Record fold.
        """

        self.total_folds += 1

        self.observations += 1

    def record_fold_to_raise(
        self
    ):
        """
        Opponent folded after raise.
        """

        self.fold_to_raise += 1

    def record_showdown(
        self
    ):
        """
        Record showdown reached.
        """

        self.showdowns += 1

    def record_street_action(self, street: str, action: str):
        """
        Record action specific to a street ('flop', 'turn', 'river').
        """
        st = str(street).lower()
        act = str(action).lower()
        if st in self.street_actions and act in self.street_actions[st]:
            self.street_actions[st][act] += 1
        # ==========================================
    # Statistics
    # ==========================================

    def vpip(
        self
    ):
        """
        Voluntarily Put Money In Pot %.
        """

        if self.hands_played == 0:

            return 0.0

        return round(

            (

                self.hands_entered

                /

                self.hands_played

            )

            *

            100,

            2

        )

    # ------------------------------------------

    def pfr(
        self
    ):
        """
        Pre-flop Raise %.
        """

        if self.hands_played == 0:

            return 0.0

        return round(

            (

                self.preflop_raises

                /

                self.hands_played

            )

            *

            100,

            2

        )

    # ------------------------------------------

    def aggression_factor(
        self
    ):
        """
        Aggression Factor:

        (Bets + Raises) / Calls
        """

        aggressive_actions = (

            self.total_bets

            +

            self.total_raises

        )

        if self.total_calls == 0:

            return round(

                float(aggressive_actions),

                2

            )

        return round(

            aggressive_actions

            /

            self.total_calls,

            2

        )

    # ------------------------------------------

    def aggression_frequency(
        self
    ):
        """
        Percentage of actions that are aggressive.

        Formula:

        (Bets + Raises) / Total Actions
        """

        total_actions = (

            self.total_bets

            +

            self.total_calls

            +

            self.total_folds

            +

            self.total_raises

        )

        if total_actions == 0:

            return 0.0

        return round(

            (

                (

                    self.total_bets

                    +

                    self.total_raises

                )

                /

                total_actions

            )

            *

            100,

            2

        )

    # ------------------------------------------

    def fold_percentage(
        self
    ):
        """
        Folding frequency.
        """

        total_actions = (

            self.total_folds

            +

            self.total_calls

            +

            self.total_bets

            +

            self.total_raises

        )

        if total_actions == 0:

            return 0.0

        return round(

            (

                self.total_folds

                /

                total_actions

            )

            *

            100,

            2

        )

    # ------------------------------------------

    def three_bet_percentage(
        self
    ):
        """
        3-bet frequency.
        """

        if self.hands_played == 0:

            return 0.0

        return round(

            (

                self.three_bets

                /

                self.hands_played

            )

            *

            100,

            2

        )

    # ------------------------------------------

    def average_raise_size(
        self
    ):
        """
        Average raise amount.
        """

        if self.total_raises == 0:

            return 0

        return round(

            self.total_raise_amount

            /

            self.total_raises,

            2

        )

    # ------------------------------------------

    def showdown_frequency(
        self
    ):
        """
        How often opponent reaches showdown.
        """

        if self.hands_played == 0:

            return 0.0

        return round(

            (

                self.showdowns

                /

                self.hands_played

            )

            *

            100,

            2

        )

    # ==========================================
    # Classification
    # ==========================================

    def classify(
        self
    ) -> OpponentType:
        """
        Classify opponent style.
        """

        if self.hands_played < 10:

            return OpponentType.UNKNOWN

        vpip = self.vpip()

        aggression = self.aggression_factor()

        if (

            vpip >= 40

            and

            aggression < 1

        ):

            return OpponentType.CALLING_STATION

        if vpip >= 35:

            if aggression >= 1.5:

                return OpponentType.LOOSE_AGGRESSIVE

            return OpponentType.LOOSE_PASSIVE

        if vpip < 25:

            if aggression >= 1.5:

                return OpponentType.TIGHT_AGGRESSIVE

            return OpponentType.TIGHT_PASSIVE

        return OpponentType.UNKNOWN

    # ==========================================
    # Threat Level
    # ==========================================

    def threat_level(
        self
    ):
        """
        Estimate opponent danger.

        Range:
        0 - 10
        """

        threat = 5

        style = self.classify()

        if style == OpponentType.LOOSE_AGGRESSIVE:

            threat += 3

        elif style == OpponentType.TIGHT_AGGRESSIVE:

            threat += 2

        elif style == OpponentType.CALLING_STATION:

            threat += 1

        elif style == OpponentType.LOOSE_PASSIVE:

            threat -= 1

        elif style == OpponentType.TIGHT_PASSIVE:

            threat -= 2

        if self.three_bet_percentage() > 8:

            threat += 1

        return max(

            0,

            min(

                10,

                threat

            )

        )

    # ==========================================
    # Confidence
    # ==========================================

    def confidence(
        self
    ):
        """
        Confidence increases with
        observed hands.
        """

        return round(

            min(

                self.hands_played / 100,

                1.0

            ),

            2

        )

    # ==========================================
    # Profiles
    # ==========================================

    def profile(
        self
    ):
        """
        Return opponent statistics.
        """

        return {

            "name":

                self.name,

            "hands_played":

                self.hands_played,

            "VPIP":

                self.vpip(),

            "PFR":

                self.pfr(),

            "aggression":

                self.aggression_factor(),

            "aggression_frequency":

                self.aggression_frequency(),

            "fold_percentage":

                self.fold_percentage(),

            "3bet_percentage":

                self.three_bet_percentage(),

            "average_raise_size":

                self.average_raise_size(),

            "showdown_frequency":

                self.showdown_frequency()

        }

    # ------------------------------------------

    def ai_profile(
        self
    ):
        """
        Complete information used by AI.
        """

        return {

            **self.profile(),

            "type":

                self.classify().value,

            "threat_level":

                self.threat_level(),

            "confidence":

                self.confidence()

        }

    # ==========================================
    # Debug
    # ==========================================

    def __repr__(self):

        return (

            f"OpponentModel("

            f"{self.name})"

        )

    def __str__(self):

        return (

            "Texas Hold'em "

            "Opponent Behaviour Model"

        )