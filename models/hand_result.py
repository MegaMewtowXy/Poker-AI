from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class HandResult:
    score: int
    rank: int
    hand_name: str

    win_probability: Optional[float] = None
    confidence: Optional[float] = None
    explanation: str = ""