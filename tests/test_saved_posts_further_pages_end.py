import pytest

from tests import conftest
from tests.support.pagination import SAVED_POSTS_FURTHER_PAGES_START


def test_saved_posts_further_pages_end_uses_configured_value() -> None:
    assert conftest.parse_saved_posts_further_pages_end(37) == 37


def test_saved_posts_further_pages_end_rejects_non_further_values() -> None:
    with pytest.raises(
        pytest.UsageError,
        match=f"must be greater than {SAVED_POSTS_FURTHER_PAGES_START}",
    ):
        conftest.parse_saved_posts_further_pages_end(SAVED_POSTS_FURTHER_PAGES_START)
