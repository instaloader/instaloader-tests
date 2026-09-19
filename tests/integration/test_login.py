import instaloader

from tests.support.credentials import SessionCredentials
from tests.support.requirements_map import requirement


@requirement("test-login-query-username-logged-in-critical")
def test_session_file_usable_with_test_login(
    logged_in_instaloader: instaloader.Instaloader,
    session_credentials: SessionCredentials | None,
) -> None:
    assert session_credentials is not None
    assert logged_in_instaloader.test_login() == session_credentials.username
