import itertools
from collections.abc import Iterable, Iterator

import pytest

FIRST_PAGE_SIZE = 12


def _skip_if_empty[T](items: Iterable[T], description: str) -> Iterator[T]:
    found = False
    for item in items:
        found = True
        yield item
    if not found:
        pytest.skip(description)


def first_page[T](items: Iterable[T], what: str) -> Iterator[T]:
    """Yield the first page of items, skipping the test if there are none."""
    return _skip_if_empty(
        itertools.islice(items, FIRST_PAGE_SIZE), f"{what} has no items"
    )


def further_pages[T](items: Iterable[T], max_items: int, what: str) -> Iterator[T]:
    """Yield items after the first page up to max_items, skipping the test if there are none."""
    return _skip_if_empty(
        itertools.islice(items, FIRST_PAGE_SIZE, max_items),
        f"{what} has no items beyond the first page",
    )
