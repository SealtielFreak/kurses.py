# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Migrated the project to use `uv` for environment and dependency management.
- Added `pyproject.toml` with project metadata, build system, and tool configuration.
- Added optional dependency extra `[sdl2]` to install `pysdl2` and `pysdl2-dll`.
- Configured `ruff` for linting and import sorting.
- Configured `mypy` for static type checking.
- Added `mkdocs` with the `material` theme and a starter `docs/index.md`.
- Added `.python-version` for local development with `uv`.
- Added development instructions to `README.md`.
- Added this `CHANGELOG.md`.
- Added full MkDocs documentation with `mkdocstrings` API reference.
- Added installation, quickstart and ten tutorial guides based on the bundled examples.
- Added `docs/changelog.md` included in the documentation site.

### Changed

- Moved the package source from `kurses/` to `src/kurses/`.
- Updated `numpy` dependency from `~=2.0.2` to `>=1.24.0,<2.0` to maintain Python 3.8 compatibility.
- Updated `.gitignore` to ignore `.venv/`, `uv.lock`, `.python-version`, `.ruff_cache/`, and MkDocs `site/` output.
- Applied minor linting fixes across the codebase (sorted imports, explicit re-exports, fixed `raise ""`, replaced a lambda with a `def`, etc.).

### Removed

- Removed `setup.py` in favor of `pyproject.toml`.
- Removed `mypy.ini`; mypy configuration now lives in `pyproject.toml`.
- Removed `requirements.txt`; runtime and development dependencies now live in `pyproject.toml`.

## [0.1.2.0] - 2024-XX-XX

### Added

- Initial public release of `kurses-py`.
- SDL2-based virtual terminal implementation.
- Text buffer with color, cursor, and style support.
- Audio support through SDL2 mixer (effects and music).
- Joystick, sensor, battery, and touch interface abstractions.
