# Copilot instructions

- This repository contains integration tests for Instaloader behavior that requires live Instagram access. Do not add offline tests.
- Never run live integration tests in CI. CI checks formatting and types, then validates test collection only.
- Treat `instaloader-requirements.md` as the source of truth for coverage. Requirements should describe observable behavior, not implementation details.
- Keep requirement IDs, authentication variants, importance levels, and tests aligned. Cover further-page behavior whenever a requirement calls for it; do not stop at first-page coverage.
- State public and private profile behavior explicitly. Private-profile tests assume the logged-in account follows the target profile.
- Keep tests focused on Instagram-facing behavior. Do not add password CLI options or local session-file round-trip checks as substitutes for integration coverage. Use the existing credential and target configuration.
- Prefer existing fixtures and shared helpers. Avoid redundant checks when configuration already enforces an invariant, unnecessary intermediate values, and abstractions that do not simplify the tests. Search for all references after renaming.
- Prefer the simplest solution that fully addresses the request; avoid speculative generalization and unnecessary complexity.
- Target Python 3.14 or newer. Use modern typing without `from __future__ import annotations`; follow Black and mypy.
- Validate changes with the existing project checks and `pytest --collect-only`. Do not run live tests without explicit configuration.
