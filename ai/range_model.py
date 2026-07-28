from copy import deepcopy

from models.player_position import PlayerPosition



class RangeModel:
    """
    Estimates possible opponent hands.

    Responsibilities
    ----------------
    • Maintain opponent range
    • Update range after actions
    • Adjust based on position
    • Adjust based on opponent style
    • Estimate range strength

    Does NOT:
        • Make decisions
        • Execute bets
        • Control gameplay
    """



    def __init__(
        self,
        opponent_name: str,
        opponent_type: str = "unknown"
    ):

        self.name = opponent_name

        self.opponent_type = opponent_type



        # ======================================
        # Default Starting Range
        # ======================================

        self.starting_range = {


            # Premium pairs

            "AA": 1.0,

            "KK": 1.0,

            "QQ": 1.0,

            "JJ": 1.0,

            "TT": 1.0,



            # Medium pairs

            "99": 0.8,

            "88": 0.7,

            "77": 0.6,



            # Big Ax hands

            "AK": 1.0,

            "AQ": 1.0,

            "AJ": 0.8,



            # Broadways

            "KQ": 0.8,

            "KJ": 0.5,

            "QJ": 0.5,

            "JT": 0.4,



            # Drawing categories

            "suited_connectors": 0.5,

            "small_pairs": 0.5,



            # Bluff category

            "bluffs": 0.3

        }



        self.range = deepcopy(

            self.starting_range

        )



        # ======================================
        # History Tracking
        # ======================================

        self.history = []

        self.observations = 0



        # Apply initial player style

        if opponent_type != "unknown":

            self.adjust_player_type(

                opponent_type

            )

            self.normalize_range()



    # ==========================================
    # Reset
    # ==========================================

    def reset(self):
        """
        Reset range at beginning of hand.
        """

        self.range = deepcopy(

            self.starting_range

        )

        self.history.clear()

        self.observations = 0



        if self.opponent_type != "unknown":

            self.adjust_player_type(

                self.opponent_type

            )

            self.normalize_range()



    # ==========================================
    # Observe Action
    # ==========================================

    def observe_action(
        self,
        action,
        position=None,
        opponent_type=None
    ):
        """
        Update opponent range after action.
        """

        self.history.append(

            {

                "action": action,

                "position": position,

                "opponent_type": opponent_type

            }

        )


        self.observations += 1



        action = action.lower()



        if action == "raise":

            self.narrow_after_raise(

                position

            )


        elif action == "call":

            self.narrow_after_call()



        elif action == "3bet":

            self.adjust_after_3bet()



        elif action == "fold":

            self.adjust_after_fold()



        if opponent_type:

            self.adjust_player_type(

                opponent_type

            )


        self.normalize_range()



    # ==========================================
    # Position Helper
    # ==========================================

    @staticmethod
    def normalize_position(
        position
    ):
        """
        Convert engine position enum
        into readable format.
        """

        if isinstance(

            position,

            PlayerPosition

        ):

            return position.name



        if isinstance(

            position,

            str

        ):

            return position.upper()



        return None



    # ==========================================
    # Raise Adjustment
    # ==========================================

    def narrow_after_raise(
        self,
        position=None
    ):
        """
        Update range after raise.

        Early positions:
            stronger range

        Late positions:
            wider stealing range
        """

        position = self.normalize_position(

            position

        )



        early_positions = {

            "UNDER_THE_GUN",

            "UNDER_THE_GUN_PLUS_ONE",

            "MIDDLE_POSITION"

        }



        late_positions = {

            "HIJACK",

            "CUTOFF",

            "BUTTON"

        }



        if position in early_positions:


            self.range["KQ"] *= 0.5

            self.range["KJ"] *= 0.5

            self.range["QJ"] *= 0.6

            self.range["bluffs"] *= 0.5



        elif position in late_positions:


            self.range["AJ"] *= 1.1

            self.range["KQ"] *= 1.1

            self.range["bluffs"] *= 1.3
        # ==========================================
    # Call Adjustment
    # ==========================================

    def narrow_after_call(
        self
    ):
        """
        Calling usually removes:

        • Pure bluffs
        • Some premium hands that would raise
        """

        self.range["bluffs"] *= 0.7

        self.range["AA"] *= 0.9

        self.range["KK"] *= 0.9



    # ==========================================
    # 3-Bet Adjustment
    # ==========================================

    def adjust_after_3bet(
        self
    ):
        """
        3-bet represents a strong range.
        """

        self.range["AA"] *= 1.2

        self.range["KK"] *= 1.2

        self.range["QQ"] *= 1.1

        self.range["AK"] *= 1.1

        self.range["bluffs"] *= 0.3



    # ==========================================
    # Fold Adjustment
    # ==========================================

    def adjust_after_fold(
        self
    ):
        """
        Folding gives little information.

        Reduce bluff frequency.
        """

        self.range["bluffs"] *= 0.5



    # ==========================================
    # Player Type Adjustment
    # ==========================================

    def adjust_player_type(
        self,
        opponent_type
    ):
        """
        Adjust range based on
        opponent playing style.
        """

        opponent_type = opponent_type.lower()



        # --------------------------------------
        # Loose Aggressive
        # --------------------------------------

        if opponent_type == "loose_aggressive":


            self.range["bluffs"] *= 1.5

            self.range["KQ"] *= 1.2

            self.range["AJ"] *= 1.1



        # --------------------------------------
        # Tight Aggressive
        # --------------------------------------

        elif opponent_type == "tight_aggressive":


            self.range["bluffs"] *= 0.6

            self.range["AA"] *= 1.1

            self.range["KK"] *= 1.1

            self.range["AK"] *= 1.1



        # --------------------------------------
        # Calling Station
        # --------------------------------------

        elif opponent_type == "calling_station":


            self.range["AQ"] *= 1.2

            self.range["KQ"] *= 1.2

            self.range["bluffs"] *= 0.5



        # --------------------------------------
        # Loose Passive
        # --------------------------------------

        elif opponent_type == "loose_passive":


            self.range["suited_connectors"] *= 1.2

            self.range["small_pairs"] *= 1.2



    # ==========================================
    # Remove Weak Hands
    # ==========================================

    def remove_weak_hands(
        self
    ):
        """
        Reduce weak holdings.
        """

        self.range["KJ"] *= 0.5

        self.range["QJ"] *= 0.5

        self.range["JT"] *= 0.5

        self.range["bluffs"] *= 0.5



    # ==========================================
    # Add Bluff Possibility
    # ==========================================

    def add_bluffs(
        self
    ):
        """
        Increase bluff probability.
        """

        self.range["bluffs"] *= 1.3



    # ==========================================
    # Normalize Range
    # ==========================================

    def normalize_range(
        self
    ):
        """
        Keep all range values
        between 0 and 1.
        """

        for hand in self.range:


            if self.range[hand] < 0:

                self.range[hand] = 0



            elif self.range[hand] > 1:

                self.range[hand] = 1



        return self.range



    # ==========================================
    # Range Strength
    # ==========================================

    def range_strength(
        self
    ):
        """
        Estimate opponent range strength.

        Scale:
        0 - 10
        """

        weights = {


            "AA": 10,

            "KK": 9,

            "QQ": 8,

            "JJ": 7,

            "TT": 6,


            "99": 5,

            "88": 4,

            "77": 3,


            "AK": 8,

            "AQ": 6,

            "AJ": 5,


            "KQ": 4,

            "KJ": 3,

            "QJ": 3,

            "JT": 2,


            "suited_connectors": 2,

            "small_pairs": 3,

            "bluffs": 0

        }



        total = 0

        probability_total = 0



        for hand, probability in self.range.items():


            weight = weights.get(

                hand,

                1

            )


            total += probability * weight

            probability_total += probability



        if probability_total == 0:

            return 0



        return round(

            total / probability_total,

            2

        )



    # ==========================================
    # Confidence
    # ==========================================

    def confidence(
        self
    ):
        """
        Confidence based on observations.
        """

        return round(

            min(

                self.observations / 20,

                1.0

            ),

            2

        )



    # ==========================================
    # Accessors
    # ==========================================

    def get_history(
        self
    ):

        return self.history.copy()



    def get_range(
        self
    ):

        return self.range.copy()



    # ==========================================
    # Profile
    # ==========================================

    def profile(
        self
    ):
        """
        Complete opponent range profile.
        """

        self.normalize_range()



        return {


            "name":

                self.name,


            "opponent_type":

                self.opponent_type,


            "range":

                self.range.copy(),


            "range_strength":

                self.range_strength(),


            "confidence":

                self.confidence(),


            "observations":

                self.observations

        }



    # ==========================================
    # Debug
    # ==========================================

    def __repr__(self):

        return (

            f"RangeModel("

            f"{self.name})"

        )



    def __str__(self):

        return (

            "Texas Hold'em "

            "Opponent Range Model"

        )