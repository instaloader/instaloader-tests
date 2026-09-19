FIRST_PAGE_ITEMS = 12


def first_page_limit(max_items: int) -> int:
    return min(FIRST_PAGE_ITEMS, max_items)


def further_pages_slice(max_items: int) -> tuple[int, int] | None:
    if max_items <= FIRST_PAGE_ITEMS:
        return None
    return FIRST_PAGE_ITEMS, max_items
