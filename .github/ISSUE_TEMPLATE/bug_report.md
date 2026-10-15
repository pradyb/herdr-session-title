---
name: Bug Report
about: Report a bug to help improve herdr-session-title
title: "[BUG] "
labels: bug
assignees: ""
---

## Describe the Bug

A clear and concise description of what the bug is.

## Steps to Reproduce

1. Layout: how many tabs in the space, how many Claude panes `...`
2. Run `/rename ...` in Claude
3. See what got renamed (or didn't)

## Expected Behaviour

What you expected to happen.

## Actual Behaviour

What actually happened. Include any error output, for example from
`~/.local/state/herdr/plugins/pradyb.session-title/daemon.log`
and `herdr plugin log list --plugin pradyb.session-title`.

## Environment

- **herdr version** (`herdr --version`):
- **herdr-session-title version** (`version` in `herdr-plugin.toml`):
- **Python version** (`python3 --version`):
- **OS and architecture**:
- **Claude Code version** (`claude --version`):

## Additional Context

Any other context about the problem. Never paste transcript content.
