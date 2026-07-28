from models.player import Player


class Pot:
    """
    Represents one poker pot.

    A Texas Hold'em hand always has one main pot
    and may have multiple side pots.
    """

    def __init__(self):

        self.amount = 0

        self.eligible_players: list[Player] = []

    # -----------------------------------

    def add_chips(self, amount: int):

        self.amount += amount

    # -----------------------------------

    def add_player(self, player: Player):

        if player not in self.eligible_players:
            self.eligible_players.append(player)

    # -----------------------------------

    def remove_player(self, player: Player):

        if player in self.eligible_players:
            self.eligible_players.remove(player)

    # -----------------------------------

    def clear(self):

        self.amount = 0

        self.eligible_players.clear()

    # -----------------------------------

    def __len__(self):

        return len(self.eligible_players)

    # -----------------------------------

    def __str__(self):

        names = ", ".join(
            player.name
            for player in self.eligible_players
        )

        return (
            f"Pot(${self.amount})\n"
            f"Eligible Players: {names}"
        )