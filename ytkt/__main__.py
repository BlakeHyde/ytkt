from argparse import ArgumentParser
from sys import stdout

import yaml

from .parsing import parse_tasks
from .printing import csv, markdown


parser = ArgumentParser()
parser.add_argument("file")
parser.add_argument("--csv", action="store_true")
parser.add_argument("--epic")
parser.add_argument("--team")
args = parser.parse_args()

with open(args.file, "r") as f:
    raw_tasks = yaml.safe_load(f)["tasks"]

tasks = parse_tasks(raw_tasks)

if args.csv:
    context = args
    stream = stdout
    csv(context, tasks, stream)
else:
    print("\n".join(markdown(tasks)))


def main():
    pass
