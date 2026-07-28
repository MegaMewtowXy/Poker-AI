from engine.game import Game

from models.player import Player


players = [

    Player("You"),

    Player("Bot 1", is_ai=True),

    Player("Bot 2", is_ai=True),

    Player("Bot 3", is_ai=True)

]

game = Game(players)

game.start_round()