import itertools
from collections.abc import Iterable, Iterator

from instaloader import NodeIterator
import pytest

FIRST_PAGE_SIZE = 12


def _page[T](
    items: Iterable[T],
    start: int,
    stop: int,
    what: str,
    expected_count: int | None,
) -> Iterator[T]:
    if expected_count is None and isinstance(items, NodeIterator):
        expected_count = items.count
    seen = 0
    found = False
    for index, item in enumerate(itertools.islice(items, stop)):
        seen += 1
        if index >= start:
            found = True
            yield item
    if not found:
        if expected_count is not None and expected_count > seen:
            pytest.fail(
                f"{what} reports {expected_count} items, but the iterator "
                f"returned only {seen} and no items in the requested slice "
                f"[{start}:{stop}]"
            )
        description = "no items" if start == 0 else "no items beyond the first page"
        pytest.skip(f"{what} has {description}")


def first_page[T](
    items: Iterable[T], what: str, *, expected_count: int | None = None
) -> Iterator[T]:
    """Yield the first page, failing if a reported count contradicts an empty result."""
    return _page(items, 0, FIRST_PAGE_SIZE, what, expected_count)


def further_pages[T](
    items: Iterable[T],
    max_items: int,
    what: str,
    *,
    expected_count: int | None = None,
) -> Iterator[T]:
    """Yield further items, failing if a reported count contradicts an empty slice."""
    return _page(items, FIRST_PAGE_SIZE, max_items, what, expected_count)
