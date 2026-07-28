from dataclasses import dataclass, field
from typing import Optional

from models.card import Card



@dataclass(slots=True)
class HandResult:
    """
    Complete poker hand evaluation result.

    Used by:
    - HandEvaluator
    - Showdown
    - AI analysis
    - Monte Carlo simulation
    """


    # =====================================================
    # Evaluation
    # =====================================================

    score: int

    rank: int

    hand_name: str

    best_five: list[Card] = field(
        default_factory=list
    )



    # =====================================================
    # AI Data
    # =====================================================

    win_probability: Optional[float] = None

    equity: Optional[float] = None

    hand_strength: Optional[float] = None

    confidence: Optional[float] = None

    explanation: str = ""



    # =====================================================
    # Showdown
    # =====================================================

    is_winner: bool = False

    chips_won: int = 0

    split_pot: bool = False



    showdown_message: str = ""



    # =====================================================
    # Validation
    # =====================================================

    def __post_init__(self):

        if self.score < 0:

            raise ValueError(
                "Hand score cannot be negative."
            )


        if not 0 <= self.rank <= 9:

            raise ValueError(
                "Invalid poker hand rank."
            )



    # =====================================================
    # AI Helpers
    # =====================================================

    def set_ai_analysis(
        self,
        win_probability: float,
        equity: float,
        hand_strength: float,
        confidence: float,
        explanation: str
    ):


        if not 0 <= win_probability <= 1:

            raise ValueError(
                "Win probability must be between 0 and 1."
            )


        if not 0 <= confidence <= 1:

            raise ValueError(
                "Confidence must be between 0 and 1."
            )


        self.win_probability = win_probability

        self.equity = equity

        self.hand_strength = hand_strength

        self.confidence = confidence

        self.explanation = explanation



    # =====================================================
    # Showdown Helpers
    # =====================================================

    def mark_winner(
        self,
        chips_won: int,
        split_pot: bool = False
    ):


        self.is_winner = True

        self.chips_won = chips_won

        self.split_pot = split_pot



    # -----------------------------------------------------

    def reset_showdown(self):

        self.is_winner = False

        self.chips_won = 0

        self.split_pot = False



        self.showdown_message = ""



    # =====================================================
    # Hand Classification
    # =====================================================

    @property
    def is_royal_flush(self):

        return (
            self.hand_name
            ==
            "Royal Flush"
        )


    @property
    def is_pair(self):

        return (
            "Pair"
            in
            self.hand_name
        )



    @property
    def has_ai_analysis(self):

        return (

            self.win_probability is not None

            and

            self.hand_strength is not None

        )



    @property
    def lost(self):

        return not self.is_winner



    # =====================================================
    # Comparison
    # =====================================================

    def __lt__(
        self,
        other
    ):

        if not isinstance(
            other,
            HandResult
        ):

            return NotImplemented


        # Lower Treys score wins

        return self.score < other.score



    # =====================================================
    # Debug
    # =====================================================

    def __repr__(self):

        return (

            "HandResult("

            f"hand='{self.hand_name}', "

            f"score={self.score}, "

            f"winner={self.is_winner}"

            ")"

        )



    # -----------------------------------------------------

    def __str__(self):

        text = [

            f"Hand : {self.hand_name}",

            f"Score : {self.score}"

        ]


        if self.win_probability is not None:

            text.append(

                f"Win Probability : "
                f"{self.win_probability:.2%}"

            )


        if self.hand_strength is not None:

            text.append(

                f"Hand Strength : "
                f"{self.hand_strength:.3f}"

            )


        if self.confidence is not None:

            text.append(

                f"Confidence : "
                f"{self.confidence:.2%}"

            )


        if self.is_winner:

            text.append(

                f"Winner (+{self.chips_won} chips)"

            )


        return "\n".join(text)