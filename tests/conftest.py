from __future__ import annotations

from collections.abc import Generator
from collections import defaultdict
from pathlib import Path
from typing import Any, cast

import instaloader
import pytest

from tests.support.credentials import SessionCredentials, load_session_credentials
from tests.support.requirements_map import (
    REQUIREMENTS,
    Importance,
    is_importance_enabled,
)
from tests.support.targets import IntegrationTargets, load_targets

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


def _authentication_label(item: pytest.Item) -> str | None:
    if item.get_closest_marker("anonymous"):
        return "anonymous"
    if item.get_closest_marker("logged_in"):
        return "logged_in"
    return None


def _importance_label(item: pytest.Item) -> str:
    importance_marker = item.get_closest_marker("importance")
    if importance_marker:
        if not importance_marker.args:
            raise pytest.UsageError(
                f"importance marker on {item.nodeid} requires a level argument"
            )
        return str(importance_marker.args[0]).lower()
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
        default=Importance.CRITICAL.name.lower(),
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
    parser.addoption(
        "--target-public-profile",
        action="store",
        default=None,
        help="public profile username for anonymous profile tests",
    )
    parser.addoption(
        "--target-public-shortcode",
        action="store",
        default=None,
        help="public shortcode for anonymous single-post tests",
    )
    parser.addoption(
        "--target-public-hashtag",
        action="store",
        default=None,
        help="public hashtag for anonymous hashtag tests",
    )
    parser.addoption(
        "--authentication",
        action="store",
        default="all",
        choices=["all", "anonymous", "logged_in"],
        help="authentication scope to execute: all, anonymous, or logged_in only",
    )


@pytest.hookimpl()
def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    max_importance = config.getoption("--max-importance")
    authentication_scope = config.getoption("--authentication")
    for item in items:
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
            authentication_scope != "all"
            and authentication_label != authentication_scope
        ):
            if authentication_label is None:
                reason = (
                    "missing authentication marker; skipped because "
                    f"--authentication={authentication_scope} was requested"
                )
            else:
                reason = f"requires --authentication={authentication_label}"
            item.add_marker(pytest.mark.skip(reason=reason))
        if authentication_label and f"[{authentication_label}]" not in item.nodeid:
            item._nodeid = f"{item.nodeid}[{authentication_label}]"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[None]
) -> Generator[None, None, None]:
    outcome = yield
    report = cast(Any, outcome).get_result()
    if _report_outcome_category(report) is None:
        return
    report.user_properties.append(
        (_REPORT_SUMMARY_KEY_PROPERTY, f"{item.nodeid}::{id(item)}")
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
        public_profile=pytestconfig.getoption("--target-public-profile"),
        public_shortcode=pytestconfig.getoption("--target-public-shortcode"),
        public_hashtag=pytestconfig.getoption("--target-public-hashtag"),
    )


@pytest.fixture(scope="session")
def session_credentials(pytestconfig: pytest.Config) -> SessionCredentials | None:
    return load_session_credentials(
        username=pytestconfig.getoption("--username"),
        sessionfile=pytestconfig.getoption("--sessionfile"),
    )


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
