import sys
import os

# Ensure project root directory is in sys.path for Linux / Streamlit Cloud deployment
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Case-sensitivity helper for Linux environments (AI vs ai)
try:
    import AI
    sys.modules['ai'] = AI
except ImportError:
    try:
        import ai
        sys.modules['AI'] = ai
    except ImportError:
        pass

import streamlit as st
import time
import random
import threading

@st.cache_resource
def get_global_rooms():
    return {}

def cleanup_stale_rooms():
    rooms = get_global_rooms()
    now = time.time()
    stale_codes = [code for code, r in rooms.items() if now - r.get("created_at", now) > 3600]
    for code in stale_codes:
        rooms.pop(code, None)

def get_room(room_code):
    if not room_code:
        return None
    cleanup_stale_rooms()
    return get_global_rooms().get(room_code)

from engine.game import Game
from models.action import Action
from models.card import Card
from models.street import Street
from engine.game_state import GameState
from AI.bot_player import BotPlayer
from AI.difficulty import Difficulty
from AI.strategy import Strategy
from AI.equity import EquityCalculator
from AI.game_context import GameContext
from engine.evaluator import HandEvaluator
from integration.ai_player import AIPlayer
from models.player import Player

# Page Setup
st.set_page_config(
    page_title="Texas Hold'em Poker AI | Web Game",
    page_icon="♠️",
    layout="wide"
)

# Custom High-End Web Aesthetics matching game_screen.py and lobby.py
st.markdown("""
<style>
    .main { background-color: #0b0f19; padding: 0.5rem 1rem !important; }
    
    .poker-title {
        text-align: center;
        color: #f59e0b;
        font-size: 1.5rem;
        font-weight: 900;
        letter-spacing: 1px;
        text-transform: uppercase;
        text-shadow: 0px 2px 10px rgba(245, 158, 11, 0.4);
        margin: 0 0 2px 0;
    }
    
    /* Felt Oval Table Container (Compact) */
    .felt-table {
        background: radial-gradient(ellipse at center, #10b981 0%, #0b4f37 70%, #0f172a 100%);
        border: 6px solid #1e293b;
        outline: 2px solid #f59e0b;
        border-radius: 40px;
        padding: 12px 15px;
        box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.8), inset 0px 0px 20px rgba(0,0,0,0.5);
        margin: 6px auto 10px auto;
        text-align: center;
        color: white;
    }

    /* Pot Display (Compact) */
    .pot-badge {
        font-size: 1.15rem;
        font-weight: 900;
        color: #fef08a;
        background: rgba(15, 23, 42, 0.95);
        padding: 4px 18px;
        border-radius: 20px;
        border: 1.5px solid #f59e0b;
        display: inline-block;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
        margin-bottom: 6px;
    }
    
    /* Card Badges (Compact) */
    .card-badge {
        display: inline-block;
        background-color: #ffffff;
        color: #0f172a;
        font-weight: 900;
        font-size: 1.1rem;
        padding: 5px 10px;
        border-radius: 6px;
        margin: 2px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
    }
    .card-red { color: #ef4444 !important; }
    .card-black { color: #0f172a !important; }
    .card-back {
        background: linear-gradient(135deg, #1e293b, #0f172a) !important;
        color: #f59e0b !important;
        border: 1.5px solid #f59e0b;
    }

    /* Player Seats (Compact) */
    .player-seat {
        background: rgba(15, 23, 42, 0.92);
        border: 2px solid #334155;
        border-radius: 12px;
        padding: 8px 6px;
        text-align: center;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4);
    }
    .active-seat-glow {
        border-color: #10b981 !important;
        box-shadow: 0 0 15px #10b981 !important;
    }
    .winner-seat-glow {
        border: 2px solid #f59e0b !important;
        box-shadow: 0 0 20px #f59e0b !important;
        background: rgba(245, 158, 11, 0.15) !important;
    }
    .winner-badge {
        background-color: #f59e0b;
        color: #0f172a;
        font-weight: 900;
        font-size: 0.75rem;
        padding: 2px 6px;
        border-radius: 8px;
        display: inline-block;
        margin-bottom: 2px;
    }
    .dealer-badge {
        background-color: #f59e0b;
        color: #0f172a;
        font-weight: 900;
        font-size: 0.7rem;
        padding: 1px 5px;
        border-radius: 50%;
        display: inline-block;
        margin-left: 4px;
    }
    
    /* AI Brain HUD Box */
    .hud-box {
        background: rgba(30, 41, 59, 0.95);
        border: 1.5px solid #6366f1;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }

    /* Winner Banner Box */
    .winner-banner-box {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.25), rgba(16, 185, 129, 0.25));
        border: 2px solid #f59e0b;
        border-radius: 10px;
        padding: 8px;
        text-align: center;
        margin-top: 6px;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
    }

    /* Room Code Box */
    .room-box {
        background: rgba(15, 23, 42, 0.95);
        border: 2px solid #10b981;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

def render_card_html(card):
    if not card:
        return '<span class="card-badge card-back">🂠</span>'
    if hasattr(card, "rank") and hasattr(card, "suit"):
        rank_str = card.rank.symbol if hasattr(card.rank, "symbol") else str(card.rank)
        suit_sym = card.suit.symbol if hasattr(card.suit, "symbol") else str(card.suit)
        is_red = getattr(card, "is_red", False)
        cls = "card-red" if is_red else "card-black"
        return f'<span class="card-badge {cls}">{rank_str}{suit_sym}</span>'
    s = str(card).strip()
    return f'<span class="card-badge card-black">{s}</span>'

def get_action_badge_html(player, is_winner):
    if is_winner:
        return ''
    
    last_act = getattr(player, "last_action", None)
    if not last_act and getattr(player, "folded", False):
        last_act = Action.FOLD
        
    if not last_act:
        return '<div style="height: 22px;"></div>'
        
    act_name = last_act.name if hasattr(last_act, "name") else str(last_act)
    
    if act_name == "FOLD":
        bg_color, text_color = "#ef4444", "#ffffff"
    elif act_name == "CHECK":
        bg_color, text_color = "#3b82f6", "#ffffff"
    elif act_name == "CALL":
        bg_color, text_color = "#10b981", "#ffffff"
    elif act_name in ("BET", "RAISE"):
        bg_color, text_color = "#f59e0b", "#0f172a"
    elif act_name == "ALL_IN":
        bg_color, text_color = "#dc2626", "#fef08a"
    else:
        bg_color, text_color = "#64748b", "#ffffff"

    return f'<div style="background-color:{bg_color}; color:{text_color}; font-weight:800; font-size:0.75rem; padding:3px 10px; border-radius:12px; display:inline-block; margin-top:4px; letter-spacing:1px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">{act_name}</div>'

def get_player_hand_name(player, community_cards):
    if not player or not hasattr(player, "hand") or len(player.hand) < 2:
        return ""
    
    if len(community_cards) < 3:
        c1, c2 = player.hand[0], player.hand[1]
        r1 = c1.rank.symbol if hasattr(c1.rank, "symbol") else str(c1.rank)
        r2 = c2.rank.symbol if hasattr(c2.rank, "symbol") else str(c2.rank)
        if r1 == r2:
            return f"Pair ({r1}s)"
        else:
            s1 = c1.numeric_rank if hasattr(c1, "numeric_rank") else 0
            s2 = c2.numeric_rank if hasattr(c2, "numeric_rank") else 0
            high_r = r1 if s1 >= s2 else r2
            return f"High Card ({high_r})"
    else:
        try:
            res = evaluator.evaluate(player.hand, community_cards)
            return res.hand_name
        except Exception:
            return "High Card"

def check_and_advance_street(game):
    if not game or game.state in (GameState.SHOWDOWN, GameState.HAND_COMPLETE):
        return
    
    active_non_folded = [p for p in game.players if not getattr(p, "folded", False)]
    
    # 1. Everyone folded except 1 player
    if len(active_non_folded) <= 1:
        if active_non_folded:
            winner = active_non_folded[0]
            pot_val = game.pot_manager.total_pot()
            winner.chips += pot_val
            game.pot_manager.reset()
            game.state = GameState.HAND_COMPLETE
            st.session_state.winners_list = [winner.name]
            st.session_state.winner_banner_text = f"🏆 WINNER: {winner.name} won ${pot_val} (Everyone Folded)!"
            st.session_state.log_messages.append(f"🏆 {winner.name} won ${pot_val} (Everyone Folded)!")
        return

    # 2. Advance exactly ONE street per call so community cards render visually
    #    step-by-step between frames (Flop → Turn → River → Showdown).
    if not game.betting_round.betting_complete():
        return

    comm = game.table.community_cards
    if len(comm) < 3:
        game.deal_flop()
        game.betting_round.reset()
        game.betting_round.set_street(Street.FLOP)
        game.betting_round.start()
        st.session_state.log_messages.append("🎴 Flop Dealt")
    elif len(comm) < 4:
        game.deal_turn()
        game.betting_round.reset()
        game.betting_round.set_street(Street.TURN)
        game.betting_round.start()
        st.session_state.log_messages.append("🎴 Turn Dealt")
    elif len(comm) < 5:
        game.deal_river()
        game.betting_round.reset()
        game.betting_round.set_street(Street.RIVER)
        game.betting_round.start()
        st.session_state.log_messages.append("🎴 River Dealt")
    else:
        # SHOWDOWN
        game.state = GameState.SHOWDOWN
        pot_val = game.pot_manager.total_pot()
        res = game.showdown.resolve(game.players, game.table.community_cards, game.pot_manager)
        
        pots = res.get("pots", []) if isinstance(res, dict) else []
        results_dict = res.get("results", {}) if isinstance(res, dict) else {}
        all_winners = res.get("winners", []) if isinstance(res, dict) else []
        
        main_pot_winners = []
        if pots:
            biggest_pot_info = max(pots, key=lambda p_info: getattr(p_info.get("pot"), "amount", 0), default=pots[0])
            main_pot_winners = biggest_pot_info.get("winners", [])
        
        if not main_pot_winners:
            main_pot_winners = all_winners

        unique_winners = []
        seen = set()
        for w in main_pot_winners:
            w_name = w.name if hasattr(w, "name") else str(w)
            if w_name not in seen:
                seen.add(w_name)
                unique_winners.append(w)

        if unique_winners:
            st.session_state.winners_list = [w.name if hasattr(w, "name") else str(w) for w in unique_winners]
            w_names = ", ".join(st.session_state.winners_list)
            
            w_res = results_dict.get(unique_winners[0])
            hand_desc = f" ({w_res.hand_name})" if w_res and hasattr(w_res, "hand_name") else ""
            
            if len(unique_winners) > 1:
                banner = f"🤝 SPLIT POT: {w_names} tied and split ${pot_val}{hand_desc}!"
            else:
                banner = f"🏆 WINNER: {w_names} won ${pot_val}{hand_desc}!"
            
            st.session_state.winner_banner_text = banner
            st.session_state.log_messages.append(banner)

def execute_player_action(game, player, action, amount=0):
    r_code = st.session_state.get("room_code", "")
    rm = get_room(r_code)
    
    def _act_body():
        if not player or not hasattr(player, "can_act") or not player.can_act():
            return
        
        current_high = getattr(game.table, "current_bet", 0)
        
        try:
            if action == Action.FOLD:
                game.betting_engine.fold(player)
            elif action == Action.CHECK:
                try:
                    game.betting_engine.check(player)
                except Exception:
                    game.betting_engine.fold(player)
            elif action == Action.CALL:
                try:
                    game.betting_engine.call(player)
                except Exception:
                    game.betting_engine.fold(player)
            elif action in (Action.BET, Action.RAISE):
                if amount >= player.chips:
                    game.betting_engine.all_in(player)
                elif current_high > 0 or action == Action.RAISE:
                    try:
                        game.betting_engine.raise_bet(player, amount)
                    except Exception:
                        game.betting_engine.all_in(player)
                else:
                    try:
                        game.betting_engine.bet(player, amount)
                    except Exception:
                        game.betting_engine.all_in(player)
            elif action == Action.ALL_IN:
                game.betting_engine.all_in(player)
        except Exception:
            try:
                game.betting_engine.fold(player)
            except Exception:
                pass

        game.betting_round.next_player()
        check_and_advance_street(game)

    if rm and "lock" in rm:
        with rm["lock"]:
            _act_body()
            rm["log_messages"] = st.session_state.log_messages
            rm["winners_list"] = st.session_state.winners_list
            rm["winner_banner_text"] = st.session_state.winner_banner_text
    else:
        _act_body()

def start_game_hand(game_obj):
    st.session_state.winners_list = []
    st.session_state.winner_banner_text = ""
    
    # Tournament Mode: Double blinds every 5 hands
    if st.session_state.get("tournament_mode", False) and st.session_state.hand_count > 1 and (st.session_state.hand_count - 1) % 5 == 0:
        game_obj.table.small_blind *= 2
        game_obj.table.big_blind *= 2
        st.session_state.log_messages.append(f"🔥 TOURNAMENT BLINDS INCREASED: ${game_obj.table.small_blind}/${game_obj.table.big_blind}!")

    game_obj.start_hand()
    game_obj.betting_round.set_street(Street.PRE_FLOP)
    game_obj.betting_round.start()
    
    r_code = st.session_state.get("room_code", "")
    rm = get_room(r_code)
    if rm:
        rm["winners_list"] = []
        rm["winner_banner_text"] = ""
        rm["log_messages"] = st.session_state.log_messages

# State Setup
if "view" not in st.session_state:
    st.session_state.view = "lobby"
    st.session_state.num_seats = 2
    st.session_state.starting_chips = 1000
    st.session_state.small_blind = 10
    st.session_state.big_blind = 20
    st.session_state.auto_rebuy = True
    st.session_state.tournament_mode = False
    st.session_state.ai_paused = False
    st.session_state.show_hud = True
    st.session_state.show_rankings = False
    st.session_state.show_cards_showdown = True
    st.session_state.room_code = ""
    st.session_state.my_player_name = "You (Human)"
    st.session_state.log_messages = []
    st.session_state.chat_messages = []
    st.session_state.hand_count = 1
    st.session_state.winners_list = []
    st.session_state.winner_banner_text = ""
    
    st.session_state.seat_configs = [
        {"name": "You (Human)", "is_ai": False, "difficulty": "HARD", "strategy": "BALANCED"},
        {"name": "Player 2 (Human)", "is_ai": False, "difficulty": "HARD", "strategy": "BALANCED"},
        {"name": "Bot Alpha", "is_ai": True, "difficulty": "HARD", "strategy": "TIGHT_AGGRESSIVE"},
        {"name": "Bot Bravo", "is_ai": True, "difficulty": "MEDIUM", "strategy": "LOOSE_AGGRESSIVE"},
        {"name": "Bot Charlie", "is_ai": True, "difficulty": "EASY", "strategy": "CALLING_STATION"},
        {"name": "Bot Delta", "is_ai": True, "difficulty": "EXPERT", "strategy": "TIGHT_PASSIVE"},
        {"name": "Bot Echo", "is_ai": True, "difficulty": "MEDIUM", "strategy": "BALANCED"},
        {"name": "Bot Foxtrot", "is_ai": True, "difficulty": "HARD", "strategy": "BALANCED"},
        {"name": "Bot Golf", "is_ai": True, "difficulty": "EASY", "strategy": "CALLING_STATION"}
    ]

equity_calc = EquityCalculator()
evaluator = HandEvaluator()

# ==============================================================================
# LOBBY VIEW
# ==============================================================================
if st.session_state.view == "lobby":
    st.markdown('<div class="poker-title">♠️ TEXAS HOLD\'EM POKER LOBBY ♠️</div>', unsafe_allow_html=True)
    st.caption("<div style='text-align:center;'>Select Game Mode, Configure Seats, AI Personalities, Blinds & Multi-Player Rooms</div>", unsafe_allow_html=True)
    st.markdown("---")

    lobby_tab1, lobby_tab2, lobby_tab3 = st.tabs([
        "🎮 LOCAL GAME / BOT BATTLE",
        "🌐 HOST MULTIPLAYER ROOM",
        "🚪 JOIN MULTIPLAYER ROOM"
    ])

    # --------------------------------------------------------------------------
    # TAB 1: LOCAL GAME & BOT BATTLE SETUP
    # --------------------------------------------------------------------------
    with lobby_tab1:
        st.markdown("##### ⚡ Quick Table Size Presets:")
        q1, q2, q3, q4 = st.columns(4)
        with q1:
            if st.button("👥 2 Players (Heads Up)", use_container_width=True):
                st.session_state.num_seats = 2
                st.session_state.num_seats_input = 2
                st.rerun()
        with q2:
            if st.button("👨‍👩‍👧‍👦 4 Players", use_container_width=True):
                st.session_state.num_seats = 4
                st.session_state.num_seats_input = 4
                st.rerun()
        with q3:
            if st.button("♠️ 6 Players (6-Max)", use_container_width=True):
                st.session_state.num_seats = 6
                st.session_state.num_seats_input = 6
                st.rerun()
        with q4:
            if st.button("🏟️ 9 Players (Full Ring)", use_container_width=True):
                st.session_state.num_seats = 9
                st.session_state.num_seats_input = 9
                st.rerun()

        st.markdown("---")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if "num_seats_input" not in st.session_state:
                st.session_state.num_seats_input = st.session_state.num_seats

            num_s = st.number_input("Number of Seats (2 to 9)", min_value=2, max_value=9, step=1, key="num_seats_input")
            st.session_state.num_seats = int(num_s)
        with c2:
            st.session_state.starting_chips = st.select_slider("Starting Stack ($)", options=[500, 1000, 2000, 5000, 10000], value=st.session_state.starting_chips)
        with c3:
            b_choice = st.selectbox("Blinds ($SB / $BB)", options=["$10 / $20", "$25 / $50", "$50 / $100"])
            st.session_state.small_blind, st.session_state.big_blind = (10, 20) if "$10" in b_choice else ((25, 50) if "$25" in b_choice else (50, 100))
        with c4:
            st.session_state.auto_rebuy = st.checkbox("🔄 Auto-Rebuy When Broke", value=st.session_state.auto_rebuy)

        st.markdown(f"### 🪑 Configuring {st.session_state.num_seats} Seats")

        while len(st.session_state.seat_configs) < st.session_state.num_seats:
            idx = len(st.session_state.seat_configs) + 1
            st.session_state.seat_configs.append({"name": f"Bot {idx}", "is_ai": True, "difficulty": "MEDIUM", "strategy": "BALANCED"})

        cols_per_row = 3
        active_seats = st.session_state.seat_configs[:st.session_state.num_seats]
        for i in range(0, len(active_seats), cols_per_row):
            row_cols = st.columns(min(cols_per_row, len(active_seats) - i))
            for j, col in enumerate(row_cols):
                idx = i + j
                cfg = active_seats[idx]
                with col:
                    st.markdown(f"#### Seat #{idx+1}")
                    cfg["name"] = st.text_input("Player Name", value=cfg["name"], key=f"s_name_{idx}")
                    p_type = st.radio("Player Type", ["HUMAN", "AI BOT"], index=1 if cfg["is_ai"] else 0, key=f"s_type_{idx}", horizontal=True)
                    cfg["is_ai"] = (p_type == "AI BOT")
                    
                    if cfg["is_ai"]:
                        cfg["difficulty"] = st.selectbox("AI Difficulty", ["EASY", "MEDIUM", "HARD", "EXPERT"], index=["EASY", "MEDIUM", "HARD", "EXPERT"].index(cfg.get("difficulty", "MEDIUM")), key=f"s_diff_{idx}")
                        cfg["strategy"] = st.selectbox("Playstyle", ["BALANCED", "TIGHT_AGGRESSIVE", "LOOSE_AGGRESSIVE", "TIGHT_PASSIVE", "CALLING_STATION"], index=0, key=f"s_strat_{idx}")
                    st.markdown("---")

        if st.button("🚀 START LOCAL POKER GAME", use_container_width=True):
            st.session_state.room_code = ""
            st.session_state.my_player_name = active_seats[0]["name"]
            
            player_objs = []
            for i in range(st.session_state.num_seats):
                cfg = active_seats[i]
                if not cfg["is_ai"]:
                    player_objs.append(Player(name=cfg["name"], chips=st.session_state.starting_chips, is_ai=False))
                else:
                    d = getattr(Difficulty, cfg["difficulty"])
                    s = getattr(Strategy, cfg["strategy"])
                    bot = BotPlayer(name=cfg["name"], difficulty=d, strategy=s)
                    player_objs.append(AIPlayer(name=cfg["name"], bot=bot, chips=st.session_state.starting_chips))

            game_obj = Game(players=player_objs)
            game_obj.table.small_blind = st.session_state.small_blind
            game_obj.table.big_blind = st.session_state.big_blind
            start_game_hand(game_obj)
            
            st.session_state.game = game_obj
            st.session_state.view = "game"
            st.session_state.log_messages = [f"Game started with {st.session_state.num_seats} seats! Hand #1."]
            st.rerun()

    # --------------------------------------------------------------------------
    # TAB 2: HOST MULTIPLAYER ROOM
    # --------------------------------------------------------------------------
    with lobby_tab2:
        st.markdown("### 🌐 Host an Online Room")
        st.caption("Create a multiplayer table and share your Room Code with friends so they can join your room!")
        
        if not st.session_state.room_code:
            rand_code = "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=4))
            st.session_state.room_code = f"PKR-{rand_code}"

        st.markdown(f"""<div class="room-box">
<h3 style="color:#10b981; margin:0;">YOUR HOST ROOM CODE:</h3>
<h1 style="color:#f59e0b; font-size:3.5rem; letter-spacing:4px; margin:10px 0;">{st.session_state.room_code}</h1>
<p style="color:#cbd5e1;">Status: <b style="color:#10b981;">Online & Ready to Host</b></p>
</div>""", unsafe_allow_html=True)

        if st.button("🎲 Generate New Random Code"):
            rand_code = "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=4))
            st.session_state.room_code = f"PKR-{rand_code}"
            st.rerun()

        host_name_in = st.text_input("Your Host Name:", value="Host (You)", key="host_name_input")

        if st.button("🚀 LAUNCH HOSTED ROOM TABLE", use_container_width=True):
            code = st.session_state.room_code
            st.session_state.my_player_name = host_name_in.strip() or "Host (You)"
            
            rooms = get_global_rooms()
            host_p = Player(name=st.session_state.my_player_name, chips=st.session_state.starting_chips, is_ai=False)
            
            rooms[code] = {
                "code": code,
                "host_name": st.session_state.my_player_name,
                "lock": threading.Lock(),
                "starting_chips": st.session_state.starting_chips,
                "small_blind": st.session_state.small_blind,
                "big_blind": st.session_state.big_blind,
                "players": [host_p],
                "game": None,
                "status": "WAITING",
                "created_at": time.time(),
                "winners_list": [],
                "winner_banner_text": "",
                "log_messages": [f"Room {code} created by {st.session_state.my_player_name}. Waiting for players to join..."],
                "hand_count": 1,
            }
            
            st.session_state.view = "waiting_room"
            st.rerun()

    # --------------------------------------------------------------------------
    # TAB 3: JOIN MULTIPLAYER ROOM
    # --------------------------------------------------------------------------
    with lobby_tab3:
        st.markdown("### 🚪 Join a Multiplayer Room")
        st.caption("Enter the Room Code provided by the Room Host:")
        
        join_code_input = st.text_input("Enter Room Code (e.g. 4892 or PKR-4892):", placeholder="e.g. 4892")
        join_name_input = st.text_input("Your Player Name:", value="Guest (You)")
        
        if st.button("🔌 CONNECT & JOIN ROOM", use_container_width=True):
            code = join_code_input.strip().upper()
            if code and not code.startswith("PKR-"):
                code = f"PKR-{code}"
            guest_name = join_name_input.strip() or "Guest (You)"
            
            rooms = get_global_rooms()
            if code not in rooms:
                st.error(f"Room {code} not found! Make sure the Room Host has launched the room.")
            else:
                room = rooms[code]
                with room["lock"]:
                    st.session_state.my_player_name = guest_name
                    st.session_state.room_code = code
                    
                    # Add guest player if not already in list
                    existing = [p for p in room["players"] if p.name == guest_name]
                    if not existing:
                        guest_p = Player(name=guest_name, chips=room["starting_chips"], is_ai=False)
                        room["players"].append(guest_p)
                    
                    if room["game"] is None:
                        game_obj = Game(players=room["players"])
                        game_obj.table.small_blind = room["small_blind"]
                        game_obj.table.big_blind = room["big_blind"]
                        start_game_hand(game_obj)
                        room["game"] = game_obj
                        room["status"] = "IN_GAME"
                    
                    st.session_state.game = room["game"]
                    st.session_state.view = "game"
                    st.rerun()

# ==============================================================================
# WAITING ROOM VIEW (Hosted Rooms)
# ==============================================================================
elif st.session_state.view == "waiting_room":
    code = st.session_state.room_code
    rooms = get_global_rooms()
    room = rooms.get(code)
    
    if not room:
        st.error("Room expired or cancelled!")
        if st.button("🏠 Return to Lobby"):
            st.session_state.view = "lobby"
            st.rerun()
    else:
        # Check if guest player connected in background
        if room["status"] == "IN_GAME" and room.get("game"):
            st.session_state.game = room["game"]
            st.session_state.view = "game"
            st.rerun()

        st.markdown('<div class="poker-title">♠️ MULTIPLAYER WAITING LOBBY ♠️</div>', unsafe_allow_html=True)
        st.caption("<div style='text-align:center;'>Share your Room Code with your friend so they can connect!</div>", unsafe_allow_html=True)
        st.markdown("---")

        st.markdown(f"""<div class="room-box">
<h3 style="color:#10b981; margin:0;">YOUR HOST ROOM CODE:</h3>
<h1 style="color:#f59e0b; font-size:3.5rem; letter-spacing:4px; margin:10px 0;">{code}</h1>
<h3 style="color:#38bdf8; margin: 10px 0;">Give this code to your friend to join your game!</h3>
<p style="color:#cbd5e1;">Status: <b style="color:#f59e0b;">Waiting for Guest Player...</b></p>
</div>""", unsafe_allow_html=True)

        st.markdown(f"### 👥 Connected Seats ({len(room['players'])} Player):")
        for i, p in enumerate(room["players"]):
            st.write(f"• **Seat #{i+1}: {p.name}** ({'AI Bot' if getattr(p, 'is_ai', False) else 'Human Player'})")

        st.markdown("---")
        w_col1, w_col2 = st.columns(2)
        with w_col1:
            if st.button("🤖 Add AI Bot & Start Game Now", use_container_width=True):
                with room["lock"]:
                    bot_p = AIPlayer(name="Bot Alpha", bot=BotPlayer(name="Bot Alpha", difficulty=Difficulty.HARD, strategy=Strategy.TIGHT_AGGRESSIVE), chips=room["starting_chips"])
                    room["players"].append(bot_p)
                    game_obj = Game(players=room["players"])
                    game_obj.table.small_blind = room["small_blind"]
                    game_obj.table.big_blind = room["big_blind"]
                    start_game_hand(game_obj)
                    room["game"] = game_obj
                    room["status"] = "IN_GAME"
                    st.session_state.game = game_obj
                    st.session_state.view = "game"
                    st.rerun()

        with w_col2:
            if st.button("❌ Cancel Hosted Room", use_container_width=True):
                rooms.pop(code, None)
                st.session_state.room_code = ""
                st.session_state.view = "lobby"
                st.rerun()

        time.sleep(1.2)
        st.rerun()

# ==============================================================================
# GAME VIEW
# ==============================================================================
elif st.session_state.view == "game":
    room_code = st.session_state.get("room_code", "")
    rooms = get_global_rooms()
    room = rooms.get(room_code) if room_code else None
    
    if room and room.get("game"):
        game = room["game"]
        st.session_state.game = game
        st.session_state.winners_list = room.get("winners_list", [])
        st.session_state.winner_banner_text = room.get("winner_banner_text", "")
        st.session_state.log_messages = room.get("log_messages", [])
    else:
        game = st.session_state.game
    
    # Auto-advance street if betting round is complete or all active players are All-In
    check_and_advance_street(game)

    # Pre-compute AI decision BEFORE rendering (so we can show what it chose)
    # but do NOT rerun yet — we rerun at the very bottom after the full UI renders.
    curr_p = game.betting_round.current_player_or_none()
    hand_in_progress = (game.state.name not in ("SHOWDOWN", "HAND_COMPLETE", "WAITING"))
    is_all_ai_game = all(getattr(p, "is_ai", False) for p in game.players)

    ai_needs_rerun = False
    if curr_p and not getattr(curr_p, "folded", False) and getattr(curr_p, "is_ai", False) and hand_in_progress and not st.session_state.ai_paused:
        # Pre-compute the AI decision synchronously (fast) so we can display it
        context = GameContext(
            hole_cards=curr_p.hand,
            community_cards=game.table.community_cards,
            pot_size=game.pot_manager.total_pot(),
            current_bet=getattr(game.table, "current_bet", 0),
            call_amount=max(0, getattr(game.table, "current_bet", 0) - curr_p.current_bet),
            player_stack=curr_p.chips,
            players_remaining=sum(1 for p in game.players if not getattr(p, "folded", False))
        )
        
        try:
            decision = curr_p.decide(context)
            if isinstance(decision, dict):
                act = decision.get("action", Action.CHECK)
                amt = decision.get("amount", 0)
            elif isinstance(decision, tuple):
                act, amt = decision
            else:
                act, amt = Action.CHECK, 0
        except Exception:
            act, amt = Action.CHECK, 0

        execute_player_action(game, curr_p, act, amt)
        st.session_state.log_messages.append(f"{curr_p.name} performed {act.name} ${amt}")
        ai_needs_rerun = True
        # Re-read current player after the action was applied
        curr_p = game.betting_round.current_player_or_none()
        hand_in_progress = (game.state.name not in ("SHOWDOWN", "HAND_COMPLETE", "WAITING"))

    # ===================== SIDEBAR CONTROLS & HUD =====================
    with st.sidebar:
        st.subheader("⚙️ Game Options")
        if st.button("🏠 Return to Lobby", use_container_width=True):
            st.session_state.view = "lobby"
            st.rerun()

        if is_all_ai_game:
            pause_label = "▶️ Resume Battle" if st.session_state.ai_paused else "⏸️ Pause AI Battle"
            if st.button(pause_label, use_container_width=True):
                st.session_state.ai_paused = not st.session_state.ai_paused
                st.rerun()

        st.session_state.show_hud = st.checkbox("🧠 Show AI Brain HUD", value=st.session_state.show_hud)
        st.session_state.show_rankings = st.checkbox("🏆 Hand Rankings Guide", value=st.session_state.show_rankings)
        st.session_state.tournament_mode = st.checkbox("🏆 Tournament Blinds Escalation", value=st.session_state.get("tournament_mode", False))

        hud_player = curr_p if (curr_p and not getattr(curr_p, "is_ai", False)) else next((p for p in game.players if not getattr(p, "is_ai", False) and not getattr(p, "folded", False)), None)
        if st.session_state.show_hud and hud_player and hasattr(hud_player, "hand") and hud_player.hand and hand_in_progress and not is_all_ai_game:
            active_opponents = sum(1 for p in game.players if not getattr(p, "folded", False) and p.name != hud_player.name)
            try:
                eq_res = equity_calc.calculate(hud_player.hand, game.table.community_cards, max(1, active_opponents), simulations=150)
                equity_pct = eq_res.get("equity", 0.5) * 100
            except Exception:
                equity_pct = 50.0
            
            rank_name = get_player_hand_name(hud_player, game.table.community_cards) or "High Card"
            ev_score = f"+{(equity_pct / 18.0):.1f} EV (Optimal)" if equity_pct >= 50 else f"-{((100-equity_pct)/25.0):.1f} EV"

            st.markdown(f"""<div class="hud-box">
<h5 style="margin:0; color:#818cf8;">🧠 AI LIVE HUD — {hud_player.name}</h5>
<div style="margin-top:6px; font-size:0.85rem;">
<div><b>Hand Strength:</b> <span style="color:#f59e0b;">{rank_name}</span></div>
<div><b>Win Equity:</b> <span style="color:#10b981;">{equity_pct:.1f}%</span></div>
<div><b>Decision EV:</b> <span style="color:#a855f7;">{ev_score}</span></div>
<div><b>Pot Odds:</b> <span style="color:#38bdf8;">{(game.table.big_blind / max(1, game.pot_manager.total_pot()))*100:.1f}%</span></div>
</div>
</div>""", unsafe_allow_html=True)

        if st.session_state.show_rankings:
            st.markdown("""
            **Rankings (High → Low):**
            1. Royal Flush  2. Straight Flush
            3. 4 of a Kind  4. Full House
            5. Flush        6. Straight
            7. 3 of a Kind  8. Two Pair
            9. One Pair     10. High Card
            """)

        # ------------------ LIVE CHAT & QUICK EMOTES ------------------
        st.markdown("---")
        st.subheader("💬 Live Chat & Reactions")
        
        sender_name = st.session_state.get("my_player_name", "Player")
        
        def _send_chat_msg(msg_text):
            r_code = st.session_state.get("room_code", "")
            rm = get_room(r_code)
            log_item = f"💬 **{sender_name}**: {msg_text}"
            if rm:
                if "chat_messages" not in rm:
                    rm["chat_messages"] = []
                rm["chat_messages"].append(log_item)
                st.session_state.chat_messages = rm["chat_messages"]
            else:
                st.session_state.chat_messages.append(log_item)

        e_col1, e_col2, e_col3 = st.columns(3)
        with e_col1:
            if st.button("🦈 Shark!", key="em_1", use_container_width=True):
                _send_chat_msg("🦈 Shark Attack!")
                st.rerun()
            if st.button("💰 Pay Me!", key="em_2", use_container_width=True):
                _send_chat_msg("💰 Pay Me!")
                st.rerun()
        with e_col2:
            if st.button("🤡 Bluff!", key="em_3", use_container_width=True):
                _send_chat_msg("🤡 Nice Bluff!")
                st.rerun()
            if st.button("🔥 All In!", key="em_4", use_container_width=True):
                _send_chat_msg("🔥 All In!")
                st.rerun()
        with e_col3:
            if st.button("🤠 Gittyup!", key="em_5", use_container_width=True):
                _send_chat_msg("🤠 Gittyup!")
                st.rerun()
            if st.button("🤝 GG!", key="em_6", use_container_width=True):
                _send_chat_msg("🤝 Good Game!")
                st.rerun()

        def _on_chat_enter():
            text = st.session_state.get("chat_input_txt", "").strip()
            if text:
                _send_chat_msg(text)
                st.session_state["chat_input_txt"] = ""

        st.text_input("Type message & press Enter:", key="chat_input_txt", placeholder="Type message & press Enter...", on_change=_on_chat_enter)
        if st.button("📤 Send Chat", key="send_chat_btn", use_container_width=True):
            _on_chat_enter()
            st.rerun()

        r_code = st.session_state.get("room_code", "")
        rm = get_room(r_code)
        active_msgs = rm.get("chat_messages", []) if rm else st.session_state.chat_messages
        for c_msg in reversed(active_msgs[-5:]):
            st.markdown(c_msg)

        st.markdown("---")
        st.subheader("📜 Hand History")
        for log_msg in reversed(st.session_state.log_messages[-6:]):
            st.caption(log_msg)

    # ===================== MAIN GAME VIEWPORT (COMPACT SINGLE SCREEN) =====================
    room_banner = f" | Room: <b style='color:#a855f7;'>{st.session_state.room_code}</b>" if st.session_state.room_code else ""
    st.markdown(f"""<div style='text-align:center; padding:0; margin-bottom:2px;'>
<span style='font-size:1.35rem; font-weight:900; color:#f59e0b;'>♠️ TEXAS HOLD'EM POKER ♠️</span>
<span style='color:#cbd5e1; font-weight:600; font-size:0.85rem; margin-left:10px;'>Hand #{st.session_state.hand_count} • Blinds ${game.table.small_blind}/${game.table.big_blind} • Street: <b style='color:#10b981;'>{game.table.street.name}</b>{room_banner}</span>
</div>""", unsafe_allow_html=True)

    last_logged_action = st.session_state.log_messages[-1] if st.session_state.log_messages else "Game Started"
    st.markdown(f'<div style="text-align:center; color:#38bdf8; font-weight:700; font-size:0.9rem; margin-bottom:4px;">📢 LAST ACTION: <span style="color:#f59e0b;">{last_logged_action}</span></div>', unsafe_allow_html=True)

    total_pot = game.pot_manager.total_pot()
    comm_cards = game.table.community_cards
    comm_html = "".join([render_card_html(c) for c in comm_cards])
    if not comm_cards:
        comm_html = "".join([render_card_html(None) for _ in range(5)])

    # FELT TABLE CONTAINER
    st.markdown(f"""<div class="felt-table">
<div class="pot-badge">🪙 POT: ${total_pot}</div>
<div style="margin-top: 4px;">{comm_html}</div>
</div>""", unsafe_allow_html=True)

    # WINNER BANNER DISPLAY
    if not hand_in_progress and st.session_state.winner_banner_text:
        st.markdown(f"""<div class="winner-banner-box">
<h3 style="color:#f59e0b; margin:0; font-size:1.3rem; font-weight:900;">{st.session_state.winner_banner_text}</h3>
</div>""", unsafe_allow_html=True)

    # PLAYER SEATS GRID
    cols = st.columns(len(game.players))
    for i, p in enumerate(game.players):
        with cols[i]:
            is_winner = (p.name in st.session_state.winners_list)
            is_curr = (curr_p and curr_p.name == p.name and hand_in_progress)
            
            box_cls = "player-seat"
            if is_winner:
                box_cls += " winner-seat-glow"
            elif is_curr:
                box_cls += " active-seat-glow"
                
            winner_badge = '<div class="winner-badge">🏆 WINNER</div>' if is_winner else ''
            dealer_badge = '<span class="dealer-badge">D</span>' if p.is_dealer() else ''
            action_badge_html = get_action_badge_html(p, is_winner)
            
            should_reveal_hole_cards = False
            if is_all_ai_game:
                should_reveal_hole_cards = True
            elif not hand_in_progress:
                should_reveal_hole_cards = st.session_state.show_cards_showdown
            elif st.session_state.room_code != "":
                should_reveal_hole_cards = (p.name == st.session_state.get("my_player_name", ""))
            else:
                should_reveal_hole_cards = (curr_p and curr_p.name == p.name and not getattr(p, "is_ai", False))

            if should_reveal_hole_cards:
                cards_html = "".join([render_card_html(c) for c in p.hand])
            else:
                cards_html = "".join([render_card_html(None) for _ in p.hand])

            hand_name_desc = ""
            if should_reveal_hole_cards and len(p.hand) >= 2:
                h_comb = get_player_hand_name(p, game.table.community_cards)
                if h_comb:
                    hand_name_desc = f'<div style="color:#f59e0b; font-weight:700; font-size:0.75rem; margin-top:2px;">✨ {h_comb}</div>'

            seat_html = (
                f'<div class="{box_cls}">'
                f'{winner_badge}'
                f'{action_badge_html}'
                f'<div style="font-weight:800; font-size:0.95rem; color:#f59e0b; margin-top:2px;">{p.name}{dealer_badge}</div>'
                f'<div style="color:#10b981; font-size:0.85rem; font-weight:700;">${p.chips}</div>'
                f'<div style="color:#cbd5e1; font-size:0.78rem;">Bet: ${p.current_bet}</div>'
                f'<div style="margin-top:2px;">{cards_html}</div>'
                f'{hand_name_desc}'
                f'</div>'
            )
            st.markdown(seat_html, unsafe_allow_html=True)

    # DOCKED HUMAN ACTION CONTROL BAR
    if curr_p and not getattr(curr_p, "is_ai", False) and hand_in_progress:
        curr_hand_combination = get_player_hand_name(curr_p, game.table.community_cards)
        current_tbl_bet = getattr(game.table, "current_bet", 0)
        call_amt = max(0, current_tbl_bet - curr_p.current_bet)

        hand_tag = f" | 🃏 BEST HAND: <span style='color:#f59e0b;'>{curr_hand_combination}</span>" if curr_hand_combination else ""
        st.markdown(f'<div style="background: rgba(16, 185, 129, 0.12); border: 1px solid #10b981; border-radius: 6px; padding: 3px 10px; margin: 4px 0; font-size: 0.9rem; font-weight: 700; color: #e2e8f0;">🎯 YOUR TURN ({curr_p.name}){hand_tag}</div>', unsafe_allow_html=True)

        qb1, qb2, qb3, qb4, qb5 = st.columns(5)
        with qb1:
            if st.button("MIN BET", use_container_width=True):
                execute_player_action(game, curr_p, Action.BET, game.table.big_blind)
                st.session_state.log_messages.append(f"{curr_p.name} BET ${game.table.big_blind}")
                st.rerun()
        with qb2:
            if st.button("+3BB", use_container_width=True):
                amt = game.table.big_blind * 3
                execute_player_action(game, curr_p, Action.RAISE, amt)
                st.session_state.log_messages.append(f"{curr_p.name} RAISED ${amt}")
                st.rerun()
        with qb3:
            if st.button("1/2 POT", use_container_width=True):
                amt = max(game.table.big_blind, int(total_pot * 0.5))
                execute_player_action(game, curr_p, Action.RAISE, amt)
                st.session_state.log_messages.append(f"{curr_p.name} RAISED 1/2 POT (${amt})")
                st.rerun()
        with qb4:
            if st.button("FULL POT", use_container_width=True):
                amt = max(game.table.big_blind, total_pot)
                execute_player_action(game, curr_p, Action.RAISE, amt)
                st.session_state.log_messages.append(f"{curr_p.name} RAISED POT (${amt})")
                st.rerun()
        with qb5:
            if st.button("🔥 ALL-IN", use_container_width=True):
                execute_player_action(game, curr_p, Action.ALL_IN, curr_p.chips)
                st.session_state.log_messages.append(f"{curr_p.name} went ALL-IN for ${curr_p.chips}!")
                st.rerun()

        ac1, ac2, ac3 = st.columns(3)
        with ac1:
            if st.button("🔴 FOLD", use_container_width=True):
                execute_player_action(game, curr_p, Action.FOLD, 0)
                st.session_state.log_messages.append(f"{curr_p.name} FOLDED")
                st.rerun()

        with ac2:
            lbl = "🟢 CHECK" if call_amt <= 0 else f"🟢 CALL (${call_amt})"
            act_type = Action.CHECK if call_amt <= 0 else Action.CALL
            if st.button(lbl, use_container_width=True):
                execute_player_action(game, curr_p, act_type, max(0, call_amt))
                st.session_state.log_messages.append(f"{curr_p.name} {lbl}")
                st.rerun()

        with ac3:
            min_raise = current_tbl_bet * 2 if current_tbl_bet > 0 else game.table.big_blind
            max_raise = curr_p.chips
            if max_raise > min_raise:
                raise_amt = st.slider("Custom Raise Amount ($)", min_value=int(min_raise), max_value=int(max_raise), value=int(min_raise), step=10, label_visibility="collapsed")
                if st.button(f"🔵 RAISE (${raise_amt})", use_container_width=True):
                    execute_player_action(game, curr_p, Action.RAISE, raise_amt)
                    st.session_state.log_messages.append(f"{curr_p.name} RAISED to ${raise_amt}")
                    st.rerun()
            else:
                st.caption("Insufficient chips to raise")

    elif not hand_in_progress:
        m_c1, m_c2 = st.columns(2)
        with m_c1:
            st.session_state.show_cards_showdown = st.checkbox("👁️ Reveal Cards at Showdown", value=st.session_state.show_cards_showdown)
        with m_c2:
            if st.button("▶️ Deal Next Hand", use_container_width=True):
                r_code = st.session_state.get("room_code", "")
                rm = rooms.get(r_code)
                if rm and "lock" in rm:
                    with rm["lock"]:
                        if st.session_state.auto_rebuy:
                            for p in game.players:
                                if p.chips <= 0:
                                    p.chips = st.session_state.starting_chips
                                    st.session_state.log_messages.append(f"🔄 Auto-Rebought {p.name} for ${st.session_state.starting_chips}")
                        st.session_state.hand_count += 1
                        start_game_hand(game)
                        rm["hand_count"] = st.session_state.hand_count
                        rm["log_messages"] = st.session_state.log_messages
                        rm["winners_list"] = []
                        rm["winner_banner_text"] = ""
                else:
                    if st.session_state.auto_rebuy:
                        for p in game.players:
                            if p.chips <= 0:
                                p.chips = st.session_state.starting_chips
                                st.session_state.log_messages.append(f"🔄 Auto-Rebought {p.name} for ${st.session_state.starting_chips}")
                    st.session_state.hand_count += 1
                    start_game_hand(game)
                st.rerun()

    # ===================== RERUN TRIGGERS (AFTER ALL UI RENDERED) =====================
    # The full table, cards, seats, and action badges have been sent to the browser.
    # Now trigger the next frame if needed.

    # 1. AI just acted — rerun for the next AI step
    if ai_needs_rerun:
        time.sleep(0.15)
        st.rerun()

    # 2. All remaining players are all-in — nobody can act, but we need to
    #    advance streets one at a time visually (Flop → Turn → River → Showdown).
    #    Each rerun draws the new community cards, then triggers the next street.
    if hand_in_progress and game.betting_round.betting_complete():
        all_in_or_folded = all(
            getattr(p, "folded", False) or not p.can_act()
            for p in game.players
        )
        if all_in_or_folded:
            time.sleep(0.8)  # Pause so user sees each street dealt
            st.rerun()

    # 3. In Online Room Multiplayer, auto-poll if waiting for opponent's turn
    if room_code and hand_in_progress:
        curr_p = game.betting_round.current_player_or_none()
        if curr_p and curr_p.name != st.session_state.my_player_name and not getattr(curr_p, "is_ai", False):
            time.sleep(1.0)
            st.rerun()
