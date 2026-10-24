# instaloader-tests

Integration tests for Instaloader features that require Instagram access.

This repository aims to provide mostly automated regression tests for Instaloader's
integration behavior. Some behaviors, particularly interactive session creation,
are not practical to cover with automated tests and may require manual validation.
The integration requirements are documented in `tests/support/requirements_map.py`
and focus only on Instagram-access-related behavior.

The test suite is intended to be user-friendly, modern Python style compliant
(typing, Black formatting), and practical without unnecessary over-engineering.
It is expected to support:

- execution up to a configurable importance level;
- parametrized test targets (e.g., public/private profiles, posts with comments);
- coverage of features regardless of how `Post` and `Profile` instances are created.

## AI usage

This project was developed with substantial assistance from AI coding agents
(GitHub Copilot). All changes are reviewed by the maintainer.

## Concept

This repository is intended to hold only integration tests that access Instagram.
It does not aim to provide offline or purely local tests.

`tests/support/requirements_map.py` is the source of truth for the integration
behaviors in scope; it does not imply that every behavior must have an automated
test. The test suite maps automated coverage to those requirements, while some
requirements may remain uncovered because they need manual validation or are not
practical to automate.

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

Profile-by-ID tests use the existing public/private profile targets to obtain
their IDs, then check that `Profile.from_id()` resolves the expected profile and
its current username without a cached ID lookup. This covers the ID-resolution
behavior needed to detect profile name changes and rename target directories.
Logged-in public and private lookups have critical importance; anonymous public
lookups have high importance. Private-profile tests assume that the logged-in
account follows the target profile.

Empty paging results are skipped only when no reported count indicates missing
items. Paging checks use the iterator's count when available, or an explicit count
from the profile, post, or story. If a first-page iterator is empty despite a
positive count, or a further-pages iterator stops before the reported count
without yielding any items beyond the first 12, the test fails instead of skipping.
Comment counts include replies, so further-page comment checks use them only to
detect a completely empty iterator, not to require more top-level comments.
When no count is available, empty results continue to skip.

The short test summary lists skipped tests individually, with the test file,
test name (including its authentication variant), and skip reason, matching the
format used for failures rather than grouping skips by their source location.

#### Invocation reference

| Option                      | Accepted values / default                                |
|-----------------------------|----------------------------------------------------------|
| `--authentication`          | `all` (default), `anonymous`, `logged_in`                |
| `--max-importance`          | `verylow` (default), `low`, `medium`, `high`, `critical` |
| `--post-checker`            | `download` (default), `fast`                             |
| `--username`                | Instagram username                                       |
| `--sessionfile`             | Filesystem path                                          |
| `--target-public-profile`   | Public Instagram username                                |
| `--target-private-profile`  | Private Instagram username                               |
| `--target-public-shortcode` | Public post shortcode                                    |
| `--target-hashtag`          | Hashtag name                                             |
| `--target-location-id`      | Instagram location ID                                    |
| `--max-items`               | Stop index for iterators (default 50)                    |

At the end of each run, pytest lists requirements without any collected test
in an `uncovered requirements` section. This is coverage information, not an
assertion that every listed requirement should be automated. Pytest also prints a
`results by criticality` summary that groups the observed outcomes by importance level.

`--post-checker=download` keeps the stronger default coverage by calling
`download_post()` on exercised posts. `--post-checker=fast` switches to a
lighter check that verifies the same caption/date access used by the single-post
test.

#### Testing a local Instaloader checkout

By default the suite imports the installed `instaloader` package. To test a local
checkout instead, make that checkout the imported copy, either by installing it
editable into the project environment:

```bash
poetry run pip install -e /path/to/instaloader
```

or by putting it on `PYTHONPATH` (the checkout root, containing the `instaloader/`
directory):

```bash
PYTHONPATH=/path/to/instaloader poetry run pytest [options...]
```

Verify which copy is used with
`poetry run python -c "import instaloader; print(instaloader.__file__)"`
(with `PYTHONPATH`, prefix the command accordingly). Re-running `poetry install` may
replace an editable install with the released package.

#### Detailed error output

Tracebacks are shortened by default (`--tb=line`). For full details on failures and
setup errors, pass pytest's own options, which override the defaults:

```bash
poetry run pytest --tb=long --showlocals --log-level=DEBUG [options...]
```

#### Example commands

Anonymous smoke run against the currently implemented public-profile and single-
post coverage:

```bash
poetry run pytest \
  --authentication=anonymous \
  --post-checker=fast \
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

Focused anonymous run that limits execution to higher-importance tests:

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
