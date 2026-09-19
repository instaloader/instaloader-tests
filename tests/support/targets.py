from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from itertools import islice
from typing import TypeVar

import pytest

FIRST_PAGE_ITEM_COUNT = 12
FIRST_50_ITEM_COUNT = 50


@dataclass(frozen=True)
class IntegrationTargets:
    public_profile: str | None = None
    public_shortcode: str | None = None
    public_hashtag: str | None = None
    public_tagged_profile: str | None = None
    public_reels_profile: str | None = None
    public_igtv_profile: str | None = None
    story_profile: str | None = None
    highlight_profile: str | None = None
    location: str | None = None


TargetItem = TypeVar("TargetItem")


def load_targets(
    *,
    public_profile: str | None,
    public_shortcode: str | None,
    public_hashtag: str | None,
    public_tagged_profile: str | None,
    public_reels_profile: str | None,
    public_igtv_profile: str | None,
    story_profile: str | None,
    highlight_profile: str | None,
    location: str | None,
) -> IntegrationTargets:
    return IntegrationTargets(
        public_profile=public_profile,
        public_shortcode=public_shortcode,
        public_hashtag=public_hashtag,
        public_tagged_profile=public_tagged_profile,
        public_reels_profile=public_reels_profile,
        public_igtv_profile=public_igtv_profile,
        story_profile=story_profile,
        highlight_profile=highlight_profile,
        location=location,
    )


def require_target(value: str | None, *, option_name: str) -> str:
    if value:
        return value
    pytest.skip(f"configure {option_name}")


def require_target_or_fallback(
    value: str | None,
    *,
    option_name: str,
    fallback_value: str | None,
    fallback_option_name: str,
) -> str:
    if value:
        return value
    if fallback_value:
        return fallback_value
    pytest.skip(f"configure {option_name} or {fallback_option_name}")


def take_first_items(
    items: Iterable[TargetItem], *, count: int, description: str
) -> list[TargetItem]:
    selected: list[TargetItem] = []
    for item in items:
        selected.append(item)
        if len(selected) == count:
            return selected
    pytest.skip(f"configured target does not provide {count} items for {description}")


def take_up_to_items(
    items: Iterable[TargetItem],
    *,
    minimum_count: int,
    maximum_count: int,
    description: str,
) -> list[TargetItem]:
    selected = list(islice(items, maximum_count))
    if len(selected) < minimum_count:
        pytest.skip(
            f"configured target does not provide {minimum_count} items for {description}"
        )
    return selected
