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
    # Session Creation / Test login
    "test-login-query-username-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL)
    ],
    # Download Targets / Profile / Profile Picture
    "profile-picture-public": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
        RequirementVariant(Authentication.ANONYMOUS, Importance.CRITICAL),
    ],
    "profile-picture-private-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL)
    ],
    # Download Targets / Profile / Profile Posts
    "profile-posts-first-page-public": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
        RequirementVariant(Authentication.ANONYMOUS, Importance.HIGH),
    ],
    "profile-posts-further-pages": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
        RequirementVariant(Authentication.ANONYMOUS, Importance.MEDIUM),
    ],
    "profile-posts-first-page-private-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL)
    ],
    "profile-posts-further-pages-private-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL)
    ],
    "profile-stories-first-page-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH)
    ],
    "profile-stories-further-pages-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.MEDIUM)
    ],
    "profile-highlights-cover-picture-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH)
    ],
    "profile-highlights-first-page-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH)
    ],
    "profile-highlights-further-pages-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.MEDIUM)
    ],
    # Download Targets / Profile / Tagged
    "profile-tagged-posts-first-page": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.MEDIUM),
        RequirementVariant(Authentication.ANONYMOUS, Importance.LOW),
    ],
    "profile-tagged-posts-further-pages": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.LOW),
        RequirementVariant(Authentication.ANONYMOUS, Importance.VERYLOW),
    ],
    # Download Targets / Profile / Reels
    "profile-reels-first-page": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.MEDIUM),
        RequirementVariant(Authentication.ANONYMOUS, Importance.LOW),
    ],
    "profile-reels-further-pages": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.LOW),
        RequirementVariant(Authentication.ANONYMOUS, Importance.VERYLOW),
    ],
    # Download Targets / Profile / IGTV
    "profile-igtv-first-page": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.MEDIUM),
        RequirementVariant(Authentication.ANONYMOUS, Importance.LOW),
    ],
    "profile-igtv-further-pages": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.LOW),
        RequirementVariant(Authentication.ANONYMOUS, Importance.VERYLOW),
    ],
    # Download Targets / Hashtags / Hashtag Profile Picture
    "hashtag-profile-picture": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH),
        RequirementVariant(Authentication.ANONYMOUS, Importance.MEDIUM),
    ],
    # Download Targets / Hashtags / Hashtag Posts
    "hashtag-posts-first-page": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
        RequirementVariant(Authentication.ANONYMOUS, Importance.HIGH),
    ],
    "hashtag-posts-further-pages": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
        RequirementVariant(Authentication.ANONYMOUS, Importance.MEDIUM),
    ],
    # Download Targets / Locations
    "location-posts-first-page-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.MEDIUM)
    ],
    "location-posts-further-pages-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.LOW)
    ],
    # Download Targets / Single Post (shortcode)
    "single-post-shortcode": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
        RequirementVariant(Authentication.ANONYMOUS, Importance.CRITICAL),
    ],
    # Post Metadata / Basic Information
    "post-basic-information": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
        RequirementVariant(Authentication.ANONYMOUS, Importance.CRITICAL),
    ],
    # Download Targets / Saved Posts
    "saved-posts-first-page-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
    ],
    "saved-posts-further-pages-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
    ],
    # Download Targets / Feed
    "feed-first-page-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH),
    ],
    "feed-further-pages-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.MEDIUM),
    ],
    # Download Targets / Stories
    "stories-first-page-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH),
    ],
    "stories-further-pages-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.MEDIUM),
    ],
    # Post Metadata / Likes
    "post-likes-first-page-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH),
    ],
    "post-likes-further-pages-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH),
    ],
    # Post Metadata / Comments
    "post-comments-first-page": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH),
        RequirementVariant(Authentication.ANONYMOUS, Importance.MEDIUM),
    ],
    "post-comments-further-pages": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.MEDIUM),
        RequirementVariant(Authentication.ANONYMOUS, Importance.LOW),
    ],
    "post-geotag-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.LOW),
    ],
    # Profile Metadata / Followers + Followees
    "profile-followers-first-page-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH),
    ],
    "profile-followers-further-pages-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.MEDIUM),
    ],
    "profile-followees-first-page-logged-in": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.HIGH),
    ],
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
