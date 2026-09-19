from collections.abc import Generator
from collections import defaultdict
from pathlib import Path
from typing import Any, cast

import instaloader
import pytest

from tests.support.credentials import SessionCredentials, load_session_credentials
from tests.support.requirements_map import (
    Authentication,
    REQUIREMENTS,
    Importance,
    is_importance_enabled,
)
from tests.support.post_checkers import (
    POST_CHECKERS,
    PostChecker,
    PostCheckerName,
    load_post_checker,
)
from tests.support.targets import (
    IntegrationTargets,
    TARGET_OPTIONS,
    load_targets,
    target_option,
)

pytest_plugins: list[str] = []
_SUMMARY_OUTCOME_ORDER = ("failed", "error", "passed", "skipped", "xfailed", "xpassed")
_REPORT_IMPORTANCE_PROPERTY = "importance"
_REPORT_SUMMARY_KEY_PROPERTY = "summary_key"
_SUMMARY_OUTCOME_PRECEDENCE = {
    "failed": 0,
    "error": 1,
    "xpassed": 2,
    "passed": 3,
    "xfailed": 4,
    "skipped": 5,
}


def _authentication_label(item: pytest.Item) -> Authentication | None:
    for authentication in Authentication:
        if item.get_closest_marker(authentication.value):
            return authentication
    return None


def _importance_label(item: pytest.Item) -> str:
    importance_marker = item.get_closest_marker("importance")
    if importance_marker:
        if not importance_marker.args:
            raise pytest.UsageError(
                f"importance marker on {item.nodeid} requires a level argument"
            )
        level = str(importance_marker.args[0]).upper()
        try:
            return Importance[level].name.lower()
        except KeyError as error:
            raise pytest.UsageError(
                f"Unknown required importance level: {importance_marker.args[0]}"
            ) from error
    return "unmarked"


def _report_outcome_category(report: Any) -> str | None:
    wasxfail = getattr(report, "wasxfail", None)
    if getattr(report, "skipped", False):
        if wasxfail:
            return "xfailed"
        return "skipped"
    if getattr(report, "passed", False):
        if report.when != "call":
            return None
        if wasxfail:
            return "xpassed"
        return "passed"
    if getattr(report, "failed", False):
        if report.when == "call":
            return "failed"
        return "error"
    return None


@pytest.hookimpl()
def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--max-importance",
        action="store",
        default=Importance.VERYLOW.name.lower(),
        choices=[importance.name.lower() for importance in Importance],
        help="maximum importance level to execute",
    )
    parser.addoption(
        "--sessionfile",
        action="store",
        default=None,
        help="optional path to an Instaloader session file override for logged-in tests",
    )
    parser.addoption(
        "--username",
        action="store",
        default=None,
        help="Instagram username that matches --sessionfile",
    )
    for target in TARGET_OPTIONS.values():
        parser.addoption(
            target.option_name,
            action="store",
            default=None,
            help=target.help_text,
        )
    parser.addoption(
        "--authentication",
        action="store",
        default="all",
        choices=["all", *[authentication.value for authentication in Authentication]],
        help="authentication scope to execute: all, anonymous, or logged_in only",
    )
    parser.addoption(
        "--post-checker",
        action="store",
        default="download",
        choices=sorted(POST_CHECKERS),
        help="post validation mode to execute: download (default) or fast",
    )
    parser.addoption(
        "--max-items",
        action="store",
        type=int,
        default=50,
        help="exclusive stop index for further-pages list slices (after first 12 items)",
    )


@pytest.hookimpl()
def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    max_importance = config.getoption("--max-importance")
    authentication_scope = config.getoption("--authentication")
    requested_authentication = (
        None if authentication_scope == "all" else Authentication(authentication_scope)
    )
    for item_index, item in enumerate(items):
        setattr(item, "_instaloader_summary_key", f"{item_index}:{item.nodeid}")
        requirement_marker = item.get_closest_marker("requirement_id")
        if requirement_marker:
            requirement_id = requirement_marker.args[0]
            if requirement_id not in REQUIREMENTS:
                raise pytest.UsageError(
                    f"Unknown requirement_id marker: {requirement_id}"
                )

        importance_marker = item.get_closest_marker("importance")
        if importance_marker and not is_importance_enabled(
            max_importance, _importance_label(item)
        ):
            item.add_marker(
                pytest.mark.skip(
                    reason=f"requires --max-importance >= {_importance_label(item)}"
                )
            )

        authentication_label = _authentication_label(item)
        if (
            requested_authentication is not None
            and authentication_label != requested_authentication
        ):
            if authentication_label is None:
                reason = (
                    "missing authentication marker; skipped because "
                    f"--authentication={authentication_scope} was requested"
                )
            else:
                reason = f"requires --authentication={authentication_label.value}"
            item.add_marker(pytest.mark.skip(reason=reason))
        if (
            authentication_label
            and f"[{authentication_label.value}]" not in item.nodeid
        ):
            item._nodeid = f"{item.nodeid}[{authentication_label.value}]"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[None]
) -> Generator[None, None, None]:
    outcome = yield
    report = cast(Any, outcome).get_result()
    if _report_outcome_category(report) is None:
        return
    report.user_properties.append(
        (
            _REPORT_SUMMARY_KEY_PROPERTY,
            getattr(item, "_instaloader_summary_key"),
        )
    )
    report.user_properties.append(
        (_REPORT_IMPORTANCE_PROPERTY, _importance_label(item))
    )


@pytest.hookimpl()
def pytest_terminal_summary(terminalreporter: Any) -> None:
    grouped_counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    seen_reports: set[int] = set()
    test_outcomes: dict[str, tuple[str, str]] = {}
    for reports in terminalreporter.stats.values():
        for report in reports:
            report_id = id(report)
            if report_id in seen_reports:
                continue
            seen_reports.add(report_id)
            outcome = _report_outcome_category(report)
            if outcome is None:
                continue
            importance = next(
                (
                    value
                    for key, value in getattr(report, "user_properties", [])
                    if key == _REPORT_IMPORTANCE_PROPERTY
                ),
                "unmarked",
            )
            summary_key = next(
                (
                    value
                    for key, value in getattr(report, "user_properties", [])
                    if key == _REPORT_SUMMARY_KEY_PROPERTY
                ),
                str(report.nodeid),
            )
            current = test_outcomes.get(str(summary_key))
            if (
                current is None
                or _SUMMARY_OUTCOME_PRECEDENCE[outcome]
                < _SUMMARY_OUTCOME_PRECEDENCE[current[0]]
            ):
                test_outcomes[str(summary_key)] = (outcome, str(importance))

    for outcome, importance in test_outcomes.values():
        grouped_counts[importance][outcome] += 1

    ordered_levels = [importance.name.lower() for importance in Importance]
    summary_levels = [
        level
        for level in ordered_levels + ["unmarked"]
        if sum(grouped_counts[level].values()) > 0
    ]
    if not summary_levels:
        return

    terminalreporter.section("results by criticality")
    for level in summary_levels:
        counts = grouped_counts[level]
        parts = [
            f"{outcome}={counts[outcome]}"
            for outcome in _SUMMARY_OUTCOME_ORDER
            if counts.get(outcome)
        ]
        total = sum(counts.values())
        terminalreporter.write_line(f"{level}: total={total}, " + ", ".join(parts))


@pytest.fixture(scope="session")
def integration_targets(pytestconfig: pytest.Config) -> IntegrationTargets:
    return load_targets(
        public_profile=pytestconfig.getoption(
            target_option("public_profile").option_name
        ),
        private_profile=pytestconfig.getoption(
            target_option("private_profile").option_name
        ),
        public_shortcode=pytestconfig.getoption(
            target_option("public_shortcode").option_name
        ),
        hashtag=pytestconfig.getoption(target_option("hashtag").option_name),
    )


@pytest.fixture(scope="session")
def session_credentials(pytestconfig: pytest.Config) -> SessionCredentials | None:
    return load_session_credentials(
        username=pytestconfig.getoption("--username"),
        sessionfile=pytestconfig.getoption("--sessionfile"),
    )


@pytest.fixture(scope="session")
def max_items(pytestconfig: pytest.Config) -> int:
    max_items_option = int(pytestconfig.getoption("--max-items"))
    if max_items_option <= 12:
        raise pytest.UsageError("--max-items must be greater than 12")
    return max_items_option


@pytest.fixture()
def output_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture(scope="session")
def anonymous_instaloader() -> instaloader.Instaloader:
    return instaloader.Instaloader(
        quiet=True, dirname_pattern="{target}", filename_pattern="{shortcode}"
    )


@pytest.fixture(scope="session")
def logged_in_instaloader(
    session_credentials: SessionCredentials | None,
) -> instaloader.Instaloader:
    if session_credentials is None:
        pytest.skip("configure --username for logged-in tests")
    if not session_credentials.session_file.exists():
        pytest.skip(f"session file not found: {session_credentials.session_file}")
    loader = instaloader.Instaloader(
        quiet=True, dirname_pattern="{target}", filename_pattern="{shortcode}"
    )
    loader.load_session_from_file(
        session_credentials.username, str(session_credentials.session_file)
    )
    return loader


@pytest.fixture()
def active_authentication(request: pytest.FixtureRequest) -> Authentication:
    return request.param


@pytest.fixture()
def active_instaloader(
    active_authentication: Authentication,
    anonymous_instaloader: instaloader.Instaloader,
    logged_in_instaloader: instaloader.Instaloader,
) -> instaloader.Instaloader:
    if active_authentication is Authentication.ANONYMOUS:
        return anonymous_instaloader
    if active_authentication is Authentication.LOGGED_IN:
        return logged_in_instaloader
    raise pytest.UsageError(f"Unknown authentication variant: {active_authentication}")


@pytest.fixture(scope="session")
def post_checker_name(pytestconfig: pytest.Config) -> PostCheckerName:
    return pytestconfig.getoption("--post-checker")


@pytest.fixture(scope="session")
def post_checker(post_checker_name: PostCheckerName) -> PostChecker:
    return load_post_checker(post_checker_name)
