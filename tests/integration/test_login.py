from pathlib import Path

import instaloader
import pytest

from tests.support.credentials import SessionCredentials
from tests.support.requirements_map import requirement


@requirement("login-create-session-no-2fa-logged-in")
def test_login_creates_session_file_without_2fa(
    session_credentials: SessionCredentials | None,
    login_password: str | None,
    tmp_path: Path,
) -> None:
    if session_credentials is None:
        pytest.skip("configure --username for login tests")
    if login_password is None:
        pytest.skip("configure --password for login-creation tests")

    username = session_credentials.username
    generated_session_file = tmp_path / f"session-{username}"
    login_loader = instaloader.Instaloader(quiet=True)
    try:
        login_loader.login(username, login_password)
    except instaloader.TwoFactorAuthRequiredException:
        pytest.skip(
            "configured account requires 2FA; this test covers the no-2FA login requirement"
        )
    login_loader.save_session_to_file(str(generated_session_file))
    assert generated_session_file.exists()

    reloaded_loader = instaloader.Instaloader(quiet=True)
    reloaded_loader.load_session_from_file(username, str(generated_session_file))
    assert reloaded_loader.test_login() == username


@requirement("test-login-query-username-logged-in")
def test_session_file_usable_with_test_login(
    active_instaloader: instaloader.Instaloader,
    session_credentials: SessionCredentials | None,
) -> None:
    assert session_credentials is not None
    assert active_instaloader.test_login() == session_credentials.username
