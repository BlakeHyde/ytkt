from __future__ import annotations

from itertools import count
from typing import Any, List, Mapping

from .types import Task


id_counter = count(1)


def parse_tasks(raw_tasks: List[Mapping[str, Any]]) -> List[Task]:
    tasks = []
    tasks_by_alias = {}
    task_blocks = {}

    for rt in raw_tasks:
        task = Task(
            id=next(id_counter),
            title=rt["title"],
            description=rt["description"],
            alias=rt.get("alias"),
            blocked_by=[],
            points=rt.get("points"),
        )
        tasks.append(task)

        if blocks := rt.get("blocked-by"):
            task_blocks[task] = blocks

        if task.alias is not None:
            tasks_by_alias[task.alias] = task

    for t in tasks:
        t.blocked_by = [tasks_by_alias[bb] for bb in task_blocks.get(t, [])]

    return tasks
