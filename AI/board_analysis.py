from models.card import Suit, Rank

class BoardAnalyzer:
    """
    Analyzes poker board texture.

    Responsibilities
    ----------------
    • Detect flush possibilities
    • Detect straight possibilities
    • Detect paired boards
    • Analyze board wetness
    • Estimate board danger

    Does NOT
    --------
    • Make betting decisions
    • Decide bluffs
    • Control strategy
    """

    def analyze(
        self,
        community_cards
    ):
        """
        Analyze complete community cards.

        Returns:

        {
            texture,
            flush_possible,
            straight_possible,
            paired_board,
            danger_level,
            high_card,
            connectedness,
            monotone,
            rainbow
        }
        """

        if community_cards is None:
            community_cards = []

        if len(community_cards) > 5:
            raise ValueError("A Hold'em board cannot contain more than five cards.")

        if len(set(community_cards)) != len(community_cards):
            raise ValueError("Community cards cannot contain duplicates.")

        result = {

            "texture":

                "dry",

            "flush_possible":

                False,

            "straight_possible":

                False,

            "paired_board":

                False,

            "danger_level":

                0,

            "high_card":

                None,

            "connectedness":

                0,

            "monotone":

                False,

            "rainbow":

                False

        }

        # ==================================
        # Not enough cards
        # ==================================

        if len(community_cards) < 3:

            return result

        # ==================================
        # Flush Detection
        # ==================================

        suit_counts = {}

        for card in community_cards:

            suit_counts[card.suit] = (

                suit_counts.get(

                    card.suit,

                    0

                )

                +

                1

            )

        max_suit_count = max(

            suit_counts.values()

        )

        if max_suit_count >= 3:

            result["flush_possible"] = True

        if max_suit_count == len(community_cards):

            result["monotone"] = True

        elif len(suit_counts) == len(community_cards):

            result["rainbow"] = True

        # ==================================
        # Pair Detection
        # ==================================

        rank_counts = {}

        for card in community_cards:

            rank_counts[card.rank] = (

                rank_counts.get(

                    card.rank,

                    0

                )

                +

                1

            )

        for count in rank_counts.values():

            if count >= 2:

                result["paired_board"] = True

                break

        # ==================================
        # High Card
        # ==================================

        result["high_card"] = max(

            [

                card.rank.strength

                for card in community_cards

            ]

        )

        # ==================================
        # Straight Detection
        # ==================================

        values = sorted(

            set(

                [

                    card.rank.strength

                    for card in community_cards

                ]

            )

        )

        # An ace may also be used as the low end of A-2-3-4-5.
        straight_values = values.copy()
        if 14 in straight_values:
            straight_values.insert(0, 1)

        connected = 0

        for i in range(

            len(values) - 1

        ):

            difference = (

                values[i + 1]

                -

                values[i]

            )

            if difference <= 2:

                connected += 1

        result["connectedness"] = connected

        for i in range(

            len(straight_values) - 2

        ):

            if (

                straight_values[i + 2]

                -

                straight_values[i]

                <= 4

            ):

                result["straight_possible"] = True

                break
                # ==================================
        # Danger Calculation
        # ==================================

        danger = 0

        if result["flush_possible"]:

            danger += 2

        if result["straight_possible"]:

            danger += 2

        if result["paired_board"]:

            danger += 1

        if result["monotone"]:

            danger += 2

        if result["connectedness"] >= 2:

            danger += 1

        result["danger_level"] = min(

            danger,

            10

        )

        # ==================================
        # Texture Classification
        # ==================================

        if result["danger_level"] >= 4:

            result["texture"] = "wet"

        elif result["danger_level"] >= 2:

            result["texture"] = "semi_wet"

        else:

            result["texture"] = "dry"

        return result

    # ==================================
    # Flush Analysis
    # ==================================

    def flush_analysis(
        self,
        community_cards
    ):
        """
        Detailed flush information.
        """

        suits = {}

        for card in community_cards:

            suits[card.suit] = (

                suits.get(

                    card.suit,

                    0

                )

                +

                1

            )

        highest = max(

            suits.values(),

            default=0

        )

        return {

            "flush_possible":

                highest >= 3,

            "cards_same_suit":

                highest,

            "flush_draw":

                highest == 4,

            "monotone":

                highest == len(community_cards)

        }

    # ==================================
    # Straight Analysis
    # ==================================

    def straight_analysis(
        self,
        community_cards
    ):
        """
        Detailed straight information.
        """

        values = sorted(

            set(

                [

                    card.rank.strength

                    for card in community_cards

                ]

            )

        )

        connected = 0

        for i in range(

            len(values)-1

        ):

            if (

                values[i+1]

                -

                values[i]

                <= 2

            ):

                connected += 1

        return {

            "straight_possible":

                connected >= 2,

            "connectedness":

                connected,

            "straight_draw":

                connected >= 3

        }

    # ==================================
    # Board Strength
    # ==================================

    def board_strength(
        self,
        community_cards
    ):
        """
        Estimate board danger.

        Range:
        0 - 10
        """

        analysis = self.analyze(

            community_cards

        )

        strength = (

            analysis["danger_level"]

        )

        return min(

            strength,

            10

        )

    # ==================================
    # Dangerous Board Check
    # ==================================

    def is_dangerous(
        self,
        community_cards
    ):
        """
        Returns whether board is dangerous.
        """

        return (

            self.board_strength(

                community_cards

            )

            >=

            5

        )

    # ==================================
    # Profile
    # ==================================

    def profile(
        self,
        community_cards
    ):
        """
        Complete board profile.
        """

        return self.analyze(

            community_cards

        )

    # ==================================
    # Debug
    # ==================================

    def __repr__(self):

        return (

            "BoardAnalyzer()"

        )

    def __str__(self):

        return (

            "Texas Hold'em "

            "Board Texture Analyzer"

        )
