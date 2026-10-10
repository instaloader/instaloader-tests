"""Single source of truth for the Instaloader integration requirements.

Requirements cover Instagram-access-related integration behavior only and
describe observable behavior, not implementation details. Statements use
"shall" for testable behavior and "will" for intended direction or convenience
behavior that is not necessarily a separate test requirement.

Each requirement lists its variants: one per authentication state, with the
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


@dataclass(frozen=True)
class Requirement:
    id: str
    section: str
    statement: str
    variants: tuple[RequirementVariant, ...]


def _variants(
    logged_in: Importance | None = None, anonymous: Importance | None = None
) -> tuple[RequirementVariant, ...]:
    variants = []
    if logged_in is not None:
        variants.append(RequirementVariant(Authentication.LOGGED_IN, logged_in))
    if anonymous is not None:
        variants.append(RequirementVariant(Authentication.ANONYMOUS, anonymous))
    return tuple(variants)


def _paged(
    section: str,
    statement: str,
    first_id: str,
    further_id: str,
    first: tuple[RequirementVariant, ...],
    further: tuple[RequirementVariant, ...],
) -> list[Requirement]:
    return [
        Requirement(first_id, section, f"{statement} (first page)", first),
        Requirement(further_id, section, f"{statement} (first 50)", further),
    ]


C, H, M, L, V = (
    Importance.CRITICAL,
    Importance.HIGH,
    Importance.MEDIUM,
    Importance.LOW,
    Importance.VERYLOW,
)

_REQUIREMENT_LIST: list[Requirement] = [
    # Session Creation
    Requirement(
        "session-import-firefox",
        "Session Creation / Import session from Firefox",
        "Instaloader will provide a single-command way to import cookies from "
        "Firefox (`instaloader --load-cookies firefox`).",
        _variants(logged_in=C),
    ),
    Requirement(
        "session-import-browser",
        "Session Creation / Import session from other browsers",
        "Instaloader will provide a single-command way to import cookies from a "
        "browser (`instaloader --load-cookies BROWSER`).",
        _variants(logged_in=H),
    ),
    Requirement(
        "login-interactive",
        "Session Creation / Login",
        "Instaloader shall be able to create a session file with "
        "`Instaloader.interactive_login()` if no 2FA is configured.",
        _variants(logged_in=H),
    ),
    Requirement(
        "test-login-query-username-logged-in",
        "Session Creation / Test login",
        "Instaloader shall be able to query Instagram for the username of the "
        "used session.",
        _variants(logged_in=C),
    ),
    Requirement(
        "login-interactive-2fa",
        "Session Creation / 2FA",
        "Instaloader shall be able to create a session file with "
        "`Instaloader.interactive_login()` if 2FA is configured.",
        _variants(logged_in=M),
    ),
    # Download Targets / Profile
    Requirement(
        "profile-picture-public",
        "Download Targets / Profile / Public Profile Picture",
        "Instaloader shall be able to download the profile picture of a public "
        "Profile.",
        _variants(C, C),
    ),
    *_paged(
        "Download Targets / Profile / Public Profile Posts",
        "Instaloader shall be able to download the Posts of a public Profile.",
        "profile-posts-first-page-public",
        "profile-posts-further-pages",
        _variants(C, H),
        _variants(C, M),
    ),
    Requirement(
        "profile-picture-private-logged-in",
        "Download Targets / Profile / Private Profile Picture",
        "Instaloader shall be able to download the profile picture of a private "
        "Profile (if logged-in).",
        _variants(logged_in=C),
    ),
    *_paged(
        "Download Targets / Profile / Private Profile Posts",
        "Instaloader shall be able to download the Posts of a private Profile "
        "(if logged-in).",
        "profile-posts-first-page-private-logged-in",
        "profile-posts-further-pages-private-logged-in",
        _variants(logged_in=C),
        _variants(logged_in=C),
    ),
    *_paged(
        "Download Targets / Profile / Stories",
        "Instaloader shall be able to download the Stories of a Profile "
        "(if logged-in).",
        "profile-stories-first-page-logged-in",
        "profile-stories-further-pages-logged-in",
        _variants(logged_in=H),
        _variants(logged_in=M),
    ),
    Requirement(
        "profile-highlights-cover-picture-logged-in",
        "Download Targets / Profile / Highlights / Cover Picture",
        "Instaloader shall be able to download the cover picture of a Highlight "
        "(if logged-in).",
        _variants(logged_in=H),
    ),
    *_paged(
        "Download Targets / Profile / Highlights / Highlights",
        "Instaloader shall be able to download the Highlights of a Profile "
        "(if logged-in).",
        "profile-highlights-first-page-logged-in",
        "profile-highlights-further-pages-logged-in",
        _variants(logged_in=H),
        _variants(logged_in=M),
    ),
    *_paged(
        "Download Targets / Profile / Tagged",
        "Instaloader shall be able to download the Posts where the Profile is "
        "tagged.",
        "profile-tagged-posts-first-page",
        "profile-tagged-posts-further-pages",
        _variants(M, L),
        _variants(L, V),
    ),
    *_paged(
        "Download Targets / Profile / Reels",
        "Instaloader shall be able to download the Reels videos of a Profile.",
        "profile-reels-first-page",
        "profile-reels-further-pages",
        _variants(M, L),
        _variants(L, V),
    ),
    *_paged(
        "Download Targets / Profile / IGTV",
        "Instaloader shall be able to download the IGTV videos of a Profile.",
        "profile-igtv-first-page",
        "profile-igtv-further-pages",
        _variants(M, L),
        _variants(L, V),
    ),
    # Download Targets / Hashtags
    Requirement(
        "hashtag-profile-picture",
        "Download Targets / Hashtags / Hashtag Profile Picture",
        "Instaloader shall be able to download the profile picture of a Hashtag.",
        _variants(H, M),
    ),
    *_paged(
        "Download Targets / Hashtags / Hashtag Posts",
        "Instaloader shall be able to download the Posts of a Hashtag.",
        "hashtag-posts-first-page",
        "hashtag-posts-further-pages",
        _variants(C, H),
        _variants(C, M),
    ),
    # Download Targets / Locations
    *_paged(
        "Download Targets / Locations",
        "Instaloader shall be able to download the Posts of a Location "
        "(if logged-in).",
        "location-posts-first-page-logged-in",
        "location-posts-further-pages-logged-in",
        _variants(logged_in=M),
        _variants(logged_in=L),
    ),
    # Download Targets / Single Post
    Requirement(
        "single-post-shortcode",
        "Download Targets / Single Post (shortcode)",
        "Instaloader shall be able to download a single Post specified by its "
        "shortcode.",
        _variants(C, C),
    ),
    # Post Metadata
    Requirement(
        "post-basic-information",
        "Post Metadata / Basic Information",
        "Instaloader shall be able to access the Caption and Date of a Post.",
        _variants(C, C),
    ),
    # Download Targets / Saved Posts
    *_paged(
        "Download Targets / Saved Posts",
        "Instaloader shall be able to download the saved Posts of the logged-in "
        "user.",
        "saved-posts-first-page-logged-in",
        "saved-posts-further-pages-logged-in",
        _variants(logged_in=C),
        _variants(logged_in=C),
    ),
    # Download Targets / Feed
    *_paged(
        "Download Targets / Feed",
        "Instaloader shall be able to download the Feed of the logged-in user.",
        "feed-first-page-logged-in",
        "feed-further-pages-logged-in",
        _variants(logged_in=H),
        _variants(logged_in=M),
    ),
    # Download Targets / Stories
    *_paged(
        "Download Targets / Stories",
        "Instaloader shall be able to download the currently-visible Stories of "
        "the logged-in user.",
        "stories-first-page-logged-in",
        "stories-further-pages-logged-in",
        _variants(logged_in=H),
        _variants(logged_in=M),
    ),
    # Post Metadata
    *_paged(
        "Post Metadata / Likes",
        "Instaloader shall be able to list the Profiles that have liked a Post "
        "(if logged-in).",
        "post-likes-first-page-logged-in",
        "post-likes-further-pages-logged-in",
        _variants(logged_in=H),
        _variants(logged_in=H),
    ),
    *_paged(
        "Post Metadata / Comments",
        "Instaloader shall be able to list the comments of a Post.",
        "post-comments-first-page",
        "post-comments-further-pages",
        _variants(H, M),
        _variants(M, L),
    ),
    Requirement(
        "post-geotag-logged-in",
        "Post Metadata / Geotags",
        "Instaloader shall be able to access the geotag of a Post (if logged-in).",
        _variants(logged_in=L),
    ),
    # Profile Metadata
    *_paged(
        "Profile Metadata / Followers",
        "Instaloader shall be able to list the followers of a Profile "
        "(if logged-in).",
        "profile-followers-first-page-logged-in",
        "profile-followers-further-pages-logged-in",
        _variants(logged_in=H),
        _variants(logged_in=M),
    ),
    *_paged(
        "Profile Metadata / Followees",
        "Instaloader shall be able to list the followees of a Profile "
        "(if logged-in).",
        "profile-followees-first-page-logged-in",
        "profile-followees-further-pages-logged-in",
        _variants(logged_in=H),
        _variants(logged_in=M),
    ),
]

REQUIREMENTS: dict[str, Requirement] = {item.id: item for item in _REQUIREMENT_LIST}
assert len(REQUIREMENTS) == len(_REQUIREMENT_LIST), "duplicate requirement id"


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
    variants = REQUIREMENTS[requirement_id].variants
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
