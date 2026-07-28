import random

from models.card import Card, Suit, Rank



class Deck:
    """
    Represents a standard 52-card poker deck.

    Responsibilities
    ----------------
    • Create cards
    • Shuffle
    • Deal cards
    • Burn cards
    • Support Monte Carlo simulation
    """



    def __init__(self):

        self.cards: list[Card] = []

        self.reset()



    # =====================================================
    # Deck Management
    # =====================================================

    def reset(self):
        """
        Create fresh 52-card deck.
        """

        self.cards = [

            Card(

                suit,

                rank

            )

            for suit in Suit

            for rank in Rank

        ]



    # -----------------------------------------------------

    def shuffle(
        self,
        seed=None
    ):
        """
        Shuffle deck.

        Seed supported for testing.
        """

        if seed is not None:

            rng = random.Random(seed)

            rng.shuffle(

                self.cards

            )

        else:

            random.shuffle(

                self.cards

            )



    # =====================================================
    # Card Operations
    # =====================================================

    def deal(self) -> Card:
        """
        Deal one card.
        """

        if self.is_empty():

            raise RuntimeError(
                "Cannot deal from empty deck."
            )


        return self.cards.pop()



    # -----------------------------------------------------

    def deal_many(
        self,
        count: int
    ) -> list[Card]:
        """
        Deal multiple cards.
        """

        if count < 0:

            raise ValueError(
                "Count cannot be negative."
            )


        if count > len(self.cards):

            raise RuntimeError(
                "Not enough cards."
            )


        return [

            self.deal()

            for _ in range(count)

        ]



    # -----------------------------------------------------

    def burn(self):
        """
        Remove one card without returning.
        """

        self.deal()



    # -----------------------------------------------------

    def remove_cards(
        self,
        cards: list[Card]
    ):
        """
        Remove known cards.

        Used by:
        • Monte Carlo
        • AI simulation
        """

        for card in cards:

            if card in self.cards:

                self.cards.remove(card)



    # -----------------------------------------------------

    def contains(
        self,
        card: Card
    ) -> bool:

        return card in self.cards
        # =====================================================
    # Simulation Helpers
    # =====================================================

    def copy(self):
        """
        Create independent deck copy.

        Used by:
        - Monte Carlo
        - AI simulations
        """

        new_deck = object.__new__(Deck)

        new_deck.cards = self.cards.copy()

        return new_deck



    # -----------------------------------------------------

    def clone(self):
        """
        Alias for copy().
        """

        return self.copy()



    # -----------------------------------------------------

    def random_cards(
        self,
        count: int
    ) -> list[Card]:
        """
        Return random cards without
        modifying original deck.

        Used for simulations.
        """

        if count < 0:

            raise ValueError(
                "Count cannot be negative."
            )


        if count > len(self.cards):

            raise RuntimeError(
                "Not enough cards available."
            )


        return random.sample(

            self.cards,

            count

        )



    # -----------------------------------------------------

    def remaining_cards(self) -> list[Card]:
        """
        Return copy of remaining cards.
        """

        return self.cards.copy()



    # =====================================================
    # Information
    # =====================================================

    def cards_remaining(self) -> int:

        return len(

            self.cards

        )



    # -----------------------------------------------------

    def is_empty(self) -> bool:

        return (

            len(self.cards)

            ==

            0

        )



    # -----------------------------------------------------

    def __len__(self):

        return len(

            self.cards

        )



    # -----------------------------------------------------

    def __iter__(self):

        return iter(

            self.cards

        )



    # =====================================================
    # Debug
    # =====================================================

    def __repr__(self):

        return (

            f"Deck("

            f"{len(self.cards)} cards)"

        )



    # -----------------------------------------------------

    def __str__(self):

        return (

            "========== DECK ==========\n"

            f"Cards Remaining : {len(self.cards)}"

        )