from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from instaloader.instaloader import get_default_session_filename


@dataclass(frozen=True)
class SessionCredentials:
    username: str
    session_file: Path


def load_session_credentials(
    *, username: str | None, sessionfile: str | None
) -> SessionCredentials | None:
    if not username:
        return None
    session_file = Path(
        sessionfile or get_default_session_filename(username)
    ).expanduser()
    return SessionCredentials(username=username, session_file=session_file)
