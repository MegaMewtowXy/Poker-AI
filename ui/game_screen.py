import math
import pygame
from engine.evaluator import HandEvaluator
from engine.game import Game
from models.action import Action
from models.player_role import PlayerRole
from ui.card_renderer import card_renderer
from ui.help_modal import HelpModal
from ui.widgets import Button, Slider

class GameScreen:
    """
    Ultra-Modern 60 FPS Pygame Poker Table Screen for 2 to 9 Players.
    Features:
    - Interactive SHOW CARDS / MUCK CARDS Option when winning by fold or ending a hand.
    - Click seat pod at hand end to reveal/show bluffs to opponents!
    - Smart 4-Quadrant Radial Hole Card Positioning: Guaranteed zero overlap across all seats, pot badge, community cards, top header buttons, and action bar.
    - Smooth Street Pacing Delay (750ms between Flop, Turn, River dealing & Showdown).
    - AI vs AI Spectator Mode with Pacing Delay (450ms per turn), Pause/Resume, and Terminate Battle buttons.
    """

    def __init__(self, screen, players, on_exit_to_lobby, starting_chips=1000, small_blind=10, big_blind=20, auto_rebuy=True):
        self.screen = screen
        self.players = players
        self.on_exit_to_lobby = on_exit_to_lobby
        self.starting_chips = starting_chips
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.auto_rebuy = auto_rebuy

        # Engine & Evaluator
        self.game = Game(players=self.players)
        self.evaluator = HandEvaluator()
        self.help_modal = HelpModal(self.screen)

        # State Variables
        self.game_over = False
        self.hand_in_progress = False
        self.is_showdown = False
        self.show_ai_hud = True
        self.show_hole_cards = True
        self.is_all_ai = all(getattr(p, "is_ai", False) for p in self.players)
        self.ai_paused = False
        self.ai_delay_ms = 450      # 450ms pacing delay for visible AI moves
        self.street_delay_ms = 750  # 750ms pacing delay between Flop, Turn, River dealing
        self.last_ai_move_time = 0
        self.display_pot = 0

        # Show / Muck Cards State
        self.winner_player = None
        self.show_winner_cards = False
        self.user_showed_players = set()

        self.status_message = f"Table Configured: ${self.starting_chips} Stacks • ${self.small_blind}/${self.big_blind} Blinds"
        self.current_ai_analysis = None
        self.last_action_texts = {}
        self.left_players = set()

        # Navigation & Action Widgets
        self.fold_btn = None
        self.call_btn = None
        self.bet_btn = None
        self.show_cards_btn = None
        self.muck_cards_btn = None
        self.pause_ai_btn = None
        self.action_buttons = []
        self.quick_bet_buttons = []
        self.bet_slider = None
        self.hud_toggle_btn = None
        self.rankings_btn = None
        self.tutorial_btn = None
        self.lobby_btn = None
        self._rebuild_layout()

        # Start first hand
        self._start_new_hand()

    def _start_new_hand(self):
        rebought = []
        if self.auto_rebuy:
            for p in self.players:
                if p.chips <= 0 and p.name not in self.left_players:
                    p.chips = self.starting_chips
                    rebought.append(p.name)

        active = [p for p in self.players if p.chips > 0 and p.name not in self.left_players]
        if len(active) < 2:
            self.game_over = True
            winner_name = active[0].name if active else "None"
            self.status_message = f"WINNER: {winner_name}"
            return

        self.is_showdown = False
        self.display_pot = 0
        self.winner_player = None
        self.show_winner_cards = False
        self.user_showed_players = set()
        self.last_action_texts = {}

        for p in self.players:
            if p.name in self.left_players:
                self.last_action_texts[p.name] = "LEFT TABLE"
            elif p.chips <= 0:
                self.last_action_texts[p.name] = "ELIMINATED"

        self.game.start_hand()

        # Display initial Small Blind and Big Blind actions
        for p in self.players:
            if p.has_role(PlayerRole.SMALL_BLIND):
                self.last_action_texts[p.name] = f"SB ${self.small_blind}"
            elif p.has_role(PlayerRole.BIG_BLIND):
                self.last_action_texts[p.name] = f"BB ${self.big_blind}"

        self.game.betting_round.set_street(self.game.betting_round.street or 1)
        self.game.betting_round.start()
        self.hand_in_progress = True
        self.last_ai_move_time = pygame.time.get_ticks()

        if rebought:
            self.status_message = f"Rebought {', '.join(rebought)} • Hand #{self.game.hand_number} Pre-Flop"
        else:
            self.status_message = f"Hand #{self.game.hand_number} Pre-Flop (${self.small_blind}/${self.big_blind})"
        self._check_next_turn()

    def _rebuild_layout(self):
        sw, sh = self.screen.get_size()
        self.action_buttons = []
        self.quick_bet_buttons = []

        self.hud_toggle_btn = Button((int(sw * 0.02), int(sh * 0.02), 115, 30), "AI BRAIN HUD", callback=self._toggle_hud, bg_color=(30, 41, 59), font_size=11)
        self.rankings_btn = Button((int(sw * 0.12), int(sh * 0.02), 125, 30), "HAND RANKINGS", callback=self.help_modal.open_rankings, bg_color=(147, 51, 234), font_size=11)
        self.tutorial_btn = Button((int(sw * 0.23), int(sh * 0.02), 105, 30), "TUTORIAL", callback=self.help_modal.open_tutorial, bg_color=(16, 185, 129), font_size=11)

        btn_text = "TERMINATE BATTLE" if self.is_all_ai else "EXIT LOBBY"
        self.lobby_btn = Button((int(sw * 0.32), int(sh * 0.02), 130, 30), btn_text, callback=self.on_exit_to_lobby, bg_color=(220, 38, 38), hover_color=(185, 28, 28), font_size=11)

        if self.is_all_ai:
            self.pause_ai_btn = Button((int(sw * 0.44), int(sh * 0.02), 110, 30), "PAUSE BATTLE", callback=self._toggle_ai_pause, bg_color=(180, 83, 9), font_size=11)

        bar_w = int(sw * 0.82)
        bar_h = int(sh * 0.13)
        bar_x = (sw - bar_w) // 2
        bar_y = int(sh * 0.85)

        btn_w = int(bar_w * 0.17)
        btn_h = int(bar_h * 0.55)
        btn_y = bar_y + int(bar_h * 0.40)

        self.fold_btn = Button((bar_x + int(bar_w * 0.02), btn_y, btn_w, btn_h), "FOLD", callback=lambda: self._handle_human_action(Action.FOLD), bg_color=(220, 38, 38), hover_color=(185, 28, 28), font_size=14)
        self.call_btn = Button((bar_x + int(bar_w * 0.20), btn_y, btn_w, btn_h), "CHECK", callback=lambda: self._handle_human_action(Action.CALL), bg_color=(37, 99, 235), hover_color=(29, 78, 216), font_size=14)

        qw = int(bar_w * 0.085)
        qh = int(bar_h * 0.32)
        qy = bar_y + 4
        qx_start = bar_x + int(bar_w * 0.39)

        self.quick_bet_buttons.append(Button((qx_start, qy, qw, qh), "MIN", callback=lambda: self._set_slider_ratio(0.0), bg_color=(51, 65, 85), font_size=11))
        self.quick_bet_buttons.append(Button((qx_start + qw + 4, qy, qw, qh), "+3BB", callback=lambda: self._set_slider_ratio(0.2), bg_color=(51, 65, 85), font_size=11))
        self.quick_bet_buttons.append(Button((qx_start + 2 * (qw + 4), qy, qw, qh), "1/2 POT", callback=lambda: self._set_slider_ratio(0.5), bg_color=(51, 65, 85), font_size=11))
        self.quick_bet_buttons.append(Button((qx_start + 3 * (qw + 4), qy, qw, qh), "POT", callback=lambda: self._set_slider_ratio(0.8), bg_color=(51, 65, 85), font_size=11))
        self.quick_bet_buttons.append(Button((qx_start + 4 * (qw + 4), qy, qw, qh), "ALL-IN", callback=lambda: self._set_slider_ratio(1.0), bg_color=(180, 83, 9), font_size=11))

        slider_x = bar_x + int(bar_w * 0.39)
        slider_w = int(bar_w * 0.42)
        self.bet_slider = Slider((slider_x, btn_y + 12, slider_w, 20), min_val=self.big_blind, max_val=self.starting_chips, initial_val=self.big_blind * 2, step=self.small_blind)

        self.bet_btn = Button((bar_x + int(bar_w * 0.82), btn_y, btn_w, btn_h), "BET / RAISE", callback=lambda: self._handle_human_action(Action.BET, self.bet_slider.val), bg_color=(16, 185, 129), hover_color=(5, 150, 105), font_size=13)

        self.action_buttons = [self.fold_btn, self.call_btn, self.bet_btn]

        # Post-Hand Show Cards / Muck Cards Buttons
        self.show_cards_btn = Button((bar_x + int(bar_w * 0.28), btn_y, int(bar_w * 0.20), btn_h), "SHOW CARDS", callback=self._show_winner_cards_action, bg_color=(16, 185, 129), hover_color=(5, 150, 105), font_size=13)
        self.muck_cards_btn = Button((bar_x + int(bar_w * 0.52), btn_y, int(bar_w * 0.20), btn_h), "MUCK CARDS", callback=self._muck_winner_cards_action, bg_color=(51, 65, 85), hover_color=(71, 85, 105), font_size=13)

    def _show_winner_cards_action(self):
        self.show_winner_cards = True
        if self.winner_player:
            self.user_showed_players.add(self.winner_player.name)
            self.status_message = f"{self.winner_player.name} SHOWED CARDS! Press SPACE for Next Hand"

    def _muck_winner_cards_action(self):
        self.show_winner_cards = False
        if self.winner_player and self.winner_player.name in self.user_showed_players:
            self.user_showed_players.remove(self.winner_player.name)
        self.status_message = "Cards Mucked! Press SPACE for Next Hand"

    def _toggle_ai_pause(self):
        self.ai_paused = not self.ai_paused
        if self.pause_ai_btn:
            self.pause_ai_btn.text = "RESUME BATTLE" if self.ai_paused else "PAUSE BATTLE"
            self.pause_ai_btn.bg_color = (16, 185, 129) if self.ai_paused else (180, 83, 9)

    def _update_action_button_labels(self):
        curr_p = self.game.betting_round.current_player_or_none()
        if not curr_p:
            return

        tbl_bet = getattr(self.game.table, "current_bet", 0)
        p_bet = getattr(curr_p, "current_bet", 0)
        call_amt = tbl_bet - p_bet

        if call_amt <= 0:
            self.call_btn.text = "CHECK"
        else:
            self.call_btn.text = f"CALL ${call_amt}"

        val = self.bet_slider.val if self.bet_slider else 0
        if val >= curr_p.chips:
            self.bet_btn.text = f"ALL-IN (${curr_p.chips})"
        elif tbl_bet > 0:
            self.bet_btn.text = f"RAISE TO ${val}"
        else:
            self.bet_btn.text = f"BET ${val}"

    def _player_leave_table(self, player):
        if player.name in self.left_players:
            return

        self.left_players.add(player.name)
        if self.hand_in_progress and not getattr(player, "folded", False):
            self.game.betting_engine.fold(player)

        player.chips = 0
        self.last_action_texts[player.name] = "LEFT TABLE"
        self.status_message = f"{player.name} left the table"

        curr_acting = self.game.betting_round.current_player()
        if curr_acting == player:
            self.game.betting_round.next_player()
            self._check_next_turn()

    def _set_slider_ratio(self, ratio):
        if self.bet_slider:
            val = int(self.bet_slider.min_val + ratio * (self.bet_slider.max_val - self.bet_slider.min_val))
            self.bet_slider.val = val

    def _toggle_hud(self):
        self.show_ai_hud = not self.show_ai_hud

    def _toggle_privacy(self):
        self.show_hole_cards = not self.show_hole_cards

    def _check_next_turn(self):
        """
        Manages turn progression & automatic board runouts when All-In occurs.
        Uses 750ms pacing delay between Flop, Turn, and River card dealing!
        """
        if not self.hand_in_progress:
            return

        now = pygame.time.get_ticks()

        # Check if everyone folded except 1 player
        active_non_folded = [p for p in self.players if not getattr(p, "folded", False) and p.name not in self.left_players]
        if len(active_non_folded) == 1:
            self.winner_player = active_non_folded[0]
            self.winner_player.chips += self.game.pot_manager.total_pot()
            self.game.pot_manager.reset()
            self.hand_in_progress = False
            self.is_showdown = False
            self.status_message = f"{self.winner_player.name} WON ${self.display_pot}! [SHOW CARDS] or [MUCK CARDS] • Press SPACE for Next Hand"
            return

        if self.game.betting_round.betting_complete():
            if self.ai_paused:
                return

            if now - self.last_ai_move_time < self.street_delay_ms:
                return

            comm = self.game.table.community_cards
            if len(comm) < 3:
                self.game.deal_flop()
                self.game.betting_round.reset()
                self.game.betting_round.start()
                self.status_message = "Flop Dealt"
                self.last_ai_move_time = now
                return
            elif len(comm) < 4:
                self.game.deal_turn()
                self.game.betting_round.reset()
                self.game.betting_round.start()
                self.status_message = "Turn Dealt"
                self.last_ai_move_time = now
                return
            elif len(comm) < 5:
                self.game.deal_river()
                self.game.betting_round.reset()
                self.game.betting_round.start()
                self.status_message = "River Dealt"
                self.last_ai_move_time = now
                return
            else:
                self.is_showdown = True
                self.game.showdown.resolve(self.players, self.game.table.community_cards, self.game.pot_manager)
                self.hand_in_progress = False
                self.status_message = "Showdown Complete! Press SPACE for Next Hand"
                return


        curr_p = self.game.betting_round.current_player()
        if curr_p and getattr(curr_p, "is_ai", False):
            if not self.ai_paused and (now - self.last_ai_move_time >= self.ai_delay_ms):
                self.last_ai_move_time = now
                self._execute_ai_turn(curr_p)

    def _execute_ai_turn(self, player):
        if player.name in self.left_players:
            self.game.betting_round.next_player()
            return

        if hasattr(player, "decide"):
            context = self.game.create_context(player)
            opponents = [p.name for p in self.players if p != player and not getattr(p, "folded", False)]
            opp_name = opponents[0] if opponents else None

            decision = player.decide(context, opponent_name=opp_name)
            self.current_ai_analysis = decision.get("analysis")

            action = decision.get("action")
            amount = decision.get("amount", 0)

            if action == Action.FOLD:
                self.game.betting_engine.fold(player)
                self.last_action_texts[player.name] = "FOLDED"
            elif action == Action.CHECK:
                self.game.betting_engine.check(player)
                self.last_action_texts[player.name] = "CHECK"
            elif action == Action.CALL:
                self.game.betting_engine.call(player)
                self.last_action_texts[player.name] = "CALL"
            elif action in (Action.BET, Action.RAISE, Action.ALL_IN):
                current_tb_bet = getattr(self.game.table, "current_bet", 0)
                if action == Action.ALL_IN or (amount and amount >= player.chips):
                    self.game.betting_engine.all_in(player)
                    self.last_action_texts[player.name] = "ALL-IN!"
                elif current_tb_bet > 0 or action == Action.RAISE:
                    raise_to = max(current_tb_bet + getattr(self.game.table, "big_blind", 20), amount or self.big_blind * 2)
                    try:
                        self.game.betting_engine.raise_bet(player, raise_to)
                        self.last_action_texts[player.name] = f"RAISE ${raise_to}"
                    except Exception:
                        self.game.betting_engine.all_in(player)
                        self.last_action_texts[player.name] = "ALL-IN!"
                else:
                    try:
                        self.game.betting_engine.bet(player, amount or self.big_blind * 2)
                        self.last_action_texts[player.name] = f"BET ${amount or self.big_blind * 2}"
                    except Exception:
                        self.game.betting_engine.all_in(player)
                        self.last_action_texts[player.name] = "ALL-IN!"

            for other in self.players:
                if other != player and hasattr(other, "record_opponent_action"):
                    other.record_opponent_action(player.name, action, getattr(player, "position", None), self.game.betting_round.street)

            act_name = action.name if hasattr(action, "name") else str(action)
            self.status_message = f"{player.name} chose {act_name.upper()}"
            self.game.betting_round.next_player()

    def _handle_human_action(self, action_type, amount=0):
        curr_p = self.game.betting_round.current_player()
        if not curr_p or getattr(curr_p, "is_ai", False):
            return

        if action_type == Action.FOLD:
            self.game.betting_engine.fold(curr_p)
            self.last_action_texts[curr_p.name] = "FOLDED"
        elif action_type == Action.CHECK:
            self.game.betting_engine.check(curr_p)
            self.last_action_texts[curr_p.name] = "CHECK"
        elif action_type == Action.CALL:
            tbl_bet = getattr(self.game.table, "current_bet", 0)
            p_bet = getattr(curr_p, "current_bet", 0)
            call_amt = tbl_bet - p_bet
            if call_amt <= 0:
                self.game.betting_engine.check(curr_p)
                self.last_action_texts[curr_p.name] = "CHECK"
            else:
                self.game.betting_engine.call(curr_p)
                self.last_action_texts[curr_p.name] = f"CALL ${call_amt}"
        elif action_type == Action.BET:
            current_tb_bet = getattr(self.game.table, "current_bet", 0)
            if amount >= curr_p.chips:
                self.game.betting_engine.all_in(curr_p)
                self.last_action_texts[curr_p.name] = "ALL-IN!"
            elif current_tb_bet > 0:
                raise_to = max(current_tb_bet + getattr(self.game.table, "big_blind", 20), amount)
                try:
                    self.game.betting_engine.raise_bet(curr_p, raise_to)
                    self.last_action_texts[curr_p.name] = f"RAISE ${raise_to}"
                except Exception:
                    self.game.betting_engine.all_in(curr_p)
                    self.last_action_texts[curr_p.name] = "ALL-IN!"
            else:
                try:
                    self.game.betting_engine.bet(curr_p, amount)
                    self.last_action_texts[curr_p.name] = f"BET ${amount}"
                except Exception:
                    self.game.betting_engine.all_in(curr_p)
                    self.last_action_texts[curr_p.name] = "ALL-IN!"

        for other in self.players:
            if other != curr_p and hasattr(other, "record_opponent_action"):
                other.record_opponent_action(curr_p.name, action_type, getattr(curr_p, "position", None), self.game.betting_round.street)

        act_name = action_type.name if hasattr(action_type, "name") else str(action_type)
        self.status_message = f"{curr_p.name} chose {act_name.upper()}"
        self.game.betting_round.next_player()
        self._check_next_turn()

    def _evaluate_made_hand(self, player):
        if not hasattr(player, "hand") or len(player.hand) < 2:
            return ""

        comm_cards = self.game.table.community_cards
        if len(comm_cards) < 3:
            c1, c2 = player.hand[0], player.hand[1]
            r1 = c1.rank.symbol if hasattr(c1.rank, "symbol") else str(c1.rank)
            r2 = c2.rank.symbol if hasattr(c2.rank, "symbol") else str(c2.rank)
            if r1 == r2:
                return f"Pocket Pair ({r1}s)"
            else:
                s1 = c1.numeric_rank if hasattr(c1, "numeric_rank") else 0
                s2 = c2.numeric_rank if hasattr(c2, "numeric_rank") else 0
                high_r = r1 if s1 >= s2 else r2
                return f"High Card ({high_r})"
        else:
            try:
                res = self.evaluator.evaluate(player.hand, comm_cards)
                return res.hand_name
            except Exception:
                return "High Card"

    def handle_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self._rebuild_layout()

        if self.help_modal.mode is not None:
            if self.help_modal.handle_event(event):
                return True

        if self.hud_toggle_btn.handle_event(event) or self.rankings_btn.handle_event(event) or self.tutorial_btn.handle_event(event) or self.lobby_btn.handle_event(event):
            return True

        if self.pause_ai_btn and self.pause_ai_btn.handle_event(event):
            return True

        # Handle post-hand SHOW CARDS / MUCK CARDS clicks
        if not self.hand_in_progress:
            if self.show_cards_btn and self.show_cards_btn.handle_event(event):
                return True
            if self.muck_cards_btn and self.muck_cards_btn.handle_event(event):
                return True

        curr_acting = self.game.betting_round.current_player_or_none()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            sw, sh = self.screen.get_size()
            table_w = int(sw * 0.66)
            table_h = int(sh * 0.44)
            table_x = (sw - table_w) // 2
            table_y = int(sh * 0.23)

            n_seats = len(self.players)
            cx_tab, cy_tab = sw // 2, table_y + table_h // 2
            rx, ry = table_w // 2 + 25, table_h // 2 + 20

            for i, player in enumerate(self.players):
                angle = (2 * math.pi * i / n_seats) + (math.pi / 2)
                px = int(cx_tab + rx * math.cos(angle))
                py = int(cy_tab + ry * math.sin(angle))
                seat_w, seat_h = int(sw * 0.122), int(sh * 0.082)
                rect = pygame.Rect(px - seat_w // 2, py - seat_h // 2, seat_w, seat_h)

                if self.hand_in_progress and player == curr_acting:
                    leave_btn_rect = pygame.Rect(rect.right - 22, rect.y + 2, 20, 20)
                    if leave_btn_rect.collidepoint(event.pos):
                        self._player_leave_table(player)
                        return True

                # Post-hand seat click: Toggle showing player's cards face up to flex or show bluff!
                if not self.hand_in_progress and rect.collidepoint(event.pos):
                    if player.name in self.user_showed_players:
                        self.user_showed_players.remove(player.name)
                        self.status_message = f"{player.name} Mucked Cards"
                    else:
                        self.user_showed_players.add(player.name)
                        self.status_message = f"{player.name} SHOWED CARDS! Press SPACE for Next Hand"
                    return True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self._toggle_hud()
                return True
            elif event.key == pygame.K_h:
                self._toggle_privacy()
                return True
            elif event.key == pygame.K_F1:
                self.help_modal.open_rankings()
                return True
            elif event.key == pygame.K_SPACE:
                if not self.hand_in_progress:
                    self._start_new_hand()
                    return True

        if curr_acting and not getattr(curr_acting, "is_ai", False) and self.hand_in_progress:
            self.bet_slider.handle_event(event)
            for btn in self.quick_bet_buttons:
                btn.handle_event(event)
            for btn in self.action_buttons:
                if btn.handle_event(event):
                    return True

        return False

    def draw(self):
        # Frame Pacing Check for AI Turns & Street Dealing
        if self.hand_in_progress:
            self._check_next_turn()

        self.screen.fill((11, 15, 25))
        sw, sh = self.screen.get_size()

        # Render Oval Felt Table (Positioned cleanly with 23% top padding)
        table_w = int(sw * 0.66)
        table_h = int(sh * 0.44)
        table_x = (sw - table_w) // 2
        table_y = int(sh * 0.23)
        table_rect = pygame.Rect(table_x, table_y, table_w, table_h)

        pygame.draw.ellipse(self.screen, (67, 40, 24), table_rect.inflate(28, 28))
        pygame.draw.ellipse(self.screen, (217, 119, 6), table_rect.inflate(6, 6))
        pygame.draw.ellipse(self.screen, (6, 95, 70), table_rect)
        pygame.draw.ellipse(self.screen, (16, 185, 129), table_rect, 2)

        # Total Pot Badge (Remembers final winning pot during Showdown)
        font_pot = pygame.font.SysFont("arial", max(13, int(sh * 0.026)), bold=True)
        current_pot = self.game.pot_manager.total_pot()
        if current_pot > 0:
            self.display_pot = current_pot

        pot_surf = font_pot.render(f"TOTAL POT: ${self.display_pot}", True, (254, 240, 138))
        pot_rect = pot_surf.get_rect(center=(sw // 2, table_y + int(table_h * 0.35)))
        pygame.draw.rect(self.screen, (15, 23, 42), pot_rect.inflate(20, 10), border_radius=10)
        pygame.draw.rect(self.screen, (234, 179, 8), pot_rect.inflate(20, 10), 2, border_radius=10)
        self.screen.blit(pot_surf, pot_rect)

        # Community Cards (FACE-UP for ALL)
        comm_cards = self.game.table.community_cards
        card_w, card_h = int(sw * 0.050), int(sh * 0.115)
        start_cx = sw // 2 - int(2.5 * card_w)
        cy = table_y + int(table_h * 0.42)

        for i in range(5):
            cx = start_cx + i * (card_w + 8)
            if i < len(comm_cards):
                card = comm_cards[i]
                c_surf = card_renderer.get_card_surface(card.rank, card.suit, card_w, card_h, face_down=False)
            else:
                c_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
                pygame.draw.rect(c_surf, (15, 23, 42, 160), (0, 0, card_w, card_h), border_radius=6)
                pygame.draw.rect(c_surf, (71, 85, 105), (0, 0, card_w, card_h), 1, border_radius=6)
            self.screen.blit(c_surf, (cx, cy))

        # Render Seats Dynamically Around Table Oval
        curr_acting = self.game.betting_round.current_player_or_none()
        n_seats = len(self.players)
        cx_tab, cy_tab = sw // 2, table_y + table_h // 2
        rx, ry = table_w // 2 + 25, table_h // 2 + 20

        for i, player in enumerate(self.players):
            angle = (2 * math.pi * i / n_seats) + (math.pi / 2)
            px = int(cx_tab + rx * math.cos(angle))
            py = int(cy_tab + ry * math.sin(angle))

            is_acting = (curr_acting == player and self.hand_in_progress)
            self._draw_player_seat(player, px, py, is_acting, curr_acting, card_w, card_h, cx_tab, cy_tab, table_w)

        # Top Navigation Bar Buttons (Rendered at top 2% of screen)
        self.hud_toggle_btn.draw(self.screen)
        self.rankings_btn.draw(self.screen)
        self.tutorial_btn.draw(self.screen)
        self.lobby_btn.draw(self.screen)
        if self.pause_ai_btn:
            self.pause_ai_btn.draw(self.screen)

        # Status Message (Centered below nav buttons, never overlaps)
        font_status = pygame.font.SysFont("arial", max(12, int(sh * 0.022)), bold=True)
        stat_surf = font_status.render(self.status_message, True, (241, 245, 249))
        self.screen.blit(stat_surf, (sw // 2 - stat_surf.get_width() // 2, int(sh * 0.06)))


        # Draw Action Bar when Human turn
        if curr_acting and not getattr(curr_acting, "is_ai", False) and self.hand_in_progress:
            self._update_action_button_labels()
            self.bet_slider.draw(self.screen)
            for btn in self.quick_bet_buttons + self.action_buttons:
                btn.draw(self.screen)

        # Draw Post-Hand SHOW CARDS / MUCK CARDS Buttons (only for human fold-winners, AI auto-reveals)
        if not self.hand_in_progress and self.winner_player and not getattr(self.winner_player, "is_ai", False):
            self.show_cards_btn.draw(self.screen)
            self.muck_cards_btn.draw(self.screen)

        # Draw "Click seat to show/muck" hint when hand ended (any mode with humans)
        if not self.hand_in_progress and not self.is_all_ai:
            hint_font = pygame.font.SysFont("arial", max(10, int(sh * 0.018)))
            hint_surf = hint_font.render("Click any seat to SHOW / MUCK cards", True, (148, 163, 184))
            self.screen.blit(hint_surf, (sw // 2 - hint_surf.get_width() // 2, int(sh * 0.82)))


        # Draw AI Brain HUD Panel
        if self.show_ai_hud:
            self._draw_ai_hud()

        # Draw Help / Tutorial Overlay Modal if active
        self.help_modal.draw()

    def _draw_player_seat(self, player, x, y, is_acting, curr_acting, card_w, card_h, cx_tab, cy_tab, table_w):
        sw, sh = self.screen.get_size()
        seat_w, seat_h = int(sw * 0.122), int(sh * 0.082)
        rect = pygame.Rect(x - seat_w // 2, y - seat_h // 2, seat_w, seat_h)

        is_human = not getattr(player, "is_ai", False)
        has_left = player.name in self.left_players
        bg_color = (15, 23, 42) if has_left else ((30, 41, 59) if is_human else (15, 23, 42))
        border_color = (250, 204, 21) if is_acting else ((59, 130, 246) if is_human else (168, 85, 247))

        if is_acting:
            pygame.draw.rect(self.screen, (250, 204, 21, 100), rect.inflate(10, 10), border_radius=12)

        pygame.draw.rect(self.screen, bg_color, rect, border_radius=10)
        pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=10)

        font = pygame.font.SysFont("arial", max(10, int(seat_h * 0.28)), bold=True)
        name_surf = font.render(player.name, True, (241, 245, 249) if not has_left else (148, 163, 184))
        chips_surf = font.render(f"${player.chips}", True, (52, 211, 153) if not has_left else (148, 163, 184))

        self.screen.blit(name_surf, (rect.x + 10, rect.y + 4))
        self.screen.blit(chips_surf, (rect.x + 10, rect.y + rect.height // 2))

        if not has_left and player == curr_acting and self.hand_in_progress:
            leave_btn_rect = pygame.Rect(rect.right - 22, rect.y + 2, 20, 20)
            pygame.draw.rect(self.screen, (220, 38, 38), leave_btn_rect, border_radius=4)
            font_x = pygame.font.SysFont("arial", 12, bold=True)
            x_surf = font_x.render("X", True, (255, 255, 255))
            self.screen.blit(x_surf, (leave_btn_rect.x + 5, leave_btn_rect.y + 2))

        # Action Banner
        if player.name in self.last_action_texts:
            act_txt = self.last_action_texts[player.name]
            font_act = pygame.font.SysFont("arial", max(9, int(seat_h * 0.24)), bold=True)
            act_surf = font_act.render(act_txt, True, (254, 240, 138) if "BET" in act_txt else (226, 232, 240))
            self.screen.blit(act_surf, (rect.x + 10, rect.bottom - 16))

        # Role Badges (Dealer D, Small Blind SB, Big Blind BB)
        if not has_left:
            d_font = pygame.font.SysFont("arial", max(9, int(seat_h * 0.26)), bold=True)
            if player.has_role(PlayerRole.DEALER):
                d_surf = d_font.render("D", True, (255, 255, 255))
                pygame.draw.circle(self.screen, (220, 38, 38), (rect.right - 14, rect.bottom - 14), 11)
                self.screen.blit(d_surf, (rect.right - 18, rect.bottom - 21))
            elif player.has_role(PlayerRole.SMALL_BLIND):
                sb_surf = d_font.render("SB", True, (255, 255, 255))
                pygame.draw.circle(self.screen, (37, 99, 235), (rect.right - 14, rect.bottom - 14), 11)
                self.screen.blit(sb_surf, (rect.right - 21, rect.bottom - 21))
            elif player.has_role(PlayerRole.BIG_BLIND):
                bb_surf = d_font.render("BB", True, (255, 255, 255))
                pygame.draw.circle(self.screen, (147, 51, 234), (rect.right - 14, rect.bottom - 14), 11)
                self.screen.blit(bb_surf, (rect.right - 21, rect.bottom - 21))

        # Smart 4-Quadrant Hole Cards Radial Placement
        if hasattr(player, "hand") and player.hand and not has_left:
            c1, c2 = player.hand[0], player.hand[1]

            is_active_human_turn = (curr_acting == player and is_human and self.show_hole_cards)
            is_winner_show = (self.winner_player == player and self.show_winner_cards)
            is_user_show = (player.name in self.user_showed_players)

            # AI players ALWAYS reveal cards face-up at round end (won by fold, folded early, or showdown)
            is_ai_round_end_reveal = (not self.hand_in_progress and not is_human)

            show_face_up = self.is_showdown or self.is_all_ai or is_active_human_turn or is_winner_show or is_user_show or is_ai_round_end_reveal


            cw, ch = card_w * 0.72, card_h * 0.72

            dx = x - cx_tab
            dy = y - cy_tab

            # 1. TOP CENTER SEATS: Render cards BELOW seat box (inside felt, avoids status text overlap)
            if abs(dx) < int(table_w * 0.28) and dy < 0:
                card_x1 = rect.centerx - int(cw * 0.8)
                card_x2 = card_x1 + int(cw * 0.6)
                card_y = rect.bottom + 4
                banner_y = rect.top - 14


            # 2. BOTTOM CENTER SEATS: Render cards BELOW seat box
            elif abs(dx) < int(table_w * 0.28) and dy >= 0:
                card_x1 = rect.centerx - int(cw * 0.8)
                card_x2 = card_x1 + int(cw * 0.6)
                card_y = rect.bottom + 4
                banner_y = card_y + int(ch) + 12

            # 3. LEFT SIDE SEATS: Render cards RIGHT of seat box inside left felt
            elif dx < 0:
                card_x1 = rect.right + 6
                card_x2 = card_x1 + int(cw * 0.55)
                card_y = rect.centery - int(ch) // 2
                banner_y = card_y - 14

            # 4. RIGHT SIDE SEATS: Render cards LEFT of seat box inside right felt
            else:
                card_x1 = rect.left - int(cw * 1.45)
                card_x2 = card_x1 + int(cw * 0.55)
                card_y = rect.centery - int(ch) // 2
                banner_y = card_y - 14

            surf1 = card_renderer.get_card_surface(c1.rank, c1.suit, cw, ch, face_down=not show_face_up)
            surf2 = card_renderer.get_card_surface(c2.rank, c2.suit, cw, ch, face_down=not show_face_up)

            self.screen.blit(surf1, (card_x1, card_y))
            self.screen.blit(surf2, (card_x2, card_y))

            # Made Hand Banner (Pre-Flop & Post-Flop)
            if show_face_up:
                if is_winner_show:
                    banner_label = "SHOWED CARDS (BLUFF!)"
                elif is_user_show:
                    banner_label = "SHOWED HAND"
                else:
                    hand_name = self._evaluate_made_hand(player)
                    banner_label = f"HAND: {hand_name}" if hand_name else ""

                if banner_label:
                    font_banner = pygame.font.SysFont("arial", max(9, int(seat_h * 0.22)), bold=True)
                    b_surf = font_banner.render(banner_label, True, (254, 240, 138))

                    b_rect = b_surf.get_rect(center=(card_x1 + int(cw * 0.8), banner_y))
                    pygame.draw.rect(self.screen, (15, 23, 42, 220), b_rect.inflate(12, 6), border_radius=6)
                    pygame.draw.rect(self.screen, (234, 179, 8), b_rect.inflate(12, 6), 1, border_radius=6)
                    self.screen.blit(b_surf, b_rect)

    def _draw_ai_hud(self):
        sw, sh = self.screen.get_size()
        panel_w = int(sw * 0.23)
        panel_h = int(sh * 0.44)
        panel_x = sw - panel_w - int(sw * 0.02)
        panel_y = int(sh * 0.02)

        rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        pygame.draw.rect(self.screen, (15, 23, 42), rect, border_radius=10)
        pygame.draw.rect(self.screen, (59, 130, 246), rect, 2, border_radius=10)

        font_h = pygame.font.SysFont("arial", max(12, int(panel_h * 0.06)), bold=True)
        title_surf = font_h.render("LIVE AI BRAIN HUD", True, (96, 165, 250))
        self.screen.blit(title_surf, (panel_x + 12, panel_y + 10))

        font_body = pygame.font.SysFont("arial", max(10, int(panel_h * 0.045)))
        y_off = panel_y + 40

        if self.current_ai_analysis:
            eq = self.current_ai_analysis.get("equity", 0)
            st = self.current_ai_analysis.get("strength", 0)
            reason = self.current_ai_analysis.get("reason", "standard_decision")
            opp = self.current_ai_analysis.get("opponent") or {}

            lines = [
                f"Win Equity: {eq}%",
                f"Hand Strength: {st}/100",
                f"Opponent Type: {opp.get('type', 'unknown')}",
                f"Threat Level: {opp.get('threat_level', 5)}/10",
                f"Reasoning: {reason}",
            ]
        else:
            lines = [
                "Waiting for AI Decision...",
                "Press [TAB] to toggle HUD",
                "Press [H] for Hole Privacy",
                "Press [F1] for Hand Rankings"
            ]

        for line in lines:
            surf = font_body.render(line, True, (226, 232, 240))
            self.screen.blit(surf, (panel_x + 12, y_off))
            y_off += int(panel_h * 0.07)
