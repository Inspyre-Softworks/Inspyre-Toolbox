# Contributing to Inspyre Toolbox

Thank you for your interest in contributing to **Inspyre Toolbox**! This document describes how to contribute effectively — whether you are a human developer or an AI coding agent.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Branching Strategy](#branching-strategy)
- [Making Changes](#making-changes)
- [Commit Message Format](#commit-message-format)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Version Numbering](#version-numbering)
- [Testing](#testing)
- [Style Guide](#style-guide)
- [For AI Agents](#for-ai-agents)

---

## Code of Conduct

By participating in this project you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

---

## Getting Started

### Prerequisites

- Python **3.10** or higher
- [Poetry](https://python-poetry.org/) for dependency management

### Setup

```bash
git clone https://github.com/Inspyre-Softworks/Inspyre-Toolbox.git
cd Inspyre-Toolbox
poetry install
```

### Running Tests

```bash
poetry run pytest
```

---

## Branching Strategy

| Branch pattern | Purpose |
|---|---|
| `main` | Stable, release-ready code |
| `1.6.0-devN` | Active development for the upcoming release cycle |
| `feature/<name>` | Isolated feature work |
| `fix/<name>` | Bug fixes |
| `copilot/<name>` | AI-agent-driven changes |
| `docs/<name>` | Documentation-only changes |

- **Always branch from `main`** unless working on an in-progress dev cycle.
- **Never push directly to `main`** — all changes must go through a pull request.
- Delete branches after they are merged.

---

## Making Changes

1. Create a branch with a descriptive name (see table above).
2. Make your changes in small, focused commits.
3. Keep each commit to a single logical change.
4. Add or update tests for any changed behaviour.
5. Update the relevant docstrings and documentation.

---

## Commit Message Format

This project uses **gitmoji**-prefixed conventional commits:

```
<emoji> <type>(<scope>): <short summary>
```

| Emoji | Type | When to use |
|---|---|---|
| ✨ | `feat` | New feature |
| 🐛 | `fix` | Bug fix |
| 🔩 | `chore` | Maintenance, version bumps, CI |
| 📝 | `docs` | Documentation only |
| ♻️ | `refactor` | Code restructuring without behaviour change |
| 🚀 | `perf` | Performance improvement |
| ✅ | `test` | Adding or fixing tests |
| 🔒 | `security` | Security fix |

**Examples:**

```
✨ feat(chrono): add interruptible sleep with precision control
🐛 fix(pypi): guard None/empty response when offline
🔩 chore(version): bump version to 1.6.0-dev.24
✅ test(pypi): add offline mode tests for PyPiVersionInfo
```

---

## Pull Request Guidelines

- Use the **pull request template** — fill in every section.
- Link the relevant issue(s) with `Closes #<number>` or `Relates to #<number>`.
- Keep PRs focused: one concern per PR.
- All CI checks must pass before merging.
- Require at least **one approving review** from a maintainer.
- Squash only when the commit history is genuinely noisy; otherwise prefer a merge commit to preserve history.

---

## Version Numbering

Inspyre Toolbox follows **Semantic Versioning** (`MAJOR.MINOR.PATCH`) with pre-release suffixes:

```
1.6.0-dev.24   ← development build
1.6.0rc1       ← release candidate
1.6.0          ← stable release
```

The authoritative version lives in **two places** that must always be kept in sync:

| File | Format |
|---|---|
| `inspyre_toolbox/common/about/version/VERSION` | `1.6.0-dev.24` |
| `pyproject.toml` | `version = "v1.6.0-dev.24"` |

> **Do not** edit `inspyre_toolbox/common/about/version/__init__.py` to change the version — only the `VERSION` file is read at runtime.

---

## Testing

- Tests live in the `tests/` directory.
- Test files must be named `test_*.py`.
- Run the full suite with `poetry run pytest`.
- New features **must** include accompanying tests.
- Bug fixes **should** include a regression test.

---

## Style Guide

- Follow **PEP 8** for code style.
- Use **type hints** for all public functions and methods.
- Write **docstrings** (NumPy or Google style) for all public symbols.
- Keep lines to a maximum of **120 characters**.
- Prefer explicit imports over wildcard imports.

---

## For AI Agents

See [`.github/copilot-instructions.md`](.github/copilot-instructions.md) for detailed, machine-readable context about this repository's conventions, structure, and decision rules that AI coding agents should follow.

**Key rules for AI agents:**

1. **Minimal, surgical changes** — only change what is required by the task. Do not refactor unrelated code.
2. **Never push to `main` directly** — all changes go through a PR branch.
3. **Always update both version files together** (`VERSION` and `pyproject.toml`).
4. **Follow the gitmoji commit format** exactly as described above.
5. **Run existing tests** (`poetry run pytest`) to validate changes; do not remove or skip tests.
6. **Preserve branch history** — prefer merge commits over squashing when integrating dev branches.
7. **Do not delete branches** unless explicitly instructed.
8. **Do not introduce new dependencies** unless the task explicitly requires them.
