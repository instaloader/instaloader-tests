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
    "test-login-query-username-logged-in-critical": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL)
    ],
    # Download Targets / Profile / Profile Picture
    "profile-picture-anonymous-critical": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
        RequirementVariant(Authentication.ANONYMOUS, Importance.CRITICAL),
    ],
    # Download Targets / Profile / Profile Posts
    "profile-posts-first-page-anonymous-critical": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
        RequirementVariant(Authentication.ANONYMOUS, Importance.HIGH),
    ],
    # Post Metadata / Basic Information
    "post-basic-information-anonymous-critical": [
        RequirementVariant(Authentication.LOGGED_IN, Importance.CRITICAL),
        RequirementVariant(Authentication.ANONYMOUS, Importance.CRITICAL),
    ],
    # Download Targets / Saved Posts
    **{
        requirement_id: [
            RequirementVariant(Authentication.LOGGED_IN, importance),
        ]
        for requirement_id, importance in {
            "saved-posts-first-page-logged-in-critical": Importance.CRITICAL,
            "saved-posts-first-50-logged-in-critical": Importance.CRITICAL,
        }.items()
    },
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
            variant.authentication.value,
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
