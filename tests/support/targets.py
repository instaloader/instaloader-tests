from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Generic, TypeVar

import pytest


@dataclass(frozen=True)
class IntegrationTargets:
    public_profile: str | None = None
    public_shortcode: str | None = None
    public_hashtag: str | None = None


TargetItem = TypeVar("TargetItem")


@dataclass(frozen=True)
class ItemWindows(Generic[TargetItem]):
    first_page: tuple[TargetItem, ...]
    extended: tuple[TargetItem, ...]
    sampled_count: int
    first_page_count: int
    total_count: int
    description: str


def load_targets(
    *,
    public_profile: str | None,
    public_shortcode: str | None,
    public_hashtag: str | None,
) -> IntegrationTargets:
    return IntegrationTargets(
        public_profile=public_profile,
        public_shortcode=public_shortcode,
        public_hashtag=public_hashtag,
    )


def require_target(value: str | None, *, option_name: str) -> str:
    if value:
        return value
    pytest.skip(f"configure {option_name}")


def take_first_items(
    items: Iterable[TargetItem], *, count: int, description: str
) -> list[TargetItem]:
    selected: list[TargetItem] = []
    for item in items:
        selected.append(item)
        if len(selected) == count:
            return selected
    pytest.skip(f"configured target does not provide {count} items for {description}")


def split_item_windows(
    items: Iterable[TargetItem],
    *,
    first_page_count: int,
    total_count: int,
    description: str,
) -> ItemWindows[TargetItem]:
    selected: list[TargetItem] = []
    for item in items:
        selected.append(item)
        if len(selected) == total_count:
            break

    return ItemWindows(
        first_page=tuple(selected[:first_page_count]),
        extended=tuple(selected[first_page_count:total_count]),
        sampled_count=len(selected),
        first_page_count=first_page_count,
        total_count=total_count,
        description=description,
    )


def require_first_page_window(
    windows: ItemWindows[TargetItem],
) -> tuple[TargetItem, ...]:
    if len(windows.first_page) < windows.first_page_count:
        pytest.skip(
            "configured target does not provide "
            f"{windows.first_page_count} items for {windows.description} first page"
        )
    return windows.first_page


def require_extended_window(
    windows: ItemWindows[TargetItem],
) -> tuple[TargetItem, ...]:
    if windows.sampled_count < windows.total_count:
        pytest.skip(
            "configured target does not provide "
            f"{windows.total_count} items for {windows.description} first {windows.total_count}"
        )
    return windows.extended
