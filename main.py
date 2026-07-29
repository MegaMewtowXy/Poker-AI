import sys
import pygame
from ui.lobby import LobbyScreen
from ui.game_screen import GameScreen

class PokerApp:
    """
    Main Pygame Texas Hold'em Application Controller.
    Manages 60 FPS loop, responsive window scaling, table configuration, and screen state transitions.
    """

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Texas Hold'em AI Engine - Desktop Edition")

        # Resizable Window
        self.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # State Manager
        self.state = "LOBBY"
        self.lobby_screen = LobbyScreen(self.screen, self.start_game)
        self.game_screen = None

    def start_game(self, players, starting_chips=1000, small_blind=10, big_blind=20, auto_rebuy=True):
        """
        Transition from Lobby to Table Game with custom table configurations.
        """
        self.game_screen = GameScreen(self.screen, players, self.return_to_lobby, starting_chips, small_blind, big_blind, auto_rebuy)
        self.state = "GAME"

    def return_to_lobby(self):
        self.state = "LOBBY"

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

                if self.state == "LOBBY":
                    self.lobby_screen.handle_event(event)
                elif self.state == "GAME" and self.game_screen:
                    self.game_screen.handle_event(event)

            if self.state == "LOBBY":
                self.lobby_screen.draw()
            elif self.state == "GAME" and self.game_screen:
                self.game_screen.draw()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    app = PokerApp()
    app.run()