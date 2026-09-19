from __future__ import annotations

from pathlib import Path

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


def _authentication_label(item: pytest.Item) -> str | None:
    if item.get_closest_marker("anonymous"):
        return "anonymous"
    if item.get_closest_marker("logged_in"):
        return "logged_in"
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
            max_importance, importance_marker.args[0]
        ):
            item.add_marker(
                pytest.mark.skip(
                    reason=f"requires --max-importance >= {importance_marker.args[0]}"
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


@pytest.fixture(scope="session")
def active_instaloader(
    request: pytest.FixtureRequest,
    anonymous_instaloader: instaloader.Instaloader,
    logged_in_instaloader: instaloader.Instaloader,
) -> instaloader.Instaloader:
    authentication = request.param
    if authentication == "anonymous":
        return anonymous_instaloader
    if authentication == "logged_in":
        return logged_in_instaloader
    raise pytest.UsageError(f"Unknown authentication variant: {authentication}")
