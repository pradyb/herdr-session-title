# Changelog

All notable changes to herdr-session-title will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0]

First release.

### Added
- Renames a space when the Claude Code session in it is renamed with `/rename`, or only the pane's tab when the space has several tabs
- Sessions that already have a title are applied when herdr starts; sessions without one are left alone
- Startup hook that launches one detached background process per herdr server, plus a `start` action for when the plugin is linked into a running server
- Repository setup: license, contributing guide, security policy, issue and PR templates, code owners, and CI on Python 3.8 and the latest 3.x
