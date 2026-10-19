#!/usr/bin/env python3
"""herdr session-title: name a herdr workspace after its Claude Code session.

The herdr startup hook (or the "start" action) spawns a detached daemon, one per
herdr server, and returns: herdr runs startup hooks once, it does not supervise
them. Every POLL seconds it reads the newly appended
part of each Claude pane's transcript for `/rename` titles (custom-title lines)
and renames that pane's workspace to match (its tab, if the workspace has several). Standard library only.
"""
import glob
import hashlib
import json
import os
import subprocess
import sys
import time

try:
    import fcntl

    def lock(f, block=True):
        fcntl.flock(f, fcntl.LOCK_EX | (0 if block else fcntl.LOCK_NB))
except ImportError:  # Windows
    import msvcrt

    def lock(f, block=True):
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK if block else msvcrt.LK_NBLCK, 1)

# Detach a child from herdr's process tree: new session on POSIX, CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP on Windows (hidden console, so child herdr calls do not flash windows).
DETACH = {"creationflags": 0x08000200} if os.name == "nt" else {"start_new_session": True}

HERDR = os.environ.get("HERDR_BIN_PATH") or "herdr"
SOCKET = os.environ.get("HERDR_SOCKET_PATH")
PROJECTS = os.path.join(os.path.expanduser(os.environ.get("CLAUDE_CONFIG_DIR", "~/.claude")), "projects")
STATE_DIR = os.environ.get("HERDR_PLUGIN_STATE_DIR") or os.path.expanduser("~/.cache/herdr-session-title")
POLL = 2  # ponytail: polling, herdr has no event for a Claude /rename


def herdr(*args):
    out = subprocess.run([HERDR, *args], capture_output=True, encoding="utf-8", errors="replace").stdout
    try:
        return json.loads(out).get("result") or {}
    except ValueError:
        return {}


def latest_title(path, state):
    """Newest customTitle in the transcript, reading only bytes added since the last call."""
    offset, title = state.get(path, (0, None))
    try:
        with open(path, "rb") as f:
            f.seek(offset)
            data = f.read()
    except OSError:
        return title
    end = data.rfind(b"\n") + 1  # leave a half-written last line for next time
    for line in data[:end].splitlines():
        if b'"custom-title"' in line:
            try:
                title = json.loads(line).get("customTitle") or title
            except ValueError:
                pass
    state[path] = (offset + end, title)
    return title


def transcript(session, paths):
    if session.get("kind") == "path":
        return session.get("value")
    sid = session.get("value")
    if sid and sid not in paths:
        found = glob.glob(os.path.join(PROJECTS, "*", sid + ".jsonl"))
        if found:
            paths[sid] = found[0]
    return paths.get(sid)


def target(agent):
    """The pane's tab if its workspace has several tabs, else the workspace."""
    ws = herdr("workspace", "get", agent["workspace_id"]).get("workspace") or {}
    if ws.get("tab_count", 1) > 1:
        return "tab", agent["tab_id"]
    return "workspace", agent["workspace_id"]


def tick(state, paths, applied):
    for agent in herdr("agent", "list").get("agents", []):
        path = transcript(agent.get("agent_session") or {}, paths)
        if not path:
            continue
        title = latest_title(path, state)
        if title and applied.get(path) != title:
            kind, target_id = target(agent)
            herdr(kind, "rename", target_id, title)
            applied[path] = title
            print(f"{kind} {target_id} -> {title}", flush=True)


def spawn():
    """Start the daemon detached from herdr's startup hook, logging to the state dir."""
    os.makedirs(STATE_DIR, exist_ok=True)
    log = open(os.path.join(STATE_DIR, "daemon.log"), "a")
    subprocess.Popen([sys.executable, os.path.abspath(__file__), "--daemon"], **DETACH,
                     stdin=subprocess.DEVNULL, stdout=log, stderr=log)


def daemon():
    os.makedirs(STATE_DIR, exist_ok=True)
    key = hashlib.sha1((SOCKET or "").encode()).hexdigest()[:12]
    lock_f = open(os.path.join(STATE_DIR, f"daemon-{key}.lock"), "w")
    try:
        lock(lock_f, block=False)
    except OSError:
        return  # a daemon is already watching this herdr server
    print(f"watching {SOCKET}", flush=True)
    state, paths, applied = {}, {}, {}
    while not SOCKET or os.path.exists(SOCKET):
        tick(state, paths, applied)
        time.sleep(POLL)


if __name__ == "__main__":
    daemon() if "--daemon" in sys.argv else spawn()
