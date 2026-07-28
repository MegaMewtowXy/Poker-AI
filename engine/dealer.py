from models.card import Card
from models.deck import Deck
from models.player import Player
from models.player_position import PlayerPosition
from models.table import Table


# ==========================================================
# Position Layouts
# ==========================================================

POSITION_LAYOUTS = {

    2: [

        PlayerPosition.BUTTON,
        PlayerPosition.BIG_BLIND

    ],

    3: [

        PlayerPosition.BUTTON,
        PlayerPosition.SMALL_BLIND,
        PlayerPosition.BIG_BLIND

    ],

    4: [

        PlayerPosition.BUTTON,
        PlayerPosition.SMALL_BLIND,
        PlayerPosition.BIG_BLIND,
        PlayerPosition.UNDER_THE_GUN

    ],

    5: [

        PlayerPosition.BUTTON,
        PlayerPosition.SMALL_BLIND,
        PlayerPosition.BIG_BLIND,
        PlayerPosition.UNDER_THE_GUN,
        PlayerPosition.CUTOFF

    ],

    6: [

        PlayerPosition.BUTTON,
        PlayerPosition.SMALL_BLIND,
        PlayerPosition.BIG_BLIND,
        PlayerPosition.UNDER_THE_GUN,
        PlayerPosition.HIJACK,
        PlayerPosition.CUTOFF

    ],

    7: [

        PlayerPosition.BUTTON,
        PlayerPosition.SMALL_BLIND,
        PlayerPosition.BIG_BLIND,
        PlayerPosition.UNDER_THE_GUN,
        PlayerPosition.MIDDLE_POSITION,
        PlayerPosition.HIJACK,
        PlayerPosition.CUTOFF

    ],

    8: [

        PlayerPosition.BUTTON,
        PlayerPosition.SMALL_BLIND,
        PlayerPosition.BIG_BLIND,
        PlayerPosition.UNDER_THE_GUN,
        PlayerPosition.UNDER_THE_GUN_PLUS_ONE,
        PlayerPosition.MIDDLE_POSITION,
        PlayerPosition.HIJACK,
        PlayerPosition.CUTOFF

    ],

    9: [

        PlayerPosition.BUTTON,
        PlayerPosition.SMALL_BLIND,
        PlayerPosition.BIG_BLIND,
        PlayerPosition.UNDER_THE_GUN,
        PlayerPosition.UNDER_THE_GUN_PLUS_ONE,
        PlayerPosition.MIDDLE_POSITION,
        PlayerPosition.MIDDLE_POSITION_PLUS_ONE,
        PlayerPosition.HIJACK,
        PlayerPosition.CUTOFF

    ]

}


class Dealer:
    """
    Represents the dealer.

    Responsibilities
    ----------------
    • Owns the deck
    • Shuffles cards
    • Deals hole cards
    • Burns cards
    • Deals community cards
    • Rotates dealer button
    • Assigns player positions
    """

    def __init__(
        self,
        deck: Deck
    ):

        self.deck = deck

    # ==================================================
    # Deck Management
    # ==================================================

    def start_new_hand(self):
        """
        Reset and shuffle the deck.
        """

        self.deck.reset()

        self.deck.shuffle()

    # --------------------------------------------------

    def reset_deck(self):

        self.start_new_hand()

    # --------------------------------------------------

    def shuffle(self):

        self.deck.shuffle()

    # --------------------------------------------------

    def cards_remaining(self) -> int:

        return self.deck.cards_remaining()

    # --------------------------------------------------

    def deck_empty(self) -> bool:

        return self.cards_remaining() == 0

    # ==================================================
    # Hole Cards
    # ==================================================

    def deal_hole_cards(
        self,
        players: list[Player]
    ):
        """
        Deal two cards to every active player.
        """

        for player in players:

            player.clear_hand()

        for _ in range(2):

            for player in players:

                if player.eliminated:
                    continue

                player.receive_card(
                    self.deck.deal()
                )

    # ==================================================
    # Burn Card
    # ==================================================

    def burn_card(self) -> Card:
        """
        Burn one card.

        Returns the burned card.
        """

        return self.deck.deal()

    # ==================================================
    # Community Cards
    # ==================================================

    def deal_flop(
        self,
        table: Table
    ):

        self.burn_card()

        for _ in range(3):

            table.add_community_card(
                self.deck.deal()
            )

    # --------------------------------------------------

    def deal_turn(
        self,
        table: Table
    ):

        self.burn_card()

        table.add_community_card(
            self.deck.deal()
        )

    # --------------------------------------------------

    def deal_river(
        self,
        table: Table
    ):

        self.burn_card()

        table.add_community_card(
            self.deck.deal()
        )
        # ==================================================
    # Dealer Button
    # ==================================================

    def rotate_dealer(
        self,
        table: Table,
        total_players: int
    ):
        """
        Move the dealer button clockwise.
        """

        if total_players < 2:

            raise ValueError(
                "Need at least two players."
            )

        table.rotate_dealer(
            total_players
        )

    # ==================================================
    # Player Positions
    # ==================================================

    def assign_positions(
        self,
        players: list[Player],
        table: Table
    ):
        """
        Assign poker positions based on the
        dealer button.

        Supports 2–9 active players.
        """

        active_players = [

            player

            for player in players

            if not player.eliminated

        ]

        total = len(active_players)

        if total < 2:

            raise ValueError(
                "At least two active players are required."
            )

        if total not in POSITION_LAYOUTS:

            raise ValueError(
                f"Unsupported player count: {total}"
            )

        # ------------------------------------------
        # Reset Positions
        # ------------------------------------------

        for player in active_players:

            player.set_position(
                PlayerPosition.UNKNOWN
            )

        # ------------------------------------------
        # Seating Order
        # ------------------------------------------

        dealer = (
            table.dealer_position % total
        )

        order = [

            active_players[
                (dealer + i) % total
            ]

            for i in range(total)

        ]

        # ------------------------------------------
        # Assign Positions
        # ------------------------------------------

        positions = POSITION_LAYOUTS[total]

        for player, position in zip(
            order,
            positions
        ):

            player.set_position(
                position
            )

    # ==================================================
    # Utility
    # ==================================================

    def remaining_cards(self) -> int:
        """
        Alias for cards_remaining().
        """

        return self.cards_remaining()

    # --------------------------------------------------

    def can_deal(
        self,
        cards_needed: int
    ) -> bool:
        """
        Returns True if enough cards remain.
        """

        return (
            self.cards_remaining()
            >= cards_needed
        )

    # ==================================================
    # Debug
    # ==================================================

    def __repr__(self):

        return (

            "Dealer("

            f"remaining_cards="

            f"{self.cards_remaining()}"

            ")"

        )

    # --------------------------------------------------

    def __str__(self):

        return (

            "========== DEALER ==========\n"

            f"Cards Remaining : "

            f"{self.cards_remaining()}"

        )