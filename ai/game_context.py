from dataclasses import dataclass, field

from models.card import Card
from models.player_position import PlayerPosition
from models.player_role import PlayerRole
from models.street import Street


@dataclass
class GameContext:
    """
    Complete poker information available to AI.

    Represents only information a real player
    can know during a hand.

    This class does NOT expose:
    - opponent hole cards
    - hidden information
    - future cards
    """

    # ==================================================
    # Cards
    # ==================================================

    hole_cards: list[Card] = field(
        default_factory=list
    )

    community_cards: list[Card] = field(
        default_factory=list
    )

    # ==================================================
    # Table Information
    # ==================================================

    position: PlayerPosition | None = None

    roles: set[PlayerRole] = field(
        default_factory=set
    )

    street: Street = Street.PRE_FLOP

    pot_size: int = 0

    current_bet: int = 0

    player_current_bet: int = 0

    call_amount: int = 0

    min_raise: int = 0

    big_blind: int = 0

    # ==================================================
    # Player Information
    # ==================================================

    player_stack: int = 0

    players_remaining: int = 0

    # ==================================================
    # Opponent Information
    # ==================================================

    opponents: list[dict] = field(
        default_factory=list
    )

    # ==================================================
    # History
    # ==================================================

    betting_history: list[dict] = field(
        default_factory=list
    )

    # ==================================================
    # Helpers
    # ==================================================

    def stack_in_bb(self) -> float:
        """
        Return stack size in big blinds.
        """

        if self.big_blind <= 0:

            return 0.0

        return round(

            self.player_stack

            /

            self.big_blind,

            2

        )

    # --------------------------------------------------

    def pot_odds(self) -> float:
        """
        Required equity to call.

        Formula:

        call / (pot + call)
        """

        if self.call_amount <= 0:

            return 0.0

        return round(

            self.call_amount

            /

            (

                self.pot_size

                +

                self.call_amount

            ),

            3

        )

    # --------------------------------------------------

    def is_pre_flop(self) -> bool:

        return self.street == Street.PRE_FLOP

    # --------------------------------------------------

    def is_post_flop(self) -> bool:

        return self.street in {

            Street.FLOP,

            Street.TURN,

            Street.RIVER

        }

    # --------------------------------------------------

    def has_to_call(self) -> bool:

        return self.call_amount > 0

    # --------------------------------------------------

    def effective_stack_bb(self) -> float:
        """
        Useful for AI decisions.

        Returns stack depth.
        """

        return self.stack_in_bb()

    # ==================================================
    # Debug
    # ==================================================

    def summary(self) -> dict:
        """
        Debug information.
        """

        return {

            "street": str(self.street),

            "position": str(self.position),

            "roles": [

                str(role)

                for role in self.roles

            ],

            "pot": self.pot_size,

            "call_amount": self.call_amount,

            "pot_odds": self.pot_odds(),

            "stack": self.player_stack,

            "stack_bb": self.stack_in_bb(),

            "players_remaining":

                self.players_remaining

        }
        # ==================================================
    # Debug
    # ==================================================

    def summary(self) -> dict:

        """
        Debug information.
        """

        return {

            "street": str(self.street),


            "position": str(self.position),


            "roles": [

                str(role)

                for role in self.roles

            ],


            "pot": self.pot_size,


            "call_amount": self.call_amount,


            "pot_odds": self.pot_odds(),


            "stack": self.player_stack,


            "stack_bb": self.stack_in_bb(),


            "players_remaining":

                self.players_remaining

        }