# Copilot Instructions for Inspyre Toolbox

This file provides machine-readable context for AI coding agents (GitHub Copilot, Claude, etc.) working in this repository.

---

## Project Overview

**Inspyre Toolbox** is a Python utility library (package name: `inspyre-toolbox`) built for Python 3.10+. It provides 27+ submodules covering timers, byte conversion, humanization, process management, CLI tools, logging, and more. It is maintained by Inspyre Softworks and managed with **Poetry**.

---

## Repository Structure

```
inspyre_toolbox/       # Main package — all submodules live here
tests/                 # pytest test suite (test_*.py files)
.github/               # Workflows, issue templates, PR template
pyproject.toml         # Project metadata and dependencies (Poetry)
inspyre_toolbox/common/about/version/VERSION  # Authoritative version file
```

---

## Tech Stack

| Concern | Tool |
|---|---|
| Language | Python 3.10+ |
| Package manager | Poetry |
| Test runner | pytest (`poetry run pytest`) |
| CI | GitHub Actions (`.github/workflows/`) |
| Version source | `inspyre_toolbox/common/about/version/VERSION` |

---

## Critical Rules for AI Agents

### Version Management
- The **single source of truth** for the runtime version is `inspyre_toolbox/common/about/version/VERSION` (plain text, e.g. `1.6.0-dev.24`).
- `pyproject.toml` must always match, prefixed with `v`: `version = "v1.6.0-dev.24"`.
- **Always update both files together** when bumping the version. Never edit `__init__.py` to change the version.

### Branching
- **Never push directly to `main`** — all changes must go through a PR branch.
- Branch naming: `feature/<name>`, `fix/<name>`, `copilot/<name>`, `docs/<name>`, `1.6.0-devN`.
- Prefer **merge commits** over squashing when integrating dev branches (preserves history).
- **Do not delete branches** unless explicitly instructed.

### Commits
Use gitmoji-prefixed conventional commits:
```
✨ feat(<scope>): <summary>
🐛 fix(<scope>): <summary>
🔩 chore(<scope>): <summary>
📝 docs(<scope>): <summary>
♻️ refactor(<scope>): <summary>
✅ test(<scope>): <summary>
🔒 security(<scope>): <summary>
```

### Code Changes
- Make **minimal, surgical changes** — only change what is required by the task.
- Do not refactor unrelated code.
- Add type hints to all public functions and methods.
- Write docstrings (Google or NumPy style) for all public symbols.
- Max line length: 120 characters.

### Testing
- Run `poetry run pytest` to validate changes.
- New features must include tests in `tests/test_*.py`.
- Bug fixes should include a regression test.
- **Do not remove or skip existing tests.**

### Dependencies
- Do not introduce new dependencies unless the task explicitly requires them.
- If adding a dependency, add it via `poetry add <package>` and check for known vulnerabilities.

---

## Key Submodules

| Module | Purpose |
|---|---|
| `chrono` | Timers, sleep utilities |
| `cli` | CLI entry points (`ist-bytes-converter`, `ist-add-to-path`, `ist-version-tool`) |
| `common.about.version` | Version reading and PyPI version comparison |
| `conversions` | Unit conversions (e.g. ByteConverter) |
| `humanize` | Human-friendly number formatting |
| `log_engine` | Centralised logging (inspy-logger) |
| `proc_man` | Process management utilities |
| `pypi` | PyPI package version checking |
| `solve_kit` | Math/calculation helpers |
| `syntactic_sweets` | Context managers, output suppression |
| `ver_man` | Version parsing, PyPI version info, argparse actions |

---

## Pull Request Checklist (for AI agents)

Before opening or updating a PR:
1. All existing tests pass (`poetry run pytest`)
2. Version files are in sync if the version was changed
3. Commit messages follow the gitmoji format
4. No unrelated files are changed
5. PR description uses the template (`.github/PULL_REQUEST_TEMPLATE.md`)
