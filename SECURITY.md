# Security Policy

## Supported Versions

Only the latest release (and the latest commit on `main`) is actively supported with security fixes.

## Reporting a Vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

Report security issues privately using
[GitHub's private vulnerability reporting](https://github.com/pradyb/herdr-session-title/security/advisories/new)
or by emailing **pradeep.devlabs@gmail.com**.

Include:
- A description of the vulnerability and its potential impact
- Steps to reproduce (proof-of-concept if possible)
- Your suggested fix or mitigation (optional)

You can expect an acknowledgement within **72 hours**.

## Scope

This plugin reads Claude Code transcripts, which can hold anything from your sessions. It only
extracts the session title from them, keeps nothing else, and never sends anything off your
machine: its only output is a herdr rename and a line in its local log.

A session title is untrusted text. It is passed to herdr as a single argument, never through a shell.

In scope: any way a session title or transcript can run commands or inject arguments, make the
plugin read or write files other than transcripts and its own state directory, or leak transcript
content beyond the title.

Out of scope: vulnerabilities in herdr itself (report those to the herdr project) or in Claude Code.
