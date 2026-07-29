import pygame
from AI.difficulty import Difficulty
from AI.strategy import Strategy
from AI.bot_player import BotPlayer
from integration.ai_player import AIPlayer
from models.player import Player
from ui.help_modal import HelpModal
from ui.widgets import Button, TextInput

class LobbyScreen:
    """
    Sleek & Modern Responsive Full Ring Lobby Screen.
    Features:
    - AI Strategy Dictionary Guide ([AI DICTIONARY] button).
    - Perfect Vertical Layout Alignment with Clean Header-Pill Spacing.
    - Configurable Starting Stack ($500, $1000, $2000, $5000, $10000).
    - Configurable Blinds ($10/$20, $25/$50, $50/$100).
    - Auto-Rebuy Mode (ON/OFF).
    - Dynamic 2 to 9 Full Ring Seats with custom names & AI personalities.
    """

    DIFFICULTIES = [("EASY", "EASY"), ("MEDIUM", "MED"), ("HARD", "HARD"), ("EXPERT", "EXPRT")]
    STRATEGIES = [
        ("BALANCED", "BAL"),
        ("TIGHT_AGGRESSIVE", "TAG"),
        ("LOOSE_AGGRESSIVE", "LAG"),
        ("TIGHT_PASSIVE", "NIT"),
        ("CALLING_STATION", "STATION")
    ]

    STACK_PRESETS = [500, 1000, 2000, 5000, 10000]
    BLIND_PRESETS = [(10, 20), (25, 50), (50, 100)]

    def __init__(self, screen, on_start_game):
        self.screen = screen
        self.on_start_game = on_start_game
        self.num_seats = 6
        self.help_modal = HelpModal(self.screen)

        # Table Configuration Values
        self.starting_chips = 1000
        self.small_blind = 10
        self.big_blind = 20
        self.auto_rebuy = True

        # Seats Profile Data
        self.seats = []
        self._init_default_seats()

        # Widgets
        self.dict_btn = None
        self.seat_count_buttons = []
        self.preset_buttons = []
        self.name_inputs = []
        self.start_button = None
        self._rebuild_layout()

    def _init_default_seats(self):
        self.seats = [
            {"type": "Human", "name": "Hero", "difficulty": "HARD", "strategy": "BALANCED"},
            {"type": "AI", "name": "DeepBot", "difficulty": "HARD", "strategy": "TIGHT_AGGRESSIVE"},
            {"type": "AI", "name": "AggroBot", "difficulty": "MEDIUM", "strategy": "LOOSE_AGGRESSIVE"},
            {"type": "AI", "name": "BluffKing", "difficulty": "HARD", "strategy": "LOOSE_AGGRESSIVE"},
            {"type": "AI", "name": "NitMaster", "difficulty": "MEDIUM", "strategy": "TIGHT_PASSIVE"},
            {"type": "AI", "name": "StationSam", "difficulty": "EASY", "strategy": "CALLING_STATION"},
            {"type": "AI", "name": "ExpertBot", "difficulty": "EXPERT", "strategy": "BALANCED"},
            {"type": "AI", "name": "SharkBot", "difficulty": "EXPERT", "strategy": "TIGHT_AGGRESSIVE"},
            {"type": "Human", "name": "Player 2", "difficulty": "MEDIUM", "strategy": "BALANCED"},
        ]

    def _apply_preset(self, preset):
        if preset == "heads_up_ai":
            self.num_seats = 2
            self.seats[0] = {"type": "AI", "name": "DeepBot", "difficulty": "HARD", "strategy": "TIGHT_AGGRESSIVE"}
            self.seats[1] = {"type": "AI", "name": "AggroBot", "difficulty": "MEDIUM", "strategy": "LOOSE_AGGRESSIVE"}
        elif preset == "human_vs_5_bots":
            self.num_seats = 6
            self.seats[0] = {"type": "Human", "name": "Hero", "difficulty": "HARD", "strategy": "BALANCED"}
            self.seats[1] = {"type": "AI", "name": "DeepBot", "difficulty": "HARD", "strategy": "TIGHT_AGGRESSIVE"}
            self.seats[2] = {"type": "AI", "name": "AggroBot", "difficulty": "MEDIUM", "strategy": "LOOSE_AGGRESSIVE"}
            self.seats[3] = {"type": "AI", "name": "BluffKing", "difficulty": "HARD", "strategy": "LOOSE_AGGRESSIVE"}
            self.seats[4] = {"type": "AI", "name": "NitMaster", "difficulty": "MEDIUM", "strategy": "TIGHT_PASSIVE"}
            self.seats[5] = {"type": "AI", "name": "StationSam", "difficulty": "EASY", "strategy": "CALLING_STATION"}
        elif preset == "full_ring_9_ai":
            self.num_seats = 9
            for i in range(9):
                self.seats[i]["type"] = "AI"
        elif preset == "human_vs_human":
            self.num_seats = 2
            self.seats[0] = {"type": "Human", "name": "Player 1", "difficulty": "HARD", "strategy": "BALANCED"}
            self.seats[1] = {"type": "Human", "name": "Player 2", "difficulty": "HARD", "strategy": "BALANCED"}

        self._rebuild_layout()

    def _rebuild_layout(self):
        sw, sh = self.screen.get_size()
        self.seat_count_buttons = []
        self.preset_buttons = []
        self.name_inputs = []

        # AI Dictionary Header Button
        self.dict_btn = Button((int(sw * 0.02), int(sh * 0.02), 125, 30), "AI DICTIONARY", callback=self.help_modal.open_dictionary, bg_color=(147, 51, 234), font_size=11)

        # Seat Count Buttons (2 to 9)
        btn_w = max(32, int(sw * 0.035))
        btn_h = max(26, int(sh * 0.04))
        start_x = (sw - (8 * (btn_w + 6))) // 2
        y_count = int(sh * 0.08)

        for count in range(2, 10):
            x = start_x + (count - 2) * (btn_w + 6)
            color = (16, 185, 129) if count == self.num_seats else (51, 65, 85)
            b = Button((x, y_count, btn_w, btn_h), str(count), callback=lambda c=count: self._set_seat_count(c), bg_color=color, font_size=13)
            self.seat_count_buttons.append(b)

        # Preset Buttons Bar
        pw = int(sw * 0.19)
        py = int(sh * 0.13)
        self.preset_buttons.append(Button((int(sw * 0.08), py, pw, btn_h), "Human vs 5 Bots", callback=lambda: self._apply_preset("human_vs_5_bots"), bg_color=(30, 41, 59), font_size=11))
        self.preset_buttons.append(Button((int(sw * 0.30), py, pw, btn_h), "Heads-Up Deep vs Aggro", callback=lambda: self._apply_preset("heads_up_ai"), bg_color=(30, 41, 59), font_size=11))
        self.preset_buttons.append(Button((int(sw * 0.51), py, pw, btn_h), "Full Ring 9-AI Battle", callback=lambda: self._apply_preset("full_ring_9_ai"), bg_color=(30, 41, 59), font_size=11))
        self.preset_buttons.append(Button((int(sw * 0.72), py, pw, btn_h), "Human vs Human", callback=lambda: self._apply_preset("human_vs_human"), bg_color=(30, 41, 59), font_size=11))

        # Rebuild Seat Cards Alignment
        cols = 3 if self.num_seats > 4 else (2 if self.num_seats > 1 else 1)
        card_w = int(sw * 0.27)
        card_h = int(sh * 0.19) if self.num_seats > 6 else int(sh * 0.215)

        y_start = int(sh * 0.235)
        y_gap = int(sh * 0.012) if self.num_seats > 6 else int(sh * 0.02)

        for i in range(self.num_seats):
            col = i % cols
            row = i // cols
            x = int(sw * 0.05) + col * (card_w + int(sw * 0.035))
            y = y_start + row * (card_h + y_gap)

            inp = TextInput((x + 75, y + 8, card_w - 170, 26), initial_text=self.seats[i]["name"], on_change=lambda text, idx=i: self._update_seat_name(idx, text))
            self.name_inputs.append(inp)

        # Start Button (Bottom Anchor)
        start_w = int(sw * 0.30)
        start_h = int(sh * 0.07)
        start_x = (sw - start_w) // 2
        start_y = int(sh * 0.90)
        self.start_button = Button((start_x, start_y, start_w, start_h), "START POKER GAME", callback=self._launch_game, bg_color=(16, 185, 129), hover_color=(5, 150, 105), font_size=20, radius=10)

    def _set_seat_count(self, count):
        self.num_seats = count
        self._rebuild_layout()

    def _update_seat_name(self, idx, text):
        if idx < len(self.seats):
            self.seats[idx]["name"] = text

    def handle_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self._rebuild_layout()

        if self.help_modal.mode is not None:
            if self.help_modal.handle_event(event):
                return True

        if self.dict_btn.handle_event(event) or self.start_button.handle_event(event):
            return True

        for btn in self.seat_count_buttons + self.preset_buttons:
            if btn.handle_event(event):
                return True

        for inp in self.name_inputs:
            if inp.handle_event(event):
                return True

        sw, sh = self.screen.get_size()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            y_cfg = int(sh * 0.18)
            s_w = int(sw * 0.06)
            for s_idx, val in enumerate(self.STACK_PRESETS):
                s_rect = pygame.Rect(int(sw * 0.15) + s_idx * (s_w + 4), y_cfg, s_w, 24)
                if s_rect.collidepoint(event.pos):
                    self.starting_chips = val
                    return True

            b_w = int(sw * 0.07)
            for b_idx, (sb, bb) in enumerate(self.BLIND_PRESETS):
                b_rect = pygame.Rect(int(sw * 0.58) + b_idx * (b_w + 4), y_cfg, b_w, 24)
                if b_rect.collidepoint(event.pos):
                    self.small_blind, self.big_blind = sb, bb
                    return True

            rebuy_rect = pygame.Rect(int(sw * 0.86), y_cfg, 75, 24)
            if rebuy_rect.collidepoint(event.pos):
                self.auto_rebuy = not self.auto_rebuy
                return True

            cols = 3 if self.num_seats > 4 else (2 if self.num_seats > 1 else 1)
            card_w = int(sw * 0.27)
            card_h = int(sh * 0.19) if self.num_seats > 6 else int(sh * 0.215)

            y_start = int(sh * 0.235)
            y_gap = int(sh * 0.012) if self.num_seats > 6 else int(sh * 0.02)

            for i in range(self.num_seats):
                col = i % cols
                row = i // cols
                x = int(sw * 0.05) + col * (card_w + int(sw * 0.035))
                y = y_start + row * (card_h + y_gap)

                type_rect = pygame.Rect(x + card_w - 85, y + 8, 75, 26)
                if type_rect.collidepoint(event.pos):
                    self.seats[i]["type"] = "AI" if self.seats[i]["type"] == "Human" else "Human"
                    return True

                if self.seats[i]["type"] == "AI":
                    pill_w = (card_w - 24) // 4
                    for d_idx, (d_code, d_label) in enumerate(self.DIFFICULTIES):
                        pill_rect = pygame.Rect(x + 12 + d_idx * pill_w, y + 54, pill_w - 4, 22)
                        if pill_rect.collidepoint(event.pos):
                            self.seats[i]["difficulty"] = d_code
                            return True

                    strat_w = (card_w - 24) // 5
                    for s_idx, (s_code, s_label) in enumerate(self.STRATEGIES):
                        s_pill_rect = pygame.Rect(x + 12 + s_idx * strat_w, y + 104, strat_w - 3, 22)
                        if s_pill_rect.collidepoint(event.pos):
                            self.seats[i]["strategy"] = s_code
                            return True

        return False

    def _launch_game(self):
        player_objects = []
        for i in range(self.num_seats):
            cfg = self.seats[i]
            p_name = cfg["name"].strip() or f"Player {i+1}"
            if cfg["type"] == "Human":
                p = Player(p_name, chips=self.starting_chips, is_ai=False)
            else:
                diff_key = cfg["difficulty"]
                strat_key = cfg["strategy"]
                diff = Difficulty[diff_key] if diff_key in Difficulty.__members__ else Difficulty.MEDIUM
                strat = Strategy[strat_key] if strat_key in Strategy.__members__ else Strategy.BALANCED
                bot = BotPlayer(p_name, difficulty=diff, strategy=strat)
                p = AIPlayer(p_name, bot=bot, chips=self.starting_chips)

            player_objects.append(p)

        self.on_start_game(player_objects, self.starting_chips, self.small_blind, self.big_blind, self.auto_rebuy)

    def draw(self):
        self.screen.fill((11, 15, 25))
        sw, sh = self.screen.get_size()

        # Title & AI Dictionary Button
        self.dict_btn.draw(self.screen)
        font_title = pygame.font.SysFont("arial", max(18, int(sh * 0.038)), bold=True)
        title_surf = font_title.render("TEXAS HOLD'EM POKER - FULL RING LOBBY", True, (241, 245, 249))
        self.screen.blit(title_surf, ((sw - title_surf.get_width()) // 2, int(sh * 0.02)))

        for btn in self.seat_count_buttons + self.preset_buttons:
            btn.draw(self.screen)

        # Table Settings Bar
        y_cfg = int(sh * 0.18)
        font_cfg = pygame.font.SysFont("arial", max(10, int(sh * 0.018)), bold=True)

        stack_lbl = font_cfg.render("STACK:", True, (148, 163, 184))
        self.screen.blit(stack_lbl, (int(sw * 0.08), y_cfg + 4))

        s_w = int(sw * 0.06)
        for s_idx, val in enumerate(self.STACK_PRESETS):
            s_rect = pygame.Rect(int(sw * 0.15) + s_idx * (s_w + 4), y_cfg, s_w, 24)
            sel = (self.starting_chips == val)
            bg = (16, 185, 129) if sel else (51, 65, 85)
            pygame.draw.rect(self.screen, bg, s_rect, border_radius=4)
            txt = font_cfg.render(f"${val}", True, (255, 255, 255) if sel else (148, 163, 184))
            self.screen.blit(txt, (s_rect.x + (s_rect.width - txt.get_width()) // 2, s_rect.y + 3))

        blind_lbl = font_cfg.render("BLINDS:", True, (148, 163, 184))
        self.screen.blit(blind_lbl, (int(sw * 0.51), y_cfg + 4))

        b_w = int(sw * 0.07)
        for b_idx, (sb, bb) in enumerate(self.BLIND_PRESETS):
            b_rect = pygame.Rect(int(sw * 0.58) + b_idx * (b_w + 4), y_cfg, b_w, 24)
            sel = (self.small_blind == sb and self.big_blind == bb)
            bg = (59, 130, 246) if sel else (51, 65, 85)
            pygame.draw.rect(self.screen, bg, b_rect, border_radius=4)
            txt = font_cfg.render(f"${sb}/${bb}", True, (255, 255, 255) if sel else (148, 163, 184))
            self.screen.blit(txt, (b_rect.x + (b_rect.width - txt.get_width()) // 2, b_rect.y + 3))

        rebuy_rect = pygame.Rect(int(sw * 0.86), y_cfg, 75, 24)
        r_bg = (16, 185, 129) if self.auto_rebuy else (220, 38, 38)
        pygame.draw.rect(self.screen, r_bg, rebuy_rect, border_radius=4)
        r_txt = font_cfg.render("REBUY: ON" if self.auto_rebuy else "REBUY: OFF", True, (255, 255, 255))
        self.screen.blit(r_txt, (rebuy_rect.x + (rebuy_rect.width - r_txt.get_width()) // 2, rebuy_rect.y + 3))

        # Seat Grid Cards
        cols = 3 if self.num_seats > 4 else (2 if self.num_seats > 1 else 1)
        card_w = int(sw * 0.27)
        card_h = int(sh * 0.19) if self.num_seats > 6 else int(sh * 0.215)

        y_start = int(sh * 0.235)
        y_gap = int(sh * 0.012) if self.num_seats > 6 else int(sh * 0.02)

        for i in range(self.num_seats):
            col = i % cols
            row = i // cols
            x = int(sw * 0.05) + col * (card_w + int(sw * 0.035))
            y = y_start + row * (card_h + y_gap)
            rect = pygame.Rect(x, y, card_w, card_h)

            cfg = self.seats[i]
            is_human = cfg["type"] == "Human"
            card_bg = (30, 41, 59) if is_human else (15, 23, 42)
            border_color = (59, 130, 246) if is_human else (168, 85, 247)

            pygame.draw.rect(self.screen, card_bg, rect, border_radius=10)
            pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=10)

            font_lbl = pygame.font.SysFont("arial", max(11, int(card_h * 0.13)), bold=True)
            seat_lbl = font_lbl.render(f"Seat {i+1}:", True, (148, 163, 184))
            self.screen.blit(seat_lbl, (x + 10, y + 10))

            if i < len(self.name_inputs):
                self.name_inputs[i].draw(self.screen)

            type_rect = pygame.Rect(x + card_w - 85, y + 8, 75, 26)
            type_bg = (37, 99, 235) if is_human else (147, 51, 234)
            pygame.draw.rect(self.screen, type_bg, type_rect, border_radius=6)
            type_surf = font_lbl.render("HUMAN" if is_human else "AI BOT", True, (255, 255, 255))
            self.screen.blit(type_surf, (type_rect.x + (75 - type_surf.get_width()) // 2, type_rect.y + 3))

            if not is_human:
                font_hdr = pygame.font.SysFont("arial", max(9, int(card_h * 0.09)), bold=True)
                
                # Difficulty Header & Pills (Generous 18px Vertical Gap)
                diff_hdr = font_hdr.render("DIFFICULTY:", True, (148, 163, 184))
                self.screen.blit(diff_hdr, (x + 12, y + 36))

                font_pill = pygame.font.SysFont("arial", max(9, int(card_h * 0.105)), bold=True)
                pill_w = (card_w - 24) // 4
                for d_idx, (d_code, d_label) in enumerate(self.DIFFICULTIES):
                    pill_rect = pygame.Rect(x + 12 + d_idx * pill_w, y + 54, pill_w - 4, 22)
                    selected = (cfg["difficulty"] == d_code)
                    p_bg = (16, 185, 129) if selected else (51, 65, 85)
                    pygame.draw.rect(self.screen, p_bg, pill_rect, border_radius=4)
                    p_surf = font_pill.render(d_label, True, (255, 255, 255) if selected else (148, 163, 184))
                    self.screen.blit(p_surf, (pill_rect.x + (pill_rect.width - p_surf.get_width()) // 2, pill_rect.y + 2))

                # Strategy Style Header & Pills (Generous 18px Vertical Gap)
                strat_hdr = font_hdr.render("PLAYSTYLE (AI STRATEGY):", True, (148, 163, 184))
                self.screen.blit(strat_hdr, (x + 12, y + 86))

                strat_w = (card_w - 24) // 5
                for s_idx, (s_code, s_label) in enumerate(self.STRATEGIES):
                    s_pill_rect = pygame.Rect(x + 12 + s_idx * strat_w, y + 104, strat_w - 3, 22)
                    selected = (cfg["strategy"] == s_code)
                    s_bg = (59, 130, 246) if selected else (51, 65, 85)
                    pygame.draw.rect(self.screen, s_bg, s_pill_rect, border_radius=4)
                    sp_surf = font_pill.render(s_label, True, (255, 255, 255) if selected else (148, 163, 184))
                    self.screen.blit(sp_surf, (s_pill_rect.x + (s_pill_rect.width - sp_surf.get_width()) // 2, s_pill_rect.y + 2))
            else:
                font_det = pygame.font.SysFont("arial", max(11, int(card_h * 0.13)))
                h_surf = font_det.render("Interactive Human Player (Local Play)", True, (148, 163, 184))
                self.screen.blit(h_surf, (x + 12, y + 60))

        self.start_button.draw(self.screen)

        # Draw AI Dictionary Modal if open
        self.help_modal.draw()
