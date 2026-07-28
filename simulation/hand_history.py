from datetime import datetime

import uuid





class HandHistory:
    """
    Complete poker hand recorder.


    Responsibilities
    ----------------
    • Store complete hand information
    • Store players
    • Store actions
    • Store board cards
    • Store winner
    • Export hand data


    Supports
    --------
    • Human players
    • AI players


    Does NOT
    --------
    • Decide actions
    • Run poker rules
    • Calculate statistics
    """





    def __init__(
        self,
        hand_id=None
    ):

        self.hand_id = (

            hand_id

            if hand_id is not None

            else str(uuid.uuid4())

        )



        self.created_at = str(

            datetime.now()

        )



        # ======================================
        # Hand Information
        # ======================================


        self.game_type = "Texas Hold'em"


        self.small_blind = 0


        self.big_blind = 0


        self.dealer_position = None





        # ======================================
        # Players
        # ======================================


        self.players = []





        # ======================================
        # Cards
        # ======================================


        self.hole_cards = {}


        self.community_cards = []





        # ======================================
        # Actions
        # ======================================


        self.actions = []





        # ======================================
        # Result
        # ======================================


        self.winner = None


        self.pot = 0


        self.completed = False






    # ==========================================
    # Card Serialization
    # ==========================================

    def serialize_cards(
        self,
        cards
    ):
        """
        Convert card objects into
        JSON compatible format.

        Supports:
        - Card objects
        - Strings
        """



        serialized = []



        for card in cards:


            if isinstance(

                card,

                str

            ):

                serialized.append(

                    card

                )



            else:

                serialized.append(

                    str(card)

                )



        return serialized
    
    # ==========================================
    # Add Player
    # ==========================================

    def add_player(
        self,
        player,
        position=None
    ):
        """
        Add player information.

        Works with:
        - Human Player
        - AIPlayer
        """



        player_data = {


            "name":

                player.name,



            "position":

                position,



            "starting_chips":

                player.chips,



            "ending_chips":

                None

        }





        self.players.append(

            player_data

        )





    # ==========================================
    # Set Blinds
    # ==========================================

    def set_blinds(
        self,
        small_blind,
        big_blind
    ):
        """
        Store blind values.
        """



        self.small_blind = small_blind


        self.big_blind = big_blind





    # ==========================================
    # Store Hole Cards
    # ==========================================

    def record_hole_cards(
        self,
        player,
        cards
    ):
        """
        Store player's hole cards.

        Converted into JSON-safe format.
        """



        self.hole_cards[player.name] = (

            self.serialize_cards(

                cards

            )

        )





    # ==========================================
    # Add Community Cards
    # ==========================================

    def add_community_cards(
        self,
        cards
    ):
        """
        Add cards dealt on board.

        Converted into JSON-safe format.
        """



        self.community_cards.extend(

            self.serialize_cards(

                cards

            )

        )





    # ==========================================
    # Record Action
    # ==========================================

    def record_action(
        self,
        player,
        action,
        amount=0,
        street=None
    ):
        """
        Record one poker action.

        Example:

        Player raises 100
        Player calls 100
        """



        if hasattr(

            action,

            "name"

        ):

            action_value = action.name



        else:

            action_value = action





        action_data = {


            "player":

                player.name,



            "action":

                action_value,



            "amount":

                amount,



            "street":

                street,



            "time":

                str(datetime.now())

        }





        self.actions.append(

            action_data

        )





    # ==========================================
    # Action Count
    # ==========================================

    def action_count(
        self
    ):
        """
        Return total actions
        recorded in this hand.
        """



        return len(

            self.actions

        )





    # ==========================================
    # Update Pot
    # ==========================================

    def update_pot(
        self,
        amount
    ):
        """
        Update current pot size.
        """



        self.pot = amount





    # ==========================================
    # Set Winner
    # ==========================================

    def set_winner(
        self,
        player
    ):
        """
        Store winning player.
        """



        if player is None:


            self.winner = None


            return





        self.winner = {


            "name":

                player.name,



            "chips":

                player.chips

        }





    # ==========================================
    # Finish Hand
    # ==========================================

    def complete(
        self
    ):
        """
        Mark hand as completed.
        """



        self.completed = True





    # ==========================================
    # Update Ending Chips
    # ==========================================

    def update_final_stacks(
        self,
        players
    ):
        """
        Store final chip counts.
        """



        for player_data in self.players:


            for player in players:


                if player.name == player_data["name"]:


                    player_data["ending_chips"] = (

                        player.chips

                    )
    
    # ==========================================
    # Convert To Dictionary
    # ==========================================

    def to_dict(
        self
    ):
        """
        Convert hand history into
        JSON serializable dictionary.

        Used by:
        - Logger
        - Replay System
        - Database
        """



        return {


            "hand_id":

                self.hand_id,



            "created_at":

                self.created_at,



            "game_type":

                self.game_type,



            "small_blind":

                self.small_blind,



            "big_blind":

                self.big_blind,



            "dealer_position":

                self.dealer_position,



            "players":

                self.players,



            "hole_cards":

                self.hole_cards,



            "community_cards":

                self.community_cards,



            "actions":

                self.actions,



            "winner":

                self.winner,



            "pot":

                self.pot,



            "completed":

                self.completed

        }





    # ==========================================
    # Load From Dictionary
    # ==========================================

    def from_dict(
        self,
        data
    ):
        """
        Restore hand history
        from saved JSON data.
        """



        self.hand_id = data.get(

            "hand_id",

            self.hand_id

        )



        self.created_at = data.get(

            "created_at",

            self.created_at

        )



        self.game_type = data.get(

            "game_type",

            "Texas Hold'em"

        )



        self.small_blind = data.get(

            "small_blind",

            0

        )



        self.big_blind = data.get(

            "big_blind",

            0

        )



        self.dealer_position = data.get(

            "dealer_position"

        )



        self.players = data.get(

            "players",

            []

        )



        self.hole_cards = data.get(

            "hole_cards",

            {}

        )



        self.community_cards = data.get(

            "community_cards",

            []

        )



        self.actions = data.get(

            "actions",

            []

        )



        self.winner = data.get(

            "winner"

        )



        self.pot = data.get(

            "pot",

            0

        )



        self.completed = data.get(

            "completed",

            False

        )





        return self





    # ==========================================
    # Profile
    # ==========================================

    def profile(
        self
    ):
        """
        Basic hand information.
        """



        return {


            "hand_id":

                self.hand_id,



            "players":

                len(

                    self.players

                ),



            "actions":

                self.action_count(),



            "community_cards":

                len(

                    self.community_cards

                ),



            "winner":

                self.winner,



            "pot":

                self.pot,



            "completed":

                self.completed

        }





    # ==========================================
    # Debug
    # ==========================================

    def __str__(
        self
    ):

        return (

            f"HandHistory("

            f"{self.hand_id})"

        )





    def __repr__(
        self
    ):

        return (

            "HandHistory()"

        )