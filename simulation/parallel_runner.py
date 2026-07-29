import concurrent.futures
import math
import os
import random
from simulation.bot_vs_bot import BotVsBotSimulation

def _run_sub_simulation(args):
    """
    Worker function to run a slice of simulation hands.
    """
    hands, starting_chips, seed, enable_logging = args
    sim = BotVsBotSimulation(
        hands=hands,
        starting_chips=starting_chips,
        seed=seed,
        enable_logging=enable_logging,
        auto_rebuy=True
    )
    return sim.run()

class ParallelSimulationRunner:
    """
    Multi-core parallel simulation execution runner.
    """

    def __init__(
        self,
        hands=500,
        starting_chips=1000,
        seed=None,
        enable_logging=False,
        num_workers=None
    ):
        self.hands = hands
        self.starting_chips = starting_chips
        self.seed = seed
        self.enable_logging = enable_logging
        self.num_workers = num_workers or min(4, os.cpu_count() or 2)

    def run(self):
        """
        Distribute hands across worker threads and merge statistics.
        """
        chunk_size = math.ceil(self.hands / self.num_workers)
        base_seed = self.seed if self.seed is not None else random.randint(1, 1000000)

        tasks = []
        for i in range(self.num_workers):
            sub_hands = min(chunk_size, self.hands - i * chunk_size)
            if sub_hands <= 0:
                break
            sub_seed = base_seed + i * 1337
            tasks.append((sub_hands, self.starting_chips, sub_seed, self.enable_logging))

        merged_results = {
            "hands_requested": self.hands,
            "hands_completed": 0,
            "hands_failed": 0,
            "results": {},
            "errors": []
        }

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            sub_results = list(executor.map(_run_sub_simulation, tasks))

        for sub in sub_results:
            merged_results["hands_completed"] += sub.get("hands_completed", 0)
            merged_results["hands_failed"] += sub.get("hands_failed", 0)
            merged_results["errors"].extend(sub.get("errors", []))

            res = sub.get("results", {})
            for bot_name, stats in res.items():
                if bot_name not in merged_results["results"]:
                    merged_results["results"][bot_name] = {
                        "hands": 0,
                        "wins": 0,
                        "losses": 0,
                        "ties": 0,
                        "chips": self.starting_chips,
                        "win_rate": 0.0,
                        "busts": 0,
                        "busted": False
                    }
                r = merged_results["results"][bot_name]
                r["hands"] += stats.get("hands", 0)
                r["wins"] += stats.get("wins", 0)
                r["losses"] += stats.get("losses", 0)
                r["ties"] += stats.get("ties", 0)
                r["busts"] += stats.get("busts", 0)
                r["chips"] += (stats.get("chips", 1000) - self.starting_chips)

        for bot_name, r in merged_results["results"].items():
            if r["hands"] > 0:
                r["win_rate"] = round(r["wins"] / r["hands"], 3)
            r["busted"] = r["chips"] <= 0

        return merged_results
