from models.card import Card
from models.hand_result import HandResult
from models.player_position import PlayerPosition
from models.player_role import PlayerRole
from engine.evaluator import HandEvaluator



class HandStrength:
    """
    Final AI hand strength analyzer.

    Responsibilities
    ----------------
    • Evaluate current hand
    • Calculate hand category strength
    • Detect draws
    • Apply modifiers
    • Generate AI-readable analysis

    Does NOT:
        • Calculate equity
        • Calculate pot odds
        • Make decisions
        • Control betting
    """



    def __init__(self):

        self.evaluator = HandEvaluator()



    # ==========================================
    # Hand Evaluation
    # ==========================================

    
    def evaluate_hand(
        self,
        hole_cards: list[Card],
        community_cards: list[Card]
    ) -> HandResult:
        """
        Evaluate current poker hand.

        Treys requires at least 5 total cards.
        Pre-flop returns a temporary High Card result.
        """

        total_cards = len(hole_cards) + len(community_cards)

        if total_cards < 5:

            return HandResult(
                score=7462,
                rank=9,
                hand_name="High Card"
            )

        return self.evaluator.evaluate(
            hole_cards,
            community_cards
        )


    # ==========================================
    # Base Strength
    # ==========================================

    def strength_score(
        self,
        result: HandResult
    ) -> int:
        """
        Convert hand category into
        base AI strength.

        Range:
        0 - 100
        """

        scores = {

            "Royal Flush": 100,

            "Straight Flush": 95,

            "Four of a Kind": 92,

            "Full House": 88,

            "Flush": 78,

            "Straight": 72,

            "Three of a Kind": 62,

            "Two Pair": 52,

            "Pair": 35,

            "High Card": 15

        }


        return scores.get(

            result.hand_name,

            0

        )



    # ==========================================
    # Category Modifier
    # ==========================================

    def category_modifier(
        self,
        hand_name: str
    ) -> int:
        """
        Adjustment based on hand category.
        """

        modifiers = {

            "Royal Flush": 0,

            "Straight Flush": 0,

            "Four of a Kind": 5,

            "Full House": 5,

            "Flush": 3,

            "Straight": 2,

            "Three of a Kind": 3,

            "Two Pair": 2,

            "Pair": 0,

            "High Card": -5

        }


        return modifiers.get(

            hand_name,

            0

        )



    # ==========================================
    # Card Helper
    # ==========================================

    @staticmethod
    def all_cards(
        hole_cards,
        community_cards
    ):
        """
        Combine player cards
        and community cards.
        """

        return (

            hole_cards

            +

            community_cards

        )



    # ==========================================
    # Flush Draw
    # ==========================================

    def flush_draw(
    self,
    hole_cards,
    community_cards
):
        """
        Detect four cards of same suit.

        Returns False if flush
        is already completed.
        """

        if len(community_cards) >= 3:

            result = self.evaluate_hand(
                hole_cards,
                community_cards
            )

            if result.hand_name == "Flush":

                return False

        cards = self.all_cards(
            hole_cards,
            community_cards
        )

        suits = {}

        for card in cards:

            suits[card.suit] = (
                suits.get(card.suit, 0) + 1
            )

        return any(
            count == 4
            for count in suits.values()
        )


    # ==========================================
    # Straight Sequences
    # ==========================================

    @staticmethod
    def straight_sequences():
        """
        Possible straight combinations.
        """

        return [

            [14,2,3,4,5],

            [2,3,4,5,6],

            [3,4,5,6,7],

            [4,5,6,7,8],

            [5,6,7,8,9],

            [6,7,8,9,10],

            [7,8,9,10,11],

            [8,9,10,11,12],

            [9,10,11,12,13],

            [10,11,12,13,14]

        ]



    # ==========================================
    # Straight Draw
    # ==========================================

    def straight_draw(
    self,
    hole_cards,
    community_cards
):
        """
        Detect open-ended straight draw.

        Returns False if straight
        already exists.
        """

        if len(community_cards) >= 3:

            result = self.evaluate_hand(
                hole_cards,
                community_cards
            )

            if result.hand_name == "Straight":

                return False

        cards = self.all_cards(
            hole_cards,
            community_cards
        )

        ranks = set(
            card.rank.strength
            for card in cards
        )

        for sequence in self.straight_sequences():

            missing = len(
                set(sequence) - ranks
            )

            if missing == 1:

                return True

        return False    
    # ==========================================
    # Gutshot Draw
    # ==========================================

    def gutshot_draw(
    self,
    hole_cards,
    community_cards
):
        """
        Detect inside straight draw.

        Returns False if straight
        already exists.
        """

        if len(community_cards) >= 3:

            result = self.evaluate_hand(
                hole_cards,
                community_cards
            )

            if result.hand_name == "Straight":

                return False

        cards = self.all_cards(
            hole_cards,
            community_cards
        )

        ranks = set(
            card.rank.strength
            for card in cards
        )

        for sequence in self.straight_sequences():

            missing = set(sequence) - ranks

            if len(missing) == 1:

                ordered = sorted(sequence)

                gaps = 0

                for i in range(len(ordered) - 1):

                    if ordered[i + 1] - ordered[i] > 1:

                        gaps += 1

                if gaps == 1:

                    return True

        return False


    # ==========================================
    # Backdoor Draw
    # ==========================================

    def backdoor_draw(
        self,
        hole_cards,
        community_cards
    ):
        """
        Detect runner-runner possibilities.
        """

        cards = self.all_cards(

            hole_cards,

            community_cards

        )


        suits = {}



        for card in cards:

            suits[card.suit] = (

                suits.get(

                    card.suit,

                    0

                )

                +

                1

            )



        return any(

            count == 3

            for count in suits.values()

        )



    # ==========================================
    # Draw Strength
    # ==========================================

    def draw_strength(
        self,
        hole_cards,
        community_cards
    ):
        """
        Calculate draw value.

        Range:
        0 - 25
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



        elif self.gutshot_draw(

            hole_cards,

            community_cards

        ):

            strength += 5



        if self.backdoor_draw(

            hole_cards,

            community_cards

        ):

            strength += 2



        return min(

            strength,

            25

        )



    # ==========================================
    # Pair Quality
    # ==========================================

    def pair_quality(
        self,
        hole_cards,
        community_cards
    ):
        """
        Evaluate one-pair quality.

        Range:
        0 - 15
        """

        if len(community_cards) == 0:

            return 0

        result = self.evaluate_hand(
            hole_cards,
            community_cards
        )

        if result.hand_name != "Pair":

            return 0

        board_ranks = [
            card.rank.strength
            for card in community_cards
        ]

        if not board_ranks:

            return 0

        highest_board = max(board_ranks)

        bonus = 0

        for card in hole_cards:

            if card.rank.strength == highest_board:

                bonus += 15

            elif card.rank.strength in board_ranks:

                bonus += 5

        return min(
            bonus,
            15
        )


    # ==========================================
    # Kicker Strength
    # ==========================================

    def kicker_strength(
        self,
        hole_cards
    ):
        """
        Evaluate hole-card kicker.

        Range:
        0 - 8
        """

        if not hole_cards:

            return 0



        ranks = sorted(

            [

                card.rank.strength

                for card in hole_cards

            ],

            reverse=True

        )


        highest = ranks[0]



        if highest == 14:

            return 8



        if highest >= 13:

            return 6



        if highest >= 11:

            return 4



        if highest >= 9:

            return 2



        return 0



    # ==========================================
    # Nuts Detection
    # ==========================================

    def nuts_bonus(
    self,
    hole_cards,
    community_cards
):
        """
        Detect extremely strong holdings.

        Range:
        0 - 15
        """

        if len(community_cards) < 3:

            return 0

        result = self.evaluate_hand(
            hole_cards,
            community_cards
        )

        if result.hand_name in [
            "Royal Flush",
            "Straight Flush"
        ]:

            return 15

        if result.hand_name == "Four of a Kind":

            return 15

        if result.hand_name == "Full House":

            return 10

        if result.hand_name == "Flush":

            for card in hole_cards:

                if card.rank.strength == 14:

                    return 8

        return 0
    # ==========================================
    # Board Danger
    # ==========================================

    def board_danger(
        self,
        community_cards
    ):
        """
        Detect dangerous boards.

        Returns penalty.

        Range:
        0 to -20
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

                +

                1

            )


            ranks.append(

                card.rank.strength

            )



        # Flush possibilities

        if any(

            count >= 3

            for count in suits.values()

        ):

            danger += 10



        # Straight possibilities

        ranks = sorted(

            set(ranks)

        )



        for i in range(

            len(ranks) - 2

        ):


            if (

                ranks[i + 2]

                -

                ranks[i]

            ) <= 4:

                danger += 5

                break



        return -min(

            danger,

            20

        )
        # ==========================================
    # Position Modifier
    # ==========================================

    def position_modifier(
    self,
    position: PlayerPosition | None,
    roles: set[PlayerRole] | None = None
):
        """
        Later positions have more information
        and can play wider ranges.

        Range:
        -8 to +10
        """

        bonus = 0

        if position is None:
            return 0

        if position == PlayerPosition.BUTTON:
            bonus += 10

        elif position == PlayerPosition.CUTOFF:
            bonus += 8

        elif position == PlayerPosition.HIJACK:
            bonus += 5

        elif position == PlayerPosition.BIG_BLIND:
            bonus -= 5

        if roles and PlayerRole.SMALL_BLIND in roles:
            bonus -= 3

        return bonus



    # ==========================================
    # Opponent Modifier
    # ==========================================

    def opponent_modifier(
        self,
        opponent_count: int
    ):
        """
        Adjust strength depending on
        number of opponents.

        More opponents:
        harder to win.

        Range:
        -20 to +10
        """

        if opponent_count <= 1:

            return 10



        if opponent_count <= 3:

            return 0



        if opponent_count <= 5:

            return -10



        return -20



    # ==========================================
    # Final Strength Calculation
    # ==========================================

    def calculate_final_strength(
        self,
        base_strength,
        category_bonus,
        draw_strength,
        pair_bonus,
        kicker_bonus,
        nuts_bonus,
        position_bonus,
        opponent_bonus,
        board_penalty
    ):
        """
        Combine all hand factors.

        Range:
        0 - 100
        """

        score = (

            base_strength

            +

            category_bonus

            +

            draw_strength

            +

            pair_bonus

            +

            kicker_bonus

            +

            nuts_bonus

            +

            position_bonus

            +

            opponent_bonus

            +

            board_penalty

        )


        return max(

            0,

            min(

                100,

                score

            )

        )



    # ==========================================
    # Complete Hand Analysis
    # ==========================================

    def analyze_hand(
        self,
        hole_cards,
        community_cards,
        opponent_count,
        position=None,
        roles=None,
        equity=None
    ):
        """
        Generate complete AI hand profile.

        Equity is supplied externally.

        This method does not make decisions.
        """

        result = self.evaluate_hand(

            hole_cards,

            community_cards

        )



        base_strength = self.strength_score(

            result

        )



        category_bonus = self.category_modifier(

            result.hand_name

        )



        draw_value = self.draw_strength(

            hole_cards,

            community_cards

        )



        pair_bonus = self.pair_quality(

            hole_cards,

            community_cards

        )



        kicker_bonus = self.kicker_strength(

            hole_cards

        )



        nuts_bonus = self.nuts_bonus(

            hole_cards,

            community_cards

        )



        position_bonus = self.position_modifier(

            position,
            roles

        )



        opponent_bonus = self.opponent_modifier(

            opponent_count

        )



        board_penalty = self.board_danger(

            community_cards

        )



        final_strength = self.calculate_final_strength(

            base_strength,

            category_bonus,

            draw_value,

            pair_bonus,

            kicker_bonus,

            nuts_bonus,

            position_bonus,

            opponent_bonus,

            board_penalty

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



        elif self.gutshot_draw(

            hole_cards,

            community_cards

        ):

            draws.append(

                "Gutshot"

            )



        if self.backdoor_draw(

            hole_cards,

            community_cards

        ):

            draws.append(

                "Backdoor Draw"

            )



        return {

            "hand_name":

                result.hand_name,


            "base_strength":

                base_strength,


            "category_bonus":

                category_bonus,


            "draw_strength":

                draw_value,


            "pair_bonus":

                pair_bonus,


            "kicker_bonus":

                kicker_bonus,


            "nuts_bonus":

                nuts_bonus,


            "equity":

                equity,


            "final_strength":

                final_strength,


            "draws":

                draws,


            "score":

                result.score

        }



    # ==========================================
    # Debug
    # ==========================================

    def __repr__(self):

        return "HandStrength()"



    def __str__(self):

        return (

            "========== HAND STRENGTH ==========\n"

            "AI Hand Analysis Engine"

        )