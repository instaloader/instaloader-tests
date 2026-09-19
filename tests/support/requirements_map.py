from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import pytest


@dataclass(frozen=True)
class RequirementCase:
    requirement_id: str
    section: str
    statement: str
    importance: str
    authentication: str


REQUIREMENTS: dict[str, RequirementCase] = {
    "profile-picture-anonymous-critical": RequirementCase(
        requirement_id="profile-picture-anonymous-critical",
        section="Download Targets / Profile / Profile Picture",
        statement="Instaloader shall be able to download the profile picture of a Profile.",
        importance="critical",
        authentication="anonymous",
    ),
    "profile-posts-first-page-anonymous-critical": RequirementCase(
        requirement_id="profile-posts-first-page-anonymous-critical",
        section="Download Targets / Profile / Profile Posts",
        statement="Instaloader shall be able to download the Posts of a Profile (first page / 12 posts).",
        importance="critical",
        authentication="anonymous",
    ),
    "post-basic-information-anonymous-critical": RequirementCase(
        requirement_id="post-basic-information-anonymous-critical",
        section="Post Metadata / Basic Information",
        statement="Instaloader shall be able to access the Caption and Date of a Post.",
        importance="critical",
        authentication="anonymous",
    ),
}

_IMPORTANCE_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
    "very-low": 4,
}


def is_importance_enabled(maximum: str, required: str) -> bool:
    if maximum not in _IMPORTANCE_ORDER:
        raise pytest.UsageError(f"Unknown maximum importance level: {maximum}")
    if required not in _IMPORTANCE_ORDER:
        raise pytest.UsageError(f"Unknown required importance level: {required}")
    return _IMPORTANCE_ORDER[required] <= _IMPORTANCE_ORDER[maximum]



def requirement(requirement_id: str) -> Callable[[Callable[..., object]], Callable[..., object]]:
    if requirement_id not in REQUIREMENTS:
        raise pytest.UsageError(f"Unknown requirement_id marker: {requirement_id}")
    case = REQUIREMENTS[requirement_id]

    def decorator(test_function: Callable[..., object]) -> Callable[..., object]:
        marked = pytest.mark.requirement_id(requirement_id)(test_function)
        marked = pytest.mark.importance(case.importance)(marked)
        marked = getattr(pytest.mark, case.authentication)(marked)
        return pytest.mark.integration(marked)

    return decorator
