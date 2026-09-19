from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Callable, TypeVar

import pytest


@dataclass(frozen=True)
class IntegrationTargets:
    public_profile: str | None = None
    public_shortcode: str | None = None
    public_hashtag: str | None = None


TargetItem = TypeVar("TargetItem")


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


def take_item_range(
    items: Iterable[TargetItem],
    *,
    start: int,
    end: int,
    description: str,
    prefix_error_handler: Callable[[Exception, int], None] | None = None,
) -> list[TargetItem]:
    if start < 1:
        raise pytest.UsageError(f"start must be >= 1, got {start}")
    if end < start:
        raise pytest.UsageError(f"end must be >= start, got start={start}, end={end}")

    iterator = iter(items)
    for position in range(1, start):
        try:
            next(iterator)
        except StopIteration:
            pytest.skip(
                f"configured target does not provide {position - 1} items for {description}"
            )
        except Exception as error:
            if isinstance(error, (pytest.skip.Exception, pytest.xfail.Exception)):
                raise
            if prefix_error_handler is not None:
                prefix_error_handler(error, position)
                raise AssertionError("prefix_error_handler must not return")
            raise

    selected: list[TargetItem] = []
    for position in range(start, end + 1):
        try:
            selected.append(next(iterator))
        except StopIteration:
            pytest.skip(
                f"configured target does not provide {position} items for {description}"
            )

    return selected
