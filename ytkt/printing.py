from csv import DictWriter
from functools import partial
from typing import Iterator, List

from ytkt.csv import field_names, map_task_to_csv
from .types import Task


def markdown(tasks: List[Task]) -> Iterator[str]:
    for task in tasks:
        yield f"# {task.title}\n"
        description_text = task.description.replace("\n", "\n\n")
        yield f"{description_text}"

        if task.blocked_by:
            yield f"## Tasks blocking this work\n"

            for blocker in task.blocked_by:
                yield f"- {blocker.title}"


def csv(context, tasks: List[Task], stream):
    writer = DictWriter(stream, field_names())
    writer.writeheader()
    task_mapper = partial(map_task_to_csv, context)
    writer.writerows(map(task_mapper, tasks))
