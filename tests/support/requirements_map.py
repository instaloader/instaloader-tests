"""Single source of truth for the Instaloader integration requirements.

Requirements cover Instagram-access-related integration behavior only and
describe observable behavior, not implementation details. Statements use
"shall" for testable behavior and "will" for intended direction or convenience
behavior that is not necessarily a separate test requirement.

Each entry below is preceded by its requirement statement as a comment and
lists its variants: one per authentication state, with the
recommended regression-test priority (importance) for that state. A requirement
whose statement says "(if logged-in)" only has a logged-in variant. Private
profile requirements assume that the logged-in account follows the target
profile. Paginated behavior is split into a first-page requirement (one page of
items) and a further-pages requirement (the first 50 items).
"""

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
class RequirementVariant:
    authentication: Authentication
    importance: Importance


REQUIREMENTS: dict[str, list[RequirementVariant]] = {
    # Session Creation / Import session from Firefox
    # Instaloader will provide a single-command way to import cookies from
    # Firefox (`instaloader --load-cookies firefox`).
    "session-import-firefox": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
    ],
    # Session Creation / Import session from other browsers
    # Instaloader will provide a single-command way to import cookies from a
    # browser (`instaloader --load-cookies BROWSER`).
    "session-import-browser": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH),
    ],
    # Session Creation / Login
    # Instaloader shall be able to create a session file with
    # `Instaloader.interactive_login()` if no 2FA is configured.
    "login-interactive": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH),
    ],
    # Session Creation / Test login
    # Instaloader shall be able to query Instagram for the username of the used
    # session.
    "test-login-query-username-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
    ],
    # Session Creation / 2FA
    # Instaloader shall be able to create a session file with
    # `Instaloader.interactive_login()` if 2FA is configured.
    "login-interactive-2fa": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.MEDIUM),
    ],
    # Download Targets / Profile / Public Profile Picture
    # Instaloader shall be able to download the profile picture of a public
    # Profile.
    "profile-picture-public": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
        RequirementVariant(Authentication.ANONYMOUS, Importance.CRITICAL),
    ],
    # Download Targets / Profile / Public Profile Posts
    # Instaloader shall be able to download the Posts of a public Profile.
    # (first page)
    "profile-posts-first-page-public": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
        RequirementVariant(Authentication.ANONYMOUS, Importance.HIGH),
    ],
    # Instaloader shall be able to download the Posts of a public Profile.
    # (first 50)
    "profile-posts-further-pages": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
        RequirementVariant(Authentication.ANONYMOUS, Importance.MEDIUM),
    ],
    # Download Targets / Profile / Private Profile Picture
    # Instaloader shall be able to download the profile picture of a private
    # Profile (if logged-in).
    "profile-picture-private-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
    ],
    # Download Targets / Profile / Private Profile Posts
    # Instaloader shall be able to download the Posts of a private Profile (if
    # logged-in). (first page)
    "profile-posts-first-page-private-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
    ],
    # Instaloader shall be able to download the Posts of a private Profile (if
    # logged-in). (first 50)
    "profile-posts-further-pages-private-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
    ],
    # Download Targets / Profile / Stories
    # Instaloader shall be able to download the Stories of a Profile (if logged-
    # in). (first page)
    "profile-stories-first-page-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH),
    ],
    # Instaloader shall be able to download the Stories of a Profile (if logged-
    # in). (first 50)
    "profile-stories-further-pages-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.MEDIUM),
    ],
    # Download Targets / Profile / Highlights / Cover Picture
    # Instaloader shall be able to download the cover picture of a Highlight (if
    # logged-in).
    "profile-highlights-cover-picture-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH),
    ],
    # Download Targets / Profile / Highlights / Highlights
    # Instaloader shall be able to download the Highlights of a Profile (if
    # logged-in). (first page)
    "profile-highlights-first-page-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH),
    ],
    # Instaloader shall be able to download the Highlights of a Profile (if
    # logged-in). (first 50)
    "profile-highlights-further-pages-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.MEDIUM),
    ],
    # Download Targets / Profile / Tagged
    # Instaloader shall be able to download the Posts where the Profile is
    # tagged. (first page)
    "profile-tagged-posts-first-page": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.MEDIUM),
        RequirementVariant(Authentication.ANONYMOUS, Importance.LOW),
    ],
    # Instaloader shall be able to download the Posts where the Profile is
    # tagged. (first 50)
    "profile-tagged-posts-further-pages": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.LOW),
        RequirementVariant(Authentication.ANONYMOUS, Importance.VERYLOW),
    ],
    # Download Targets / Profile / Reels
    # Instaloader shall be able to download the Reels videos of a Profile.
    # (first page)
    "profile-reels-first-page": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.MEDIUM),
        RequirementVariant(Authentication.ANONYMOUS, Importance.LOW),
    ],
    # Instaloader shall be able to download the Reels videos of a Profile.
    # (first 50)
    "profile-reels-further-pages": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.LOW),
        RequirementVariant(Authentication.ANONYMOUS, Importance.VERYLOW),
    ],
    # Download Targets / Profile / IGTV
    # Instaloader shall be able to download the IGTV videos of a Profile. (first
    # page)
    "profile-igtv-first-page": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.MEDIUM),
        RequirementVariant(Authentication.ANONYMOUS, Importance.LOW),
    ],
    # Instaloader shall be able to download the IGTV videos of a Profile. (first
    # 50)
    "profile-igtv-further-pages": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.LOW),
        RequirementVariant(Authentication.ANONYMOUS, Importance.VERYLOW),
    ],
    # Download Targets / Hashtags / Hashtag Profile Picture
    # Instaloader shall be able to download the profile picture of a Hashtag.
    "hashtag-profile-picture": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH),
        RequirementVariant(Authentication.ANONYMOUS, Importance.MEDIUM),
    ],
    # Download Targets / Hashtags / Hashtag Posts
    # Instaloader shall be able to download the Posts of a Hashtag. (first page)
    "hashtag-posts-first-page": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
        RequirementVariant(Authentication.ANONYMOUS, Importance.HIGH),
    ],
    # Instaloader shall be able to download the Posts of a Hashtag. (first 50)
    "hashtag-posts-further-pages": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
        RequirementVariant(Authentication.ANONYMOUS, Importance.MEDIUM),
    ],
    # Download Targets / Locations
    # Instaloader shall be able to download the Posts of a Location (if logged-
    # in). (first page)
    "location-posts-first-page-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.MEDIUM),
    ],
    # Instaloader shall be able to download the Posts of a Location (if logged-
    # in). (first 50)
    "location-posts-further-pages-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.LOW),
    ],
    # Download Targets / Single Post (shortcode)
    # Instaloader shall be able to download a single Post specified by its
    # shortcode.
    "single-post-shortcode": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
        RequirementVariant(Authentication.ANONYMOUS, Importance.CRITICAL),
    ],
    # Post Metadata / Basic Information
    # Instaloader shall be able to access the Caption and Date of a Post.
    "post-basic-information": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
        RequirementVariant(Authentication.ANONYMOUS, Importance.CRITICAL),
    ],
    # Download Targets / Saved Posts
    # Instaloader shall be able to download the saved Posts of the logged-in
    # user. (first page)
    "saved-posts-first-page-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
    ],
    # Instaloader shall be able to download the saved Posts of the logged-in
    # user. (first 50)
    "saved-posts-further-pages-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
    ],
    # Download Targets / Feed
    # Instaloader shall be able to download the Feed of the logged-in user.
    # (first page)
    "feed-first-page-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH),
    ],
    # Instaloader shall be able to download the Feed of the logged-in user.
    # (first 50)
    "feed-further-pages-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.MEDIUM),
    ],
    # Download Targets / Stories
    # Instaloader shall be able to download the currently-visible Stories of the
    # logged-in user. (first page)
    "stories-first-page-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH),
    ],
    # Instaloader shall be able to download the currently-visible Stories of the
    # logged-in user. (first 50)
    "stories-further-pages-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.MEDIUM),
    ],
    # Post Metadata / Likes
    # Instaloader shall be able to list the Profiles that have liked a Post (if
    # logged-in). (first page)
    "post-likes-first-page-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH),
    ],
    # Instaloader shall be able to list the Profiles that have liked a Post (if
    # logged-in). (first 50)
    "post-likes-further-pages-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH),
    ],
    # Post Metadata / Comments
    # Instaloader shall be able to list the comments of a Post. (first page)
    "post-comments-first-page": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH),
        RequirementVariant(Authentication.ANONYMOUS, Importance.MEDIUM),
    ],
    # Instaloader shall be able to list the comments of a Post. (first 50)
    "post-comments-further-pages": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.MEDIUM),
        RequirementVariant(Authentication.ANONYMOUS, Importance.LOW),
    ],
    # Post Metadata / Geotags
    # Instaloader shall be able to access the geotag of a Post (if logged-in).
    "post-geotag-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.LOW),
    ],
    # Profile Metadata / Resolve Public Profile by ID
    # Instaloader shall be able to resolve a public Profile from its ID.
    "profile-from-id-public": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
        RequirementVariant(Authentication.ANONYMOUS, Importance.HIGH),
    ],
    # Profile Metadata / Resolve Private Profile by ID
    # Instaloader shall be able to resolve a private Profile from its ID (if
    # logged-in).
    "profile-from-id-private-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
    ],
    # Profile Metadata / Followers
    # Instaloader shall be able to list the followers of a Profile (if logged-
    # in). (first page)
    "profile-followers-first-page-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH),
    ],
    # Instaloader shall be able to list the followers of a Profile (if logged-
    # in). (first 50)
    "profile-followers-further-pages-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.MEDIUM),
    ],
    # Profile Metadata / Followees
    # Instaloader shall be able to list the followees of a Profile (if logged-
    # in). (first page)
    "profile-followees-first-page-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH),
    ],
    # Instaloader shall be able to list the followees of a Profile (if logged-
    # in). (first 50)
    "profile-followees-further-pages-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.MEDIUM),
    ],
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
    variants = REQUIREMENTS[requirement_id]
    params = [
        pytest.param(
            variant.authentication,
            marks=(
                getattr(pytest.mark, variant.authentication.value),
                pytest.mark.importance(variant.importance.name.lower()),
            ),
            id=variant.authentication.value,
        )
        for variant in variants
    ]

    def decorator(test_function: Callable[..., object]) -> Callable[..., object]:
        marked = pytest.mark.usefixtures("active_authentication")(test_function)
        marked = pytest.mark.parametrize(
            "active_authentication", params, indirect=True
        )(marked)
        marked = pytest.mark.requirement_id(requirement_id)(marked)
        return pytest.mark.integration(marked)

    return decorator
