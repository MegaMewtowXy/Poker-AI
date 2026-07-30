import concurrent.futures
import os
import math
from models.card import Card
from models.deck import Deck
from engine.evaluator import HandEvaluator

def _run_simulation_chunk(hero_cards, community_cards, opponent_count, num_trials, seed_offset, deck_proto=None):
    """
    Thread-safe standalone worker for parallel Monte Carlo trials.
    """
    evaluator = HandEvaluator()
    wins = 0
    ties = 0
    tie_equity = 0.0
    losses = 0
    base_deck = deck_proto if deck_proto is not None else Deck()

    for idx in range(num_trials):
        sim_deck = base_deck.clone()
        shuffle_seed = (seed_offset + idx) if seed_offset is not None else None
        sim_deck.shuffle(shuffle_seed)

        known_cards = hero_cards + community_cards
        sim_deck.remove_cards(known_cards)

        opponents = [sim_deck.deal_many(2) for _ in range(opponent_count)]

        board = community_cards.copy()
        missing = 5 - len(board)
        if missing > 0:
            board.extend(sim_deck.deal_many(missing))

        hero_score = evaluator.evaluate(hero_cards, board).score
        tied_players = 1
        lost = False

        for opp in opponents:
            opp_score = evaluator.evaluate(opp, board).score
            if opp_score < hero_score:
                lost = True
                break
            elif opp_score == hero_score:
                tied_players += 1

        if lost:
            losses += 1
        elif tied_players > 1:
            ties += 1
            tie_equity += 1.0 / tied_players
        else:
            wins += 1

    return wins, ties, tie_equity, losses

class EquityCalculator:
    """
    Multi-Threaded Monte Carlo Poker Equity Calculator.

    Calculates:
    - Win percentage
    - Tie percentage
    - Lose percentage
    - Equity

    Simulation safe:
    ----------------
    Does not modify:
    - Player objects
    - Deck objects
    - Game state
    """

    def __init__(self, seed: int | None = None, max_workers: int | None = None):
        self.evaluator = HandEvaluator()
        self.seed = seed
        self.max_workers = max_workers or min(os.cpu_count() or 4, 8)
        self._simulation_index = 0
        self._last_tied_players = 1

    def calculate(
        self,
        hero_cards: list[Card],
        community_cards: list[Card],
        opponent_count: int = 1,
        simulations: int = 5000,
        deck: Deck = None
    ) -> dict:
        """
        Calculate hero equity using parallel multi-threaded Monte Carlo trials.
        """
        if len(hero_cards) != 2:
            raise ValueError("Hero must have exactly two hole cards.")

        if len(community_cards) > 5:
            raise ValueError("Community cards cannot exceed five cards.")

        known_cards = hero_cards + community_cards
        if len(set(known_cards)) != len(known_cards):
            raise ValueError("Known cards cannot contain duplicates.")

        if opponent_count <= 0:
            raise ValueError("Opponent count must be positive.")

        if simulations <= 0:
            raise ValueError("Simulation count must be positive.")

        available_cards = 52 - len(known_cards)
        cards_needed = opponent_count * 2 + (5 - len(community_cards))
        if cards_needed > available_cards:
            raise ValueError("Not enough cards available for the requested simulation.")

        # Multi-Threaded Execution for 100+ trials
        if simulations >= 100 and self.max_workers > 1:
            workers = min(self.max_workers, simulations)
            chunk_size = simulations // workers
            remainder = simulations % workers

            chunks = [chunk_size + (1 if i < remainder else 0) for i in range(workers)]
            chunks = [c for c in chunks if c > 0]

            wins, ties, tie_equity, losses = 0, 0, 0.0, 0

            with concurrent.futures.ThreadPoolExecutor(max_workers=len(chunks)) as executor:
                futures = []
                for i, count in enumerate(chunks):
                    seed_off = (self.seed + i * chunk_size) if self.seed is not None else None
                    futures.append(
                        executor.submit(
                            _run_simulation_chunk,
                            hero_cards,
                            community_cards,
                            opponent_count,
                            count,
                            seed_off,
                            deck
                        )
                    )

                for f in concurrent.futures.as_completed(futures):
                    w, t, te, l = f.result()
                    wins += w
                    ties += t
                    tie_equity += te
                    losses += l
        else:
            wins, ties, tie_equity, losses = _run_simulation_chunk(
                hero_cards,
                community_cards,
                opponent_count,
                simulations,
                self.seed,
                deck
            )

        total = wins + ties + losses

        return {
            "win_percentage": round(wins / total * 100, 2),
            "tie_percentage": round(ties / total * 100, 2),
            "lose_percentage": round(losses / total * 100, 2),
            "equity": round((wins + tie_equity) / total * 100, 2),
        }

    def simulate(
        self,
        hero_cards: list[Card],
        community_cards: list[Card],
        opponent_count: int,
        deck: Deck = None
    ) -> str:
        """
        Run one simulation.
        """
        wins, ties, tie_eq, losses = _run_simulation_chunk(
            hero_cards,
            community_cards,
            opponent_count,
            1,
            self.seed + self._simulation_index if self.seed is not None else None,
            deck
        )
        self._simulation_index += 1

        if wins > 0:
            self._last_tied_players = 1
            return "win"
        elif ties > 0:
            self._last_tied_players = int(round(1.0 / tie_eq)) if tie_eq > 0 else 2
            return "tie"
        else:
            self._last_tied_players = 0
            return "lose"

    def __repr__(self):
        return "EquityCalculator()"

    def __str__(self):
        return "Texas Hold'em Multi-Threaded Equity Calculator"
