# herdr session-title

Name your [herdr](https://herdr.dev) spaces after your Claude Code sessions. When you
`/rename` a Claude session, the space it runs in is renamed to match, so you stop renaming
things twice.

- `/rename My feature` in Claude → the space becomes **My feature** within ~2 seconds
- Space with several tabs? Only the tab that Claude pane is in gets renamed
- Resuming a session that already has a name renames its space when herdr starts
- Sessions you never `/rename` are left alone, so names you set by hand stay

This is an unofficial community plugin. It is not affiliated with or endorsed
by herdr or Anthropic.

## Requirements

- herdr 0.9.3 or newer (the only version tested so far)
- herdr's built-in Claude integration (`herdr integration install claude`), which tells herdr
  which Claude session runs in each pane
- `python3` on your PATH. It only uses the standard library.
- Linux or macOS

## Install

```sh
herdr plugin install pradyb/herdr-session-title
```

Or from a local clone, for development: `herdr plugin link "$PWD"`.

herdr runs a plugin's startup hook only when a server starts, not when a plugin is installed
or linked. So right after installing, either restart herdr or start it by hand:

```sh
herdr plugin action invoke start --plugin pradyb.session-title
```

It's safe to run this again: if it's already running for that herdr session, it does nothing.
Run it in each herdr session you have open (each one has its own server).

## How it works

herdr has no event for a Claude rename, so the plugin watches for it:

1. The startup hook (or the `start` action) launches one background process per herdr server
   and returns. herdr runs startup hooks once and does not keep them alive, so the plugin
   detaches itself.
2. Every 2 seconds it asks herdr for the Claude panes and the session each one runs.
3. It reads the lines added to each session's transcript (`~/.claude/projects/*/<session>.jsonl`)
   since the last check, and looks for the title `/rename` writes there. Only new bytes are
   read, so large transcripts stay cheap.
4. When a session's title changes, it renames the space, or the pane's tab if the space has
   more than one tab.
5. It exits when the herdr server stops.

If you use `CLAUDE_CONFIG_DIR`, set it in the environment that starts herdr, and the plugin
looks for transcripts there instead of `~/.claude`.

## Limits

- **Up to ~2 seconds' delay**, because it checks on a timer. Change `POLL` in `session_title.py`.
- **Tab or space is decided at rename time.** Add a second tab to a space after naming a
  session and nothing moves; the next `/rename` goes to the tab.
- **Two Claude panes in one single-tab space:** the most recent rename wins.
- **Only one way:** renaming a space in herdr doesn't rename the Claude session.
- **Claude Code only.** Other agents don't write a session title herdr can read.

## Troubleshooting

- **Nothing gets renamed:** check that it's running with `pgrep -fl "session_title.py --daemon"`.
  If not, run the `start` action above.
- **Log:** `daemon.log` in the plugin's state directory, by default
  `~/.local/state/herdr/plugins/pradyb.session-title/daemon.log`. Each rename is logged as `workspace w1 -> My feature`.
- **Pane not picked up:** `herdr agent list` should show an `agent_session` for that Claude pane.
  If it's empty, install herdr's Claude integration and restart that Claude session.

## License

[MIT](LICENSE)
