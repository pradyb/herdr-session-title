# Contributing

## Setup

```sh
git clone https://github.com/pradyb/herdr-session-title
cd herdr-session-title
herdr plugin link "$PWD"   # use your checkout as the installed plugin
herdr plugin action invoke start --plugin pradyb.session-title
```

The background process keeps running the code it started with. After changing
`session_title.py`, stop it (`pkill -f "session_title.py --daemon"`) and run the `start`
action again.

## Before opening a PR

```sh
python3 -m compileall -q .
python3 test_session_title.py
```

CI runs the same checks on Python 3.8 and the latest 3.x for every push and PR.

## Guidelines

- Keep the plugin dependency-free (Python standard library only, 3.8+).
- Add a check to `test_session_title.py` for any new transcript-reading or renaming behaviour.
- Update the README if you change user-facing behaviour.
- Bump `version` in `herdr-plugin.toml` and add an entry to `CHANGELOG.md` for any change users would notice.
- Never commit real transcript content, including in tests and fixtures.

## Questions

For usage questions or half-formed ideas, use
[Discussions](https://github.com/pradyb/herdr-session-title/discussions) rather than
the issue tracker. Issues are for reproducible bugs and concrete feature requests.
