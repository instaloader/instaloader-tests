import pytest

from tests import conftest


def test_saved_posts_further_pages_end_uses_configured_value() -> None:
    assert conftest.parse_saved_posts_further_pages_end(37) == 37


def test_saved_posts_further_pages_end_rejects_non_further_values() -> None:
    with pytest.raises(pytest.UsageError, match="must be greater than 12"):
        conftest.parse_saved_posts_further_pages_end(12)
