from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from instaloader.instaloader import get_default_session_filename


@dataclass(frozen=True)
class SessionCredentials:
    username: str
    session_file: Path


ENV_USERNAME = "INSTALOADER_USERNAME"
ENV_SESSION_FILE = "INSTALOADER_SESSIONFILE"


def _first_value(*values: str | None) -> str | None:
    for value in values:
        if value:
            return value
    return None


def load_session_credentials(
    *, username: str | None, sessionfile: str | None
) -> SessionCredentials | None:
    resolved_username = _first_value(username, os.getenv(ENV_USERNAME))
    if not resolved_username:
        return None
    resolved_sessionfile = _first_value(sessionfile, os.getenv(ENV_SESSION_FILE))
    session_file = Path(
        resolved_sessionfile or get_default_session_filename(resolved_username)
    ).expanduser()
    return SessionCredentials(username=resolved_username, session_file=session_file)
