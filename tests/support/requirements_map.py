from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, StrEnum
from typing import Callable

import pytest


class Importance(IntEnum):
    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    VERYLOW = 4


class Authentication(StrEnum):
    ANONYMOUS = "anonymous"
    LOGGED_IN = "logged_in"


@dataclass(frozen=True)
class RequirementCase:
    section: str
    statement: str
    importance: Importance
    authentication: Authentication


REQUIREMENTS: dict[str, RequirementCase] = {
    "test-login-query-username-logged-in-critical": RequirementCase(
        section="Session Creation / Test login",
        statement="Instaloader shall be able to query Instagram for the username of the used Session.",
        importance=Importance.CRITICAL,
        authentication=Authentication.LOGGED_IN,
    ),
    "profile-picture-anonymous-critical": RequirementCase(
        section="Download Targets / Profile / Profile Picture",
        statement="Instaloader shall be able to download the profile picture of a Profile.",
        importance=Importance.CRITICAL,
        authentication=Authentication.ANONYMOUS,
    ),
    "profile-posts-first-page-logged-in-critical": RequirementCase(
        section="Download Targets / Profile / Profile Posts / logged-in / First page (12 Posts)",
        statement="Instaloader shall be able to download the Posts of a Profile.",
        importance=Importance.CRITICAL,
        authentication=Authentication.LOGGED_IN,
    ),
    "profile-posts-first-50-logged-in-critical": RequirementCase(
        section="Download Targets / Profile / Profile Posts / logged-in / First 50 Posts",
        statement="Instaloader shall be able to download the Posts of a Profile.",
        importance=Importance.CRITICAL,
        authentication=Authentication.LOGGED_IN,
    ),
    "profile-posts-first-page-anonymous-high": RequirementCase(
        section="Download Targets / Profile / Profile Posts / anonymous / First page (12 Posts)",
        statement="Instaloader shall be able to download the Posts of a Profile.",
        importance=Importance.HIGH,
        authentication=Authentication.ANONYMOUS,
    ),
    "profile-posts-first-50-anonymous-medium": RequirementCase(
        section="Download Targets / Profile / Profile Posts / anonymous / First 50 Posts",
        statement="Instaloader shall be able to download the Posts of a Profile.",
        importance=Importance.MEDIUM,
        authentication=Authentication.ANONYMOUS,
    ),
    "profile-stories-first-page-logged-in-high": RequirementCase(
        section="Download Targets / Profile / Stories / logged-in / First page (12 StoryItems)",
        statement="Instaloader shall be able to download the Stories of a Profile (if logged-in).",
        importance=Importance.HIGH,
        authentication=Authentication.LOGGED_IN,
    ),
    "profile-stories-first-50-logged-in-medium": RequirementCase(
        section="Download Targets / Profile / Stories / logged-in / First 50 StoryItems",
        statement="Instaloader shall be able to download the Stories of a Profile (if logged-in).",
        importance=Importance.MEDIUM,
        authentication=Authentication.LOGGED_IN,
    ),
    "profile-highlights-first-page-logged-in-high": RequirementCase(
        section="Download Targets / Profile / Highlights / First page (12 Highlights)",
        statement="Instaloader shall be able to download the Highlights of a Profile (if logged-in).",
        importance=Importance.HIGH,
        authentication=Authentication.LOGGED_IN,
    ),
    "profile-highlights-first-50-logged-in-medium": RequirementCase(
        section="Download Targets / Profile / Highlights / First 50 Highlights",
        statement="Instaloader shall be able to download the Highlights of a Profile (if logged-in).",
        importance=Importance.MEDIUM,
        authentication=Authentication.LOGGED_IN,
    ),
    "profile-tagged-first-page-logged-in-medium": RequirementCase(
        section="Download Targets / Profile / Tagged / logged-in / First page (12 Posts)",
        statement="Instaloader shall be able to download the Posts where the Profile is tagged.",
        importance=Importance.MEDIUM,
        authentication=Authentication.LOGGED_IN,
    ),
    "profile-tagged-first-50-logged-in-low": RequirementCase(
        section="Download Targets / Profile / Tagged / logged-in / First 50 Posts",
        statement="Instaloader shall be able to download the Posts where the Profile is tagged.",
        importance=Importance.LOW,
        authentication=Authentication.LOGGED_IN,
    ),
    "profile-tagged-first-page-anonymous-low": RequirementCase(
        section="Download Targets / Profile / Tagged / anonymous / First page (12 Posts)",
        statement="Instaloader shall be able to download the Posts where the Profile is tagged.",
        importance=Importance.LOW,
        authentication=Authentication.ANONYMOUS,
    ),
    "profile-tagged-first-50-anonymous-verylow": RequirementCase(
        section="Download Targets / Profile / Tagged / anonymous / First 50 Posts",
        statement="Instaloader shall be able to download the Posts where the Profile is tagged.",
        importance=Importance.VERYLOW,
        authentication=Authentication.ANONYMOUS,
    ),
    "profile-reels-first-page-logged-in-medium": RequirementCase(
        section="Download Targets / Profile / Reels / logged-in / First page (12 Posts)",
        statement="Instaloader shall be able to download the Reels videos of a Profile.",
        importance=Importance.MEDIUM,
        authentication=Authentication.LOGGED_IN,
    ),
    "profile-reels-first-50-logged-in-low": RequirementCase(
        section="Download Targets / Profile / Reels / logged-in / First 50 Posts",
        statement="Instaloader shall be able to download the Reels videos of a Profile.",
        importance=Importance.LOW,
        authentication=Authentication.LOGGED_IN,
    ),
    "profile-reels-first-page-anonymous-low": RequirementCase(
        section="Download Targets / Profile / Reels / anonymous / First page (12 Posts)",
        statement="Instaloader shall be able to download the Reels videos of a Profile.",
        importance=Importance.LOW,
        authentication=Authentication.ANONYMOUS,
    ),
    "profile-reels-first-50-anonymous-verylow": RequirementCase(
        section="Download Targets / Profile / Reels / anonymous / First 50 Posts",
        statement="Instaloader shall be able to download the Reels videos of a Profile.",
        importance=Importance.VERYLOW,
        authentication=Authentication.ANONYMOUS,
    ),
    "profile-igtv-first-page-logged-in-medium": RequirementCase(
        section="Download Targets / Profile / IGTV / logged-in / First page (12 Posts)",
        statement="Instaloader shall be able to download the IGTV videos of a Profile.",
        importance=Importance.MEDIUM,
        authentication=Authentication.LOGGED_IN,
    ),
    "profile-igtv-first-50-logged-in-low": RequirementCase(
        section="Download Targets / Profile / IGTV / logged-in / First 50 Posts",
        statement="Instaloader shall be able to download the IGTV videos of a Profile.",
        importance=Importance.LOW,
        authentication=Authentication.LOGGED_IN,
    ),
    "profile-igtv-first-page-anonymous-low": RequirementCase(
        section="Download Targets / Profile / IGTV / anonymous / First page (12 Posts)",
        statement="Instaloader shall be able to download the IGTV videos of a Profile.",
        importance=Importance.LOW,
        authentication=Authentication.ANONYMOUS,
    ),
    "profile-igtv-first-50-anonymous-verylow": RequirementCase(
        section="Download Targets / Profile / IGTV / anonymous / First 50 Posts",
        statement="Instaloader shall be able to download the IGTV videos of a Profile.",
        importance=Importance.VERYLOW,
        authentication=Authentication.ANONYMOUS,
    ),
    "hashtag-posts-first-page-logged-in-critical": RequirementCase(
        section="Download Targets / Hashtags / Hashtag Posts / logged-in / First page (12 Posts)",
        statement="Instaloader shall be able to download the Posts of a Hashtag.",
        importance=Importance.CRITICAL,
        authentication=Authentication.LOGGED_IN,
    ),
    "hashtag-posts-first-50-logged-in-critical": RequirementCase(
        section="Download Targets / Hashtags / Hashtag Posts / logged-in / First 50 Posts",
        statement="Instaloader shall be able to download the Posts of a Hashtag.",
        importance=Importance.CRITICAL,
        authentication=Authentication.LOGGED_IN,
    ),
    "hashtag-posts-first-page-anonymous-high": RequirementCase(
        section="Download Targets / Hashtags / Hashtag Posts / anonymous / First page (12 Posts)",
        statement="Instaloader shall be able to download the Posts of a Hashtag.",
        importance=Importance.HIGH,
        authentication=Authentication.ANONYMOUS,
    ),
    "hashtag-posts-first-50-anonymous-medium": RequirementCase(
        section="Download Targets / Hashtags / Hashtag Posts / anonymous / First 50 Posts",
        statement="Instaloader shall be able to download the Posts of a Hashtag.",
        importance=Importance.MEDIUM,
        authentication=Authentication.ANONYMOUS,
    ),
    "location-posts-first-page-logged-in-medium": RequirementCase(
        section="Download Targets / Locations / logged-in / First page (12 Posts)",
        statement="Instaloader shall be able to download the Posts of a Location (if logged-in).",
        importance=Importance.MEDIUM,
        authentication=Authentication.LOGGED_IN,
    ),
    "location-posts-first-50-logged-in-low": RequirementCase(
        section="Download Targets / Locations / logged-in / First 50 Posts",
        statement="Instaloader shall be able to download the Posts of a Location (if logged-in).",
        importance=Importance.LOW,
        authentication=Authentication.LOGGED_IN,
    ),
    "post-basic-information-anonymous-critical": RequirementCase(
        section="Post Metadata / Basic Information",
        statement="Instaloader shall be able to access the Caption and Date of a Post.",
        importance=Importance.CRITICAL,
        authentication=Authentication.ANONYMOUS,
    ),
    "saved-posts-first-page-logged-in-critical": RequirementCase(
        section="Download Targets / Saved Posts / logged-in / First page (12 Posts)",
        statement="Instaloader shall be able to download the saved posts of the logged-in user.",
        importance=Importance.CRITICAL,
        authentication=Authentication.LOGGED_IN,
    ),
    "saved-posts-first-50-logged-in-critical": RequirementCase(
        section="Download Targets / Saved Posts / logged-in / First 50 Posts",
        statement="Instaloader shall be able to download the saved posts of the logged-in user.",
        importance=Importance.CRITICAL,
        authentication=Authentication.LOGGED_IN,
    ),
    "feed-first-page-logged-in-high": RequirementCase(
        section="Download Targets / Feed / logged-in / First page (12 Posts)",
        statement="Instaloader shall be able to download the Feed of the logged-in user.",
        importance=Importance.HIGH,
        authentication=Authentication.LOGGED_IN,
    ),
    "feed-first-50-logged-in-medium": RequirementCase(
        section="Download Targets / Feed / logged-in / First 50 Posts",
        statement="Instaloader shall be able to download the Feed of the logged-in user.",
        importance=Importance.MEDIUM,
        authentication=Authentication.LOGGED_IN,
    ),
    "stories-first-page-logged-in-high": RequirementCase(
        section="Download Targets / Stories / logged-in / First page (12 Stories)",
        statement="Instaloader shall be able to download the currently-visible Stories of the logged-in user.",
        importance=Importance.HIGH,
        authentication=Authentication.LOGGED_IN,
    ),
    "stories-first-50-logged-in-medium": RequirementCase(
        section="Download Targets / Stories / logged-in / First 50 Stories",
        statement="Instaloader shall be able to download the currently-visible Stories of the logged-in user.",
        importance=Importance.MEDIUM,
        authentication=Authentication.LOGGED_IN,
    ),
}


def _coerce_importance(value: Importance | str, *, label: str) -> Importance:
    if isinstance(value, Importance):
        return value
    try:
        return Importance[value.upper()]
    except KeyError as error:
        raise pytest.UsageError(f"Unknown {label} importance level: {value}") from error


def is_importance_enabled(
    maximum: Importance | str, required: Importance | str
) -> bool:
    maximum_importance = _coerce_importance(maximum, label="maximum")
    required_importance = _coerce_importance(required, label="required")
    return required_importance <= maximum_importance


def requirement(
    requirement_id: str,
) -> Callable[[Callable[..., object]], Callable[..., object]]:
    if requirement_id not in REQUIREMENTS:
        raise pytest.UsageError(f"Unknown requirement_id marker: {requirement_id}")
    case = REQUIREMENTS[requirement_id]

    def decorator(test_function: Callable[..., object]) -> Callable[..., object]:
        marked = pytest.mark.requirement_id(requirement_id)(test_function)
        marked = pytest.mark.importance(case.importance.name.lower())(marked)
        marked = getattr(pytest.mark, case.authentication.value)(marked)
        return pytest.mark.integration(marked)

    return decorator
