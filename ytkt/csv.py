from __future__ import annotations

from typing import Any, List, Mapping, Protocol

from .types import Task


class AttributeMapping(Protocol):
    def __call__(self, context, task):
        raise NotImplementedError()


class Static(AttributeMapping):
    def __init__(self, value):
        self.value = value
    def __call__(self, *_):
        return self.value


class TaskAttribute(AttributeMapping):
    def __init__(self, *attributes):
        self.attributes = attributes

    def __call__(self, _, task: Task):
        last_value = getattr(task, self.attributes[0])

        for attr in self.attributes[1:]:
            if last_value is not None:
                last_value = getattr(last_value, attr)

        return last_value


class CommandLineArg(AttributeMapping):
    def __init__(self, arg):
        self.arg = arg

    def __call__(self, context, _):
        return getattr(context, self.arg)


class Conditional(AttributeMapping):
    def __init__(self, mapping: AttributeMapping, comparison, true, false):
        self.mapping = mapping
        self.comparison = comparison
        self.true = true
        self.false = false

    def __call__(self, context, task):
        next_mapping = self.true if self.comparison(context, task) else self.false
        return next_mapping(context, task)


def _present(_, x):
    return x is not None


COLUMN_MAPPINGS = {
    #"Issue ID": TaskAttribute("id"),
    "Issue Type": Static("Task"),
    "Summary": TaskAttribute("title"),
    "Description": TaskAttribute("description"),
    "Component": Static("Ownership"),
    "Epic Link": CommandLineArg("epic"),
    "Points": TaskAttribute("points"),
    "Workstream": Static("backlog"),
    "Priority": Static(None),
    "Sprint": Conditional(TaskAttribute("points"), _present, Static("Refined"), Static(None)),
    "Assignee": Static(None),
    "Label": Static(None),
    "Team": CommandLineArg("team"),
    #"Blocked By": TaskAttribute("blocked_by", "id"),
}


def field_names(mappings: Mapping[str, Any] = COLUMN_MAPPINGS) -> List[str]:
    return list(mappings.keys())


def map_task_to_csv(context, task, mappings=COLUMN_MAPPINGS):
    return {column: mapping(context, task) for column, mapping in mappings.items()}

