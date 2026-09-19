from tests.support.pagination import (
    FIRST_PAGE_ITEMS,
    first_page_limit,
    further_pages_slice,
)


def test_first_page_limit_uses_max_items_when_smaller_than_first_page() -> None:
    assert first_page_limit(1) == 1


def test_further_pages_slice_returns_none_at_first_page_boundary() -> None:
    assert further_pages_slice(FIRST_PAGE_ITEMS) is None


def test_further_pages_slice_starts_after_first_page() -> None:
    assert further_pages_slice(FIRST_PAGE_ITEMS + 1) == (
        FIRST_PAGE_ITEMS,
        FIRST_PAGE_ITEMS + 1,
    )
