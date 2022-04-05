from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Task:
    id: int
    title: str
    description: str
    alias: Optional[str]
    blocks: List[Task]
    blocked_by: List[Task]
    points: Optional[int]

    def __hash__(self):
        return self.id
