This utility converts a set of tickets defined in YAML into friendly
Markdown or a Jira-formatted CSV.

# Usage

To install its dependencies, clone the repository and run `poetry install`
in the root directory.

To run the script, use the `ytkt` command:

```
ytkt [--csv] [--epic <Epic ID>] [--team <Team Name>] <yaml file>
```

Without `--csv`, the output will be Markdown.

# Formatting Your Tickets

Use a YAML file with this structure:

```yaml
tasks:
  - title: string
    description: string
    alias: optional string
    blocks: optional list of aliases
    blocked-by: optional list of aliases
    points: optional int
```

Note that the script does not (yet) export blocking relationships to the
Jira CSV.
