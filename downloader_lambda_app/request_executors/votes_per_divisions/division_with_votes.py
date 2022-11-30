from dataclasses import dataclass
from typing import List


@dataclass
class DivisionWithVotes:
    division_id: int
    ayes: List[int]
    noes: List[int]
    no_attends: List[int]
