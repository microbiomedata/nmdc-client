# NMDC skills

## Install with npx skills

See the [branch-specific installation instructions](../README.md#agent-skills)
to list and install `gff-analysis` or `enrichment-analysis` for your agent, with
project or global scope. Use the explicit `adding-cli-and-docs` URL: the current
default branch does not contain these skills.

## Use in Claude Code

The existing local marketplace command, run in Claude Code from the repository
root of this branch, is:

```text
/plugin marketplace add ./.claude-plugin/marketplace.json
```

This registers a Claude marketplace rather than installing skills through the
Skills CLI. The legacy manifest also references `nmdc-data`, which is absent from
this branch; `npx skills ... --list` reports only the two available skills above.
