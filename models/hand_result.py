from dataclasses import dataclass, field
from typing import Optional

from models.card import Card


@dataclass(slots=True)
class HandResult:
    """
    Represents the evaluation of a player's hand.

    Produced by HandEvaluator and later enriched
    by Monte Carlo simulations and AI analysis.
    """

    # =====================================================
    # Hand Evaluation
    # =====================================================

    # Treys score (lower is better)
    score: int

    # Treys rank class (0-9 depending on evaluator)
    rank: int

    # Human-readable name
    hand_name: str

    # Best five cards that form the hand
    best_five: list[Card] = field(
        default_factory=list
    )

    # =====================================================
    # AI Information
    # =====================================================

    # Probability of winning (0.0 - 1.0)
    win_probability: Optional[float] = None

    # Hand equity from Monte Carlo
    equity: Optional[float] = None

    # Strength score used by AI
    hand_strength: Optional[float] = None

    # Confidence of AI recommendation
    confidence: Optional[float] = None

    # AI explanation
    explanation: str = ""

    # =====================================================
    # Showdown Information
    # =====================================================

    # Did this hand win?
    is_winner: bool = False

    # Pot won
    chips_won: int = 0

    # Was the pot split?
    split_pot: bool = False
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
        """
        Store AI analysis results.
        """

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
        """
        Mark this hand as a winner.
        """

        self.is_winner = True
        self.chips_won = chips_won
        self.split_pot = split_pot

    # -----------------------------------------------------

    def reset_showdown(self):
        """
        Clear showdown-specific information.
        """

        self.is_winner = False
        self.chips_won = 0
        self.split_pot = False

    # =====================================================
    # Information
    # =====================================================

    @property
    def lost(self) -> bool:

        return not self.is_winner

    # -----------------------------------------------------

    @property
    def has_ai_analysis(self) -> bool:

        return (
            self.win_probability is not None
            and self.hand_strength is not None
        )

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
                f"Win Probability : {self.win_probability:.2%}"
            )

        if self.hand_strength is not None:
            text.append(
                f"Hand Strength : {self.hand_strength:.3f}"
            )

        if self.confidence is not None:
            text.append(
                f"Confidence : {self.confidence:.2%}"
            )

        if self.is_winner:
            text.append(
                f"Winner (+{self.chips_won} chips)"
            )

        return "\n".join(text)