import pygame
from ui.widgets import Button

class HelpModal:
    """
    Sleek Glassmorphic Overlay Modal for:
    1. Poker Hand Rankings Guide
    2. Interactive How-To-Play Tutorial
    3. AI Bot Strategy & Personality Dictionary (GTO, TAG, LAG, NIT, STATION)
    """

    HAND_RANKINGS = [
        ("1. ROYAL FLUSH", "[A♠ K♠ Q♠ J♠ T♠] • Highest possible hand of the same suit", (234, 179, 8)),
        ("2. STRAIGHT FLUSH", "[9♥ 8♥ 7♥ 6♥ 5♥] • 5 consecutive cards of the same suit", (250, 204, 21)),
        ("3. FOUR OF A KIND", "[A♣ A♦ A♥ A♠ K♦] • 4 cards of the exact same rank", (168, 85, 247)),
        ("4. FULL HOUSE", "[K♣ K♦ K♠ 8♥ 8♦] • 3 of a Kind + 1 Pair combined", (192, 132, 252)),
        ("5. FLUSH", "[A♦ J♦ 8♦ 4♦ 2♦] • Any 5 cards of the same suit", (59, 130, 246)),
        ("6. STRAIGHT", "[T♣ 9♦ 8♠ 7♥ 6♦] • 5 consecutive cards of any suit", (96, 165, 250)),
        ("7. THREE OF A KIND", "[Q♣ Q♦ Q♠ 9♥ 4♦] • 3 cards of the exact same rank", (45, 212, 191)),
        ("8. TWO PAIR", "[J♣ J♦ 7♠ 7♥ K♦] • 2 different matching pairs", (52, 211, 153)),
        ("9. ONE PAIR", "[10♣ 10♦ A♠ 8♥ 3♦] • 2 cards of matching rank", (148, 163, 184)),
        ("10. HIGH CARD", "[A♠ K♦ 9♣ 7♥ 4♦] • Highest single card counts", (203, 213, 225)),
    ]

    AI_DICTIONARY = [
        ("BALANCED (GTO)", "Game Theory Optimal. Plays balanced value-to-bluff ratios. Hard to exploit.", (59, 130, 246)),
        ("TAG (Tight-Aggressive)", "Plays selective strong hands & bets aggressively when involved (DeepBot style).", (16, 185, 129)),
        ("LAG (Loose-Aggressive)", "Plays a wide hand range & bluffs frequently to apply table pressure (AggroBot style).", (168, 85, 247)),
        ("NIT (Tight-Passive)", "Extremely cautious. Only plays monster hands (AA, KK) & folds easily to bets.", (234, 179, 8)),
        ("STATION (Calling Station)", "Plays almost every hand & calls all bets; rarely raises or folds. Easy value target!", (244, 63, 94)),
    ]

    TUTORIAL_SLIDES = [
        {
            "title": "TUTORIAL 1: OBJECTIVE & HOLE CARDS",
            "lines": [
                "• Texas Hold'em is played with a standard 52-card deck.",
                "• Every player receives 2 private Hole Cards face-down.",
                "• Your goal is to make the BEST 5-CARD POKER HAND",
                "  using your 2 Hole Cards + 5 Community Cards on the table."
            ]
        },
        {
            "title": "TUTORIAL 2: BETTING ROUNDS",
            "lines": [
                "1. PRE-FLOP : Betting occurs after receiving 2 hole cards.",
                "2. FLOP     : 3 community cards are dealt face-up.",
                "3. TURN     : The 4th community card is dealt face-up.",
                "4. RIVER    : The 5th & final community card is dealt.",
                "5. SHOWDOWN : Surviving players reveal cards. Best hand wins!"
            ]
        },
        {
            "title": "TUTORIAL 3: ACTION CONTROLS",
            "lines": [
                "• FOLD       : Discard your hand & forfeit the current pot.",
                "• CHECK      : Pass action to next player without putting in chips.",
                "• CALL       : Match the highest current bet at the table.",
                "• BET / RAISE: Increase the current bet amount using slider or buttons.",
                "• ALL-IN     : Bet all remaining chips in your stack!"
            ]
        },
        {
            "title": "TUTORIAL 4: AI BRAIN HUD & PRIVACY SHORTCUTS",
            "lines": [
                "• Press [TAB] or click 'AI BRAIN HUD' to toggle live AI calculations",
                "  (Win Equity %, Pot Odds, Opponent Threat & Reasoning).",
                "• Press [H] for Hole Card Privacy Toggle during local play.",
                "• Only active human sees their cards face-up when acting!"
            ]
        }
    ]

    def __init__(self, screen):
        self.screen = screen
        self.mode = None  # None, "RANKINGS", "TUTORIAL", "DICTIONARY"
        self.slide_idx = 0

    def open_rankings(self):
        self.mode = "RANKINGS"

    def open_tutorial(self):
        self.mode = "TUTORIAL"
        self.slide_idx = 0

    def open_dictionary(self):
        self.mode = "DICTIONARY"

    def close(self):
        self.mode = None

    def handle_event(self, event):
        if self.mode is None:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_F1):
                self.close()
                return True
            elif self.mode == "TUTORIAL":
                if event.key == pygame.K_RIGHT:
                    self.slide_idx = min(len(self.TUTORIAL_SLIDES) - 1, self.slide_idx + 1)
                    return True
                elif event.key == pygame.K_LEFT:
                    self.slide_idx = max(0, self.slide_idx - 1)
                    return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            sw, sh = self.screen.get_size()
            modal_w = int(sw * 0.70)
            modal_h = int(sh * 0.78)
            mx = (sw - modal_w) // 2
            my = (sh - modal_h) // 2

            close_rect = pygame.Rect(mx + modal_w - 40, my + 10, 30, 30)
            if close_rect.collidepoint(event.pos):
                self.close()
                return True

            if self.mode == "TUTORIAL":
                prev_rect = pygame.Rect(mx + 20, my + modal_h - 45, 90, 32)
                next_rect = pygame.Rect(mx + modal_w - 110, my + modal_h - 45, 90, 32)
                if prev_rect.collidepoint(event.pos):
                    self.slide_idx = max(0, self.slide_idx - 1)
                    return True
                elif next_rect.collidepoint(event.pos):
                    if self.slide_idx < len(self.TUTORIAL_SLIDES) - 1:
                        self.slide_idx += 1
                    else:
                        self.close()
                    return True

        return True

    def draw(self):
        if self.mode is None:
            return

        sw, sh = self.screen.get_size()
        modal_w = int(sw * 0.70)
        modal_h = int(sh * 0.78)
        mx = (sw - modal_w) // 2
        my = (sh - modal_h) // 2

        backdrop = pygame.Surface((sw, sh), pygame.SRCALPHA)
        backdrop.fill((0, 0, 0, 180))
        self.screen.blit(backdrop, (0, 0))

        modal_rect = pygame.Rect(mx, my, modal_w, modal_h)
        pygame.draw.rect(self.screen, (15, 23, 42), modal_rect, border_radius=14)
        pygame.draw.rect(self.screen, (59, 130, 246), modal_rect, 2, border_radius=14)

        close_rect = pygame.Rect(mx + modal_w - 40, my + 10, 30, 30)
        pygame.draw.rect(self.screen, (220, 38, 38), close_rect, border_radius=6)
        font_x = pygame.font.SysFont("arial", 16, bold=True)
        x_surf = font_x.render("X", True, (255, 255, 255))
        self.screen.blit(x_surf, (close_rect.x + 9, close_rect.y + 5))

        if self.mode == "RANKINGS":
            self._draw_rankings(mx, my, modal_w, modal_h)
        elif self.mode == "TUTORIAL":
            self._draw_tutorial(mx, my, modal_w, modal_h)
        elif self.mode == "DICTIONARY":
            self._draw_dictionary(mx, my, modal_w, modal_h)

    def _draw_rankings(self, mx, my, mw, mh):
        font_title = pygame.font.SysFont("arial", max(18, int(mh * 0.05)), bold=True)
        t_surf = font_title.render("OFFICIAL TEXAS HOLD'EM HAND RANKINGS", True, (241, 245, 249))
        self.screen.blit(t_surf, (mx + 20, my + 16))

        y_off = my + int(mh * 0.12)
        font_name = pygame.font.SysFont("arial", max(12, int(mh * 0.038)), bold=True)
        font_desc = pygame.font.SysFont("arial", max(11, int(mh * 0.032)))

        for rank_title, desc, color in self.HAND_RANKINGS:
            r_surf = font_name.render(rank_title, True, color)
            d_surf = font_desc.render(f"— {desc}", True, (226, 232, 240))
            self.screen.blit(r_surf, (mx + 25, y_off))
            self.screen.blit(d_surf, (mx + 220, y_off))
            y_off += int(mh * 0.08)

    def _draw_dictionary(self, mx, my, mw, mh):
        font_title = pygame.font.SysFont("arial", max(18, int(mh * 0.05)), bold=True)
        t_surf = font_title.render("AI BOT PERSONALITY & PLAYSTYLE DICTIONARY", True, (52, 211, 153))
        self.screen.blit(t_surf, (mx + 20, my + 16))

        y_off = my + int(mh * 0.13)
        font_name = pygame.font.SysFont("arial", max(13, int(mh * 0.04)), bold=True)
        font_desc = pygame.font.SysFont("arial", max(11, int(mh * 0.034)))

        for strat_title, desc, color in self.AI_DICTIONARY:
            r_surf = font_name.render(strat_title, True, color)
            d_surf = font_desc.render(desc, True, (241, 245, 249))
            self.screen.blit(r_surf, (mx + 25, y_off))
            self.screen.blit(d_surf, (mx + 25, y_off + 24))
            y_off += int(mh * 0.15)

    def _draw_tutorial(self, mx, my, mw, mh):
        slide = self.TUTORIAL_SLIDES[self.slide_idx]
        font_title = pygame.font.SysFont("arial", max(18, int(mh * 0.05)), bold=True)
        t_surf = font_title.render(slide["title"], True, (52, 211, 153))
        self.screen.blit(t_surf, (mx + 20, my + 20))

        font_body = pygame.font.SysFont("arial", max(13, int(mh * 0.038)))
        y_off = my + int(mh * 0.16)

        for line in slide["lines"]:
            line_surf = font_body.render(line, True, (241, 245, 249))
            self.screen.blit(line_surf, (mx + 25, y_off))
            y_off += int(mh * 0.09)

        font_p = pygame.font.SysFont("arial", 13, bold=True)
        pag_surf = font_p.render(f"Slide {self.slide_idx + 1} of {len(self.TUTORIAL_SLIDES)} (Use ← → keys)", True, (148, 163, 184))
        self.screen.blit(pag_surf, (mx + (mw - pag_surf.get_width()) // 2, my + mh - 40))

        if self.slide_idx > 0:
            prev_rect = pygame.Rect(mx + 20, my + mh - 45, 90, 32)
            pygame.draw.rect(self.screen, (51, 65, 85), prev_rect, border_radius=6)
            pr_surf = font_p.render("← PREV", True, (255, 255, 255))
            self.screen.blit(pr_surf, (prev_rect.x + 18, prev_rect.y + 6))

        next_rect = pygame.Rect(mx + mw - 110, my + mh - 45, 90, 32)
        next_bg = (16, 185, 129) if self.slide_idx == len(self.TUTORIAL_SLIDES) - 1 else (37, 99, 235)
        pygame.draw.rect(self.screen, next_bg, next_rect, border_radius=6)
        nx_text = "FINISH" if self.slide_idx == len(self.TUTORIAL_SLIDES) - 1 else "NEXT →"
        nx_surf = font_p.render(nx_text, True, (255, 255, 255))
        self.screen.blit(nx_surf, (next_rect.x + 16, next_rect.y + 6))
