from models.card import Card
from models.deck import Deck
from models.player import Player
from models.player_position import PlayerPosition
from models.player_role import PlayerRole
from models.table import Table
from models.street import Street

# ==========================================================
# Position Layouts
# ==========================================================

POSITION_LAYOUTS = {

    # ==========================================
    # Heads Up
    #
    # Button player:
    #   Position -> BUTTON
    #   Role -> DEALER + SMALL_BLIND
    #
    # Other player:
    #   Position -> BIG_BLIND
    #   Role -> BIG_BLIND
    # ==========================================

    2: [

        PlayerPosition.BUTTON,

        PlayerPosition.BIG_BLIND

    ],

    3: [

        PlayerPosition.BUTTON,

        PlayerPosition.BIG_BLIND,

        PlayerPosition.CUTOFF

    ],

    4: [

        PlayerPosition.BUTTON,

        PlayerPosition.BIG_BLIND,

        PlayerPosition.CUTOFF,

        PlayerPosition.UNDER_THE_GUN

    ],

    5: [

        PlayerPosition.BUTTON,

        PlayerPosition.BIG_BLIND,

        PlayerPosition.CUTOFF,

        PlayerPosition.HIJACK,

        PlayerPosition.UNDER_THE_GUN

    ],

    6: [

        PlayerPosition.BUTTON,

        PlayerPosition.BIG_BLIND,

        PlayerPosition.CUTOFF,

        PlayerPosition.HIJACK,

        PlayerPosition.MIDDLE_POSITION,

        PlayerPosition.UNDER_THE_GUN

    ],

    7: [

        PlayerPosition.BUTTON,

        PlayerPosition.BIG_BLIND,

        PlayerPosition.CUTOFF,

        PlayerPosition.HIJACK,

        PlayerPosition.MIDDLE_POSITION,

        PlayerPosition.UNDER_THE_GUN_PLUS_ONE,

        PlayerPosition.UNDER_THE_GUN

    ],

    8: [

        PlayerPosition.BUTTON,

        PlayerPosition.BIG_BLIND,

        PlayerPosition.CUTOFF,

        PlayerPosition.HIJACK,

        PlayerPosition.MIDDLE_POSITION,

        PlayerPosition.MIDDLE_POSITION_PLUS_ONE,

        PlayerPosition.UNDER_THE_GUN_PLUS_ONE,

        PlayerPosition.UNDER_THE_GUN

    ],

    9: [

        PlayerPosition.BUTTON,

        PlayerPosition.BIG_BLIND,

        PlayerPosition.CUTOFF,

        PlayerPosition.HIJACK,

        PlayerPosition.MIDDLE_POSITION,

        PlayerPosition.MIDDLE_POSITION_PLUS_ONE,

        PlayerPosition.UNDER_THE_GUN_PLUS_ONE,

        PlayerPosition.UNDER_THE_GUN,

        PlayerPosition.UNKNOWN

    ]

}

class Dealer:
    """
    Represents poker dealer.

    Responsibilities:

    - Own deck
    - Shuffle cards
    - Deal hole cards
    - Burn cards
    - Deal community cards
    - Rotate dealer button
    - Assign positions
    - Assign temporary roles

    Does NOT handle:

    - Betting
    - Pots
    - Winners
    """

    def __init__(
        self,
        deck: Deck
    ):

        if deck is None:

            raise ValueError(
                "Dealer requires a deck."
            )

        self.deck = deck

    # ==================================================
    # Deck Management
    # ==================================================

    def start_new_hand(self):
        """
        Reset and shuffle deck.
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

        return (

            self.cards_remaining() == 0

        )

    # --------------------------------------------------

    def can_deal(
        self,
        cards_needed: int = 1
    ) -> bool:

        return (

            self.cards_remaining()

            >=

            cards_needed

        )
        # ==================================================
    # Hole Cards
    # ==================================================

    def deal_hole_cards(
        self,
        players: list[Player]
    ):
        """
        Deal two hole cards to every active player.

        Texas Hold'em:
        One card per player,
        repeated twice.
        """

        active_players = [

            player

            for player in players

            if not player.eliminated

        ]

        if not active_players:

            raise ValueError(
                "No active players."
            )

        required_cards = (

            len(active_players)

            * 2

        )

        if not self.can_deal(
            required_cards
        ):

            raise RuntimeError(
                "Not enough cards for hole cards."
            )

        # Clear previous hand

        for player in active_players:

            player.clear_hand()

        # Deal clockwise

        for _ in range(2):

            for player in active_players:

                player.receive_card(

                    self.deck.deal()

                )

    # ==================================================
    # Burn Card
    # ==================================================

    def burn_card(self) -> Card:
        """
        Burn one card before community cards.
        """

        if not self.can_deal():

            raise RuntimeError(
                "Cannot burn card. Deck empty."
            )

        return self.deck.deal()

    # ==================================================
    # Community Cards
    # ==================================================

    def deal_flop(
        self,
        table: Table
    ):
        """
        Burn one card.

        Deal three community cards.
        """

        if not self.can_deal(4):

            raise RuntimeError(
                "Not enough cards for flop."
            )

        self.burn_card()

        for _ in range(3):

            table.add_community_card(

                self.deck.deal()

            )

        table.set_street(

            Street.FLOP

        )

    # --------------------------------------------------

    def deal_turn(
        self,
        table: Table
    ):
        """
        Burn one card.

        Deal fourth community card.
        """

        if not self.can_deal(2):

            raise RuntimeError(
                "Not enough cards for turn."
            )

        self.burn_card()

        table.add_community_card(

            self.deck.deal()

        )

        table.set_street(

            Street.TURN

        )

    # --------------------------------------------------

    def deal_river(
        self,
        table: Table
    ):
        """
        Burn one card.

        Deal fifth community card.
        """

        if not self.can_deal(2):

            raise RuntimeError(
                "Not enough cards for river."
            )

        self.burn_card()

        table.add_community_card(

            self.deck.deal()

        )

        table.set_street(

            Street.RIVER

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
        Rotate dealer button clockwise.

        Heads-up:
        Button alternates between players.
        """

        if total_players < 2:

            raise ValueError(
                "Need at least two players."
            )

        table.rotate_dealer(
            total_players
        )

    # ==================================================
    # Player Positions + Roles
    # ==================================================

    def assign_positions(
        self,
        players: list[Player],
        table: Table
    ):
        """
        Assign table positions and temporary roles.

        Example:

        Heads-up:

        Player A:
            Position:
                BUTTON

            Roles:
                DEALER
                SMALL_BLIND

        Player B:
            Position:
                BIG_BLIND

            Roles:
                BIG_BLIND
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
        # Clear old state
        # ------------------------------------------

        for player in active_players:

            player.set_position(

                PlayerPosition.UNKNOWN

            )

            player.clear_roles()

        # ------------------------------------------
        # Dealer button order
        # ------------------------------------------

        dealer_index = (

            table.dealer_position % total

        )

        ordered_players = [

            active_players[

                (dealer_index + i) % total

            ]

            for i in range(total)

        ]

        # ------------------------------------------
        # Assign positions
        # ------------------------------------------

        positions = POSITION_LAYOUTS[total]

        for player, position in zip(

            ordered_players,

            positions

        ):

            player.set_position(

                position

            )

        # ------------------------------------------
        # Assign Dealer Role
        # ------------------------------------------

        button_player = ordered_players[0]

        button_player.add_role(

            PlayerRole.DEALER

        )

        # ------------------------------------------
        # Assign Blind Roles
        # ------------------------------------------

        if total == 2:

            # Heads-up:
            # Button player is also Small Blind

            button_player.add_role(

                PlayerRole.SMALL_BLIND

            )

        else:

            ordered_players[1].add_role(

                PlayerRole.SMALL_BLIND

            )

        # Big Blind always second player

        ordered_players[1].add_role(

            PlayerRole.BIG_BLIND

        )
        # ==================================================
    # Utility
    # ==================================================

    def remaining_cards(self) -> int:
        """
        Return remaining cards in deck.
        """

        return self.cards_remaining()

    # --------------------------------------------------

    def cards_remaining(self) -> int:
        """
        Return deck size.
        """

        return len(self.deck)

    # --------------------------------------------------

    def __len__(self):

        return self.cards_remaining()

    # --------------------------------------------------

    def reset(self):
        """
        Reset dealer deck for a new hand.

        Does NOT:
        - Change dealer button
        - Change player roles
        - Reset table

        Game controller handles those.
        """

        self.reset_deck()

    # --------------------------------------------------

    def can_deal_cards(
        self,
        amount: int
    ) -> bool:
        """
        Check if required number of cards exist.
        """

        return (

            self.cards_remaining()

            >=

            amount

        )

    # ==================================================
    # Debug
    # ==================================================

    def __repr__(self):

        return (

            "Dealer("

            f"remaining_cards={self.cards_remaining()}"

            ")"

        )

    # --------------------------------------------------

    def __str__(self):

        return (

            "========== DEALER ==========\n"

            f"Cards Remaining : "

            f"{self.cards_remaining()}"

        )