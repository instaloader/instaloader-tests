# instaloader-tests

Integration tests for Instaloader features that require Instagram access.

This repository aims to provide mostly automated regression tests for Instaloader's
integration behavior. The integration requirements are documented in
`instaloader-requirements.md` and focus only on Instagram-access-related behavior.

The test suite is intended to be user-friendly, modern Python style compliant
(typing, Black formatting), and practical without unnecessary over-engineering.
It is expected to support:

- execution up to a configurable importance level;
- parametrized test targets (e.g., public/private profiles, posts with comments);
- coverage of features regardless of how `Post` and `Profile` instances are created.

## Concept

This repository is intended to hold only integration tests that access Instagram.
It does not aim to provide offline or purely local tests.

`instaloader-requirements.md` is the source of truth for what behavior shall be
covered. The test suite should be organized around those requirements and make it
easy to see which integration behavior is already covered and which still needs a
test.

## Project Structure

The project uses a small pytest-based layout with clear separation between test
cases and shared support code:

```text
tests/
  conftest.py
  integration/
    test_profiles.py
    test_posts.py
  support/
    credentials.py
    targets.py
    requirements_map.py
```

This structure is meant to replace the legacy monolithic test module with a suite
that is easier to extend and discuss feature by feature.

## Relation to the Legacy Tests

The previous tests that motivate this repository are:

- <https://github.com/instaloader/instaloader/blob/master/test/instaloader_unittests.py>

That legacy module mixes different kinds of Instagram-backed checks in one
`unittest` file. The new repository should instead:

- separate tests by feature area;
- distinguish anonymous and logged-in scenarios within the integration suite;
- allow configurable execution by importance level;
- make documented requirements easier to map to individual tests.

## CI Scope

Continuous integration is intended to validate the test project itself, not to run
Instagram-backed integration scenarios.

In particular, CI should be limited to things such as:

- installing the project and test dependencies;
- running local project-quality checks such as formatting and type validation;
- validating that the test suite imports and collects correctly;
- running additional repository-quality checks that stay independent of live
  Instagram access.

The integration tests themselves must not run in CI. This is a hard constraint for
this repository and should be reflected in the eventual test configuration, for
example by keeping those tests behind explicit markers or explicit local-only
commands that CI never enables.

The current GitHub Actions workflow therefore installs the project, runs Black
and mypy, and performs pytest collection only.

## Integration Test Execution

Integration tests are intended to be executed manually in a developer-controlled
environment.

Execution is expected to require:

- locally prepared credentials, cookies, or session files;
- locally configured test targets;
- explicit selection of the desired execution scope.

The suite should support:

- anonymous-only execution;
- logged-in execution;
- selection up to a configurable importance level;
- running individual feature groups or narrower subsets while iterating on a
  specific requirement.

This keeps the repository practical for real-world Instagram integration checks
while avoiding any assumption that the tests are safe or stable enough for
unattended CI execution.

### Running the suite locally

Install the project and collect the test suite:

```bash
python -m pip install poetry
poetry install --no-root --extras dev
poetry run pytest --collect-only
```

Run the currently implemented anonymous integration tests:

```bash
poetry run pytest \
  --target-public-profile nasa \
  --target-public-shortcode CxD6K_4M8QK
```

Run logged-in tests with Instaloader's default session-file path:

```bash
poetry run pytest \
  --username youraccount \
  --authentication logged_in \
  --target-public-profile nasa \
  --target-public-shortcode CxD6K_4M8QK
```

Run only anonymous tests:

```bash
poetry run pytest \
  --authentication anonymous \
  --target-public-profile nasa \
  --target-public-shortcode CxD6K_4M8QK
```

Run a wider slice of the suite up to a higher importance level:

```bash
poetry run pytest \
  --max-importance high \
  --target-public-profile nasa \
  --target-public-shortcode CxD6K_4M8QK
```

If `--username` is set, the suite uses Instaloader's default session-file path
unless `--sessionfile` overrides it.

Use `--max-importance` to widen execution beyond critical tests as more coverage
is added.

Use `--authentication` to restrict execution to `anonymous` or `logged_in`
tests.
