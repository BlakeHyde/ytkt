from __future__ import annotations

from collections import defaultdict
from itertools import count
from typing import Any, List, Mapping

from .types import Task


id_counter = count(1)


def parse_tasks(raw_tasks: List[Mapping[str, Any]]) -> List[Task]:
    tasks = []
    tasks_by_alias = {}

    # Allow both outward and inward links; Jira only allows importing outward links.
    inward_blocks = {}
    outward_blocks = {}

    for rt in raw_tasks:
        task = Task(
            id=next(id_counter),
            title=rt["title"],
            description=rt["description"],
            alias=rt.get("alias"),
            blocks=[],
            blocked_by=[],
            points=rt.get("points"),
        )
        tasks.append(task)

        if blocks := rt.get("blocked-by"):
            inward_blocks[task] = blocks

        if blocks := rt.get("blocks"):
            outward_blocks[task] = blocks

        if task.alias is not None:
            tasks_by_alias[task.alias] = task

    inverted_inward_blocks = _invert_references(tasks_by_alias, inward_blocks)
    inverted_outward_blocks = _invert_references(tasks_by_alias, outward_blocks)

    for t in tasks:
        t.blocks = [tasks_by_alias[bb] for bb in outward_blocks.get(t, [])]
        t.blocks.extend(inverted_inward_blocks.get(t, []))

        t.blocked_by = [tasks_by_alias[bb] for bb in inward_blocks.get(t, [])]
        t.blocked_by.extend(inverted_outward_blocks.get(t, []))


    return tasks


def _invert_references(mapping, inward_references):
    """
    Convert a dictionary of ``Task -> [TaskRef]`` to a list of ``Task ->
    [Task]``, with the key tasks built from the ``TaskRef`` in the original
    dictionary.
    """
    inverted = defaultdict(list)

    for task, references in inward_references.items():
        for ref in references:
            inverted[mapping[ref]].append(task)

    return inverted
