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

The suite is driven entirely through pytest CLI options:

```bash
poetry run pytest [pytest selection options...] [instaloader test options...]
```

Tests that need data you did not provide are skipped with a short explanation.
For example, logged-in tests are skipped unless `--username` is set, and
target-specific tests are skipped unless their corresponding `--target-*`
option is configured.

#### Invocation reference

| Option                      | Accepted values / default                                |
|-----------------------------|----------------------------------------------------------|
| `--authentication`          | `all` (default), `anonymous`, `logged_in`                |
| `--max-importance`          | `critical` (default), `high`, `medium`, `low`, `verylow` |
| `--username`                | Instagram username                                       |
| `--sessionfile`             | Filesystem path                                          |
| `--target-public-profile`   | Public Instagram username                                |
| `--target-private-profile`  | Private Instagram username                               |
| `--target-public-shortcode` | Public post shortcode                                    |
| `--target-public-hashtag`   | Public hashtag name                                      |
| `--saved-posts-further-pages-end` | Exclusive end index for saved-posts further-pages test (`50` default, must be `> 12`) |

At the end of each run, pytest prints a `results by criticality` summary that
groups the observed outcomes by importance level.

#### Example commands

Anonymous smoke run against the currently implemented public-profile and single-
post coverage:

```bash
poetry run pytest \
  --authentication=anonymous \
  --target-public-profile=nasa \
  --target-public-shortcode=CxD6K_4M8QK
```

Logged-in run that exercises public, private, and account-owned coverage using
Instaloader's default session-file path:

```bash
poetry run pytest \
  --authentication=logged_in \
  --username=youraccount \
  --target-public-profile=nasa \
  --target-private-profile=your-private-target \
  --target-public-shortcode=CxD6K_4M8QK
```

Logged-in run with an explicit session file, focused on saved-post coverage
while iterating on that feature area:

```bash
poetry run pytest \
  tests/integration/test_saved_posts.py \
  --authentication=logged_in \
  --username=youraccount \
  --sessionfile=/absolute/path/to/session-youraccount
```

Broader anonymous run that also enables tests marked above the default
`critical` level:

```bash
poetry run pytest \
  --authentication=anonymous \
  --max-importance=high \
  --target-public-profile=nasa \
  --target-public-shortcode=CxD6K_4M8QK
```

Dry-run collection for a planned logged-in execution, useful to confirm which
cases would run before hitting Instagram:

```bash
poetry run pytest --collect-only \
  --authentication=logged_in \
  --username=youraccount \
  --target-public-profile=nasa \
  --target-private-profile=your-private-target \
  --target-public-shortcode=CxD6K_4M8QK
```
