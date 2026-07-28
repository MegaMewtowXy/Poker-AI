import os

import json

from simulation.hand_history import HandHistory





class GameLogger:
    """
    Poker game event logger.

    Responsibilities
    ----------------
    • Create hand records
    • Record player actions
    • Record cards
    • Record results
    • Save hand histories
    • Load saved histories


    Does NOT
    --------
    • Decide poker actions
    • Modify game rules
    • Control AI
    """





    def __init__(
        self,
        save_directory="data/hand_history"
    ):

        self.current_hand = None


        self.history = []


        self.save_directory = save_directory





        # ======================================
        # Create Storage Directory
        # ======================================

        os.makedirs(

            self.save_directory,

            exist_ok=True

        )





    # ==========================================
    # Start Hand
    # ==========================================

    def start_hand(
        self,
        players,
        small_blind=0,
        big_blind=0,
        dealer_position=None
    ):
        """
        Create new hand history.
        """



        self.current_hand = HandHistory()





        self.current_hand.set_blinds(

            small_blind,

            big_blind

        )





        self.current_hand.dealer_position = (

            dealer_position

        )





        for player in players:


            self.current_hand.add_player(

                player

            )





        return self.current_hand





    # ==========================================
    # Get Current Hand
    # ==========================================

    def get_current_hand(
        self
    ):
        """
        Return active hand.
        """



        return self.current_hand
    
    # ==========================================
    # Record Action
    # ==========================================

    def log_action(
        self,
        player,
        action,
        amount=0,
        street=None
    ):
        """
        Record poker action.
        """



        if self.current_hand is None:

            raise ValueError(

                "No active hand to log."

            )





        self.current_hand.record_action(

            player,

            action,

            amount,

            street

        )





    # ==========================================
    # Record Hole Cards
    # ==========================================

    def log_hole_cards(
        self,
        player,
        cards
    ):
        """
        Record player's hole cards.
        """



        if self.current_hand is None:

            raise ValueError(

                "No active hand to log."

            )





        self.current_hand.record_hole_cards(

            player,

            cards

        )





    # ==========================================
    # Record Community Cards
    # ==========================================

    def log_community_cards(
        self,
        cards
    ):
        """
        Record flop, turn and river cards.
        """



        if self.current_hand is None:

            raise ValueError(

                "No active hand to log."

            )





        self.current_hand.add_community_cards(

            cards

        )





    # ==========================================
    # Update Pot
    # ==========================================

    def log_pot(
        self,
        pot
    ):
        """
        Record current pot size.
        """



        if self.current_hand is None:

            raise ValueError(

                "No active hand to log."

            )





        self.current_hand.update_pot(

            pot

        )





    # ==========================================
    # Record Winner
    # ==========================================

    def log_winner(
        self,
        player
    ):
        """
        Store hand winner.
        """



        if self.current_hand is None:

            raise ValueError(

                "No active hand to log."

            )





        self.current_hand.set_winner(

            player

        )





    # ==========================================
    # Save Single Hand
    # ==========================================

    def save_hand(
        self,
        hand=None
    ):
        """
        Save one hand history as JSON.

        Output:

        data/hand_history/
            hand_<id>.json
        """



        if hand is None:

            hand = self.current_hand





        if hand is None:

            raise ValueError(

                "No hand available to save."

            )





        file_name = (

            f"hand_{hand.hand_id}.json"

        )





        path = os.path.join(

            self.save_directory,

            file_name

        )





        with open(

            path,

            "w",

            encoding="utf-8"

        ) as file:


            json.dump(

                hand.to_dict(),

                file,

                indent=4,

                default=str

            )





        return path
    
    # ==========================================
    # Finish Hand
    # ==========================================

    def finish_hand(
        self,
        players
    ):
        """
        Complete current hand.

        Updates:
        - Final stacks
        - Completion status
        - Memory history
        - JSON storage
        """



        if self.current_hand is None:

            raise ValueError(

                "No active hand to finish."

            )





        self.current_hand.update_final_stacks(

            players

        )





        self.current_hand.complete()





        self.history.append(

            self.current_hand

        )





        # ======================================
        # Save Permanently
        # ======================================

        self.save_hand(

            self.current_hand

        )





        finished_hand = self.current_hand



        self.current_hand = None





        return finished_hand





    # ==========================================
    # Save All History
    # ==========================================

    def save_all_history(
        self
    ):
        """
        Save all completed hands
        into one JSON file.

        Useful for:
        - simulations
        - datasets
        - training
        """



        path = os.path.join(

            self.save_directory,

            "all_hands.json"

        )





        data = [


            hand.to_dict()

            for hand in self.history


        ]





        with open(

            path,

            "w",

            encoding="utf-8"

        ) as file:


            json.dump(

                data,

                file,

                indent=4,

                default=str

            )





        return path





    # ==========================================
    # Load History
    # ==========================================

    def load_history(
        self,
        as_objects=False
    ):
        """
        Load saved hand histories.


        Parameters
        ----------
        as_objects:
            False -> return dictionaries

            True -> return HandHistory objects
        """



        path = os.path.join(

            self.save_directory,

            "all_hands.json"

        )





        if not os.path.exists(path):

            return []





        with open(

            path,

            "r",

            encoding="utf-8"

        ) as file:


            data = json.load(file)





        if not as_objects:


            return data





        histories = []





        for item in data:


            hand = HandHistory()



            hand.from_dict(

                item

            )



            histories.append(

                hand

            )





        return histories





    # ==========================================
    # Get History
    # ==========================================

    def get_history(
        self
    ):
        """
        Return completed hands.
        """



        return self.history.copy()





    # ==========================================
    # Get Last Hand
    # ==========================================

    def get_last_hand(
        self
    ):
        """
        Return latest completed hand.
        """



        if not self.history:

            return None





        return self.history[-1]





    # ==========================================
    # Clear Logger
    # ==========================================

    def clear(
        self
    ):
        """
        Reset logger memory.

        Does not delete files.
        """



        self.current_hand = None


        self.history.clear()





    # ==========================================
    # Profile
    # ==========================================

    def profile(
        self
    ):
        """
        Logger information.
        """



        return {


            "saved_directory":

                self.save_directory,



            "completed_hands":

                len(

                    self.history

                ),



            "active_hand":

                self.current_hand is not None

        }





    # ==========================================
    # Debug
    # ==========================================

    def __str__(
        self
    ):

        return (

            "Poker Game Logger"

        )





    def __repr__(
        self
    ):

        return (

            f"GameLogger("

            f"hands={len(self.history)})"

        )