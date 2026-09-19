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


@pytest.hookimpl()
def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-instagram",
        action="store_true",
        default=False,
        help="run Instagram-backed integration tests",
    )
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
        "--target-public-tagged-profile",
        action="store",
        default=None,
        help="public profile username with tagged posts; falls back to --target-public-profile",
    )
    parser.addoption(
        "--target-public-reels-profile",
        action="store",
        default=None,
        help="public profile username with reels; falls back to --target-public-profile",
    )
    parser.addoption(
        "--target-public-igtv-profile",
        action="store",
        default=None,
        help="public profile username with IGTV posts; falls back to --target-public-profile",
    )
    parser.addoption(
        "--target-story-profile",
        action="store",
        default=None,
        help="profile username with visible stories for logged-in story-item tests",
    )
    parser.addoption(
        "--target-highlight-profile",
        action="store",
        default=None,
        help="profile username with highlights for logged-in highlight tests",
    )
    parser.addoption(
        "--target-location",
        action="store",
        default=None,
        help="Instagram location ID for logged-in location tests",
    )


@pytest.hookimpl()
def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    max_importance = config.getoption("--max-importance")
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

        if item.get_closest_marker("integration") and not config.getoption(
            "--run-instagram"
        ):
            item.add_marker(
                pytest.mark.skip(
                    reason="pass --run-instagram to execute Instagram-backed tests"
                )
            )


@pytest.fixture(scope="session")
def integration_targets(pytestconfig: pytest.Config) -> IntegrationTargets:
    return load_targets(
        public_profile=pytestconfig.getoption("--target-public-profile"),
        public_shortcode=pytestconfig.getoption("--target-public-shortcode"),
        public_hashtag=pytestconfig.getoption("--target-public-hashtag"),
        public_tagged_profile=pytestconfig.getoption("--target-public-tagged-profile"),
        public_reels_profile=pytestconfig.getoption("--target-public-reels-profile"),
        public_igtv_profile=pytestconfig.getoption("--target-public-igtv-profile"),
        story_profile=pytestconfig.getoption("--target-story-profile"),
        highlight_profile=pytestconfig.getoption("--target-highlight-profile"),
        location=pytestconfig.getoption("--target-location"),
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
