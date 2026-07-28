from models.card import Card
from models.hand_result import HandResult

from engine.evaluator import HandEvaluator
from engine.probability import Probability


class HandStrength:
    """
    Calculates poker hand strength for AI decisions.

    Responsibilities
    ----------------
    • Evaluate current hand
    • Convert hand category into strength score
    • Detect basic draws
    • Provide AI-readable information

    This class does NOT:
        • Make betting decisions
        • Control strategy
        • Modify game state
    """


    def __init__(self):

        self.evaluator = HandEvaluator()

        self.probability = Probability()


    # ==================================================
    # Hand Evaluation
    # ==================================================

    def evaluate_hand(
        self,
        hole_cards: list[Card],
        community_cards: list[Card]
    ) -> HandResult:
        """
        Evaluate current poker hand.
        """

        return self.evaluator.evaluate(

            hole_cards,

            community_cards

        )


    # ==================================================
    # Strength Score
    # ==================================================

    def strength_score(
        self,
        result: HandResult
    ) -> int:
        """
        Convert hand category into
        AI strength score.

        Range:
            0 - 100
        """

        scores = {

            "Royal Flush": 100,

            "Straight Flush": 95,

            "Four of a Kind": 90,

            "Full House": 85,

            "Flush": 75,

            "Straight": 70,

            "Three of a Kind": 60,

            "Two Pair": 50,

            "Pair": 35,

            "High Card": 15

        }


        return scores.get(

            result.hand_name,

            0

        )
        # ==================================================
    # Draw Detection
    # ==================================================

    def flush_draw(
        self,
        hole_cards: list[Card],
        community_cards: list[Card]
    ) -> bool:
        """
        Detect if player has a flush draw.

        A flush draw means:
        4 cards of the same suit.
        """

        cards = (

            hole_cards

            +

            community_cards

        )

        suits = {}

        for card in cards:

            suits[card.suit] = (

                suits.get(
                    card.suit,
                    0
                )

                + 1

            )


        return any(

            count == 4

            for count in suits.values()

        )


    # --------------------------------------------------

    def straight_draw(
        self,
        hole_cards: list[Card],
        community_cards: list[Card]
    ) -> bool:
        """
        Basic straight draw detection.

        Detects if five-card straight
        can potentially be completed.
        """

        cards = (

            hole_cards

            +

            community_cards

        )


        ranks = [

            card.rank.value

            for card in cards

        ]


        ranks = sorted(

            set(ranks)

        )


        for i in range(
            len(ranks)
        ):

            window = ranks[i:i+4]


            if len(window) == 4:

                if (

                    window[-1]

                    -

                    window[0]

                    == 3

                ):

                    return True


        return False


    # ==================================================
    # Draw Information
    # ==================================================

    def draw_strength(
        self,
        hole_cards: list[Card],
        community_cards: list[Card]
    ) -> int:
        """
        Calculate draw value.

        Range:
        0 - 20
        """

        strength = 0


        if self.flush_draw(

            hole_cards,

            community_cards

        ):

            strength += 10


        if self.straight_draw(

            hole_cards,

            community_cards

        ):

            strength += 10


        return strength
        # ==================================================
    # Situation Modifiers
    # ==================================================

    def opponent_modifier(
        self,
        opponent_count: int
    ) -> int:
        """
        Adjust strength based on number
        of opponents.

        More opponents = weaker relative strength.
        """

        if opponent_count <= 1:

            return 10


        if opponent_count <= 3:

            return 0


        if opponent_count <= 5:

            return -10


        return -20


    # --------------------------------------------------

    def position_modifier(
        self,
        position
    ) -> int:
        """
        Position advantage.

        Later positions have more information.
        """

        position_name = str(
            position
        ).upper()


        if "BUTTON" in position_name:

            return 10


        if "CUTOFF" in position_name:

            return 8


        if "HIJACK" in position_name:

            return 5


        if "BIG_BLIND" in position_name:

            return -5


        if "SMALL_BLIND" in position_name:

            return -3


        return 0


    # --------------------------------------------------

    def board_danger(
        self,
        community_cards: list[Card]
    ) -> int:
        """
        Detect dangerous boards.

        Wet boards:
        - Flush possibilities
        - Straight possibilities

        Returns penalty.
        """

        danger = 0


        suits = {}

        ranks = []


        for card in community_cards:

            suits[card.suit] = (

                suits.get(
                    card.suit,
                    0
                )

                + 1

            )

            ranks.append(
                card.rank.value
            )


        # Flush danger

        if any(

            count >= 3

            for count in suits.values()

        ):

            danger += 10


        # Straight danger

        ranks = sorted(
            set(ranks)
        )


        if len(ranks) >= 3:

            danger += 5


        return -danger


    # ==================================================
    # Adjusted Strength
    # ==================================================

    def adjusted_strength(
        self,
        base_strength: int,
        draw_strength: int,
        opponent_count: int,
        position=None,
        community_cards=None
    ) -> int:
        """
        Final AI strength score.

        Range:
        0 - 100
        """

        score = (

            base_strength

            +

            draw_strength

        )


        score += self.opponent_modifier(

            opponent_count

        )


        if position:

            score += self.position_modifier(

                position

            )


        if community_cards:

            score += self.board_danger(

                community_cards

            )


        return max(

            0,

            min(

                100,

                score

            )

        )
        # ==================================================
    # Complete Hand Analysis
    # ==================================================

    def analyze_hand(
        self,
        hole_cards: list[Card],
        community_cards: list[Card],
        opponent_count: int,
        position=None
    ) -> dict:
        """
        Generate complete AI hand profile.

        Used by Decision Engine.
        """


        result = self.evaluate_hand(

            hole_cards,

            community_cards

        )


        base_strength = self.strength_score(

            result

        )


        draw_value = self.draw_strength(

            hole_cards,

            community_cards

        )


        final_strength = self.adjusted_strength(

            base_strength,

            draw_value,

            opponent_count,

            position,

            community_cards

        )


        draws = []


        if self.flush_draw(

            hole_cards,

            community_cards

        ):

            draws.append(
                "Flush Draw"
            )


        if self.straight_draw(

            hole_cards,

            community_cards

        ):

            draws.append(
                "Straight Draw"
            )


        return {

            "hand_name":

                result.hand_name,


            "base_strength":

                base_strength,


            "draw_strength":

                draw_value,


            "final_strength":

                final_strength,


            "draws":

                draws,


            "score":

                result.score

        }


    # ==================================================
    # Debug
    # ==================================================

    def __repr__(self):

        return "HandStrength()"


    # --------------------------------------------------

    def __str__(self):

        return (

            "========== HAND STRENGTH ==========\n"

            "AI Hand Evaluation System"

        )