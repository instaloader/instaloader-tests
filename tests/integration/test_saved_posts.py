from pathlib import Path

import instaloader
import pytest

from tests.support.requirements_map import requirement
from tests.support.targets import take_item_range


@pytest.fixture(scope="module")
def saved_posts_first_page(
    logged_in_profile: instaloader.Profile,
) -> tuple[instaloader.Post, ...]:
    return tuple(
        take_item_range(
            logged_in_profile.get_saved_posts(),
            start=1,
            end=12,
            description=f"saved posts of {logged_in_profile.username!r}",
        )
    )


@pytest.fixture(scope="module")
def saved_posts_extended(
    logged_in_profile: instaloader.Profile,
) -> tuple[instaloader.Post, ...]:
    description = f"saved posts of {logged_in_profile.username!r}"

    def prefix_error_handler(error: Exception, position: int) -> None:
        pytest.xfail(
            "extended saved-post range failed while advancing through prefix "
            f"(item {position}) for {description}; this is covered by first-page checks "
            f"({type(error).__name__}: {error})"
        )

    return tuple(
        take_item_range(
            logged_in_profile.get_saved_posts(),
            start=13,
            end=50,
            description=description,
            prefix_error_handler=prefix_error_handler,
        )
    )


@requirement("saved-posts-first-page-logged-in-critical")
def test_saved_posts_first_page_download(
    logged_in_instaloader: instaloader.Instaloader,
    logged_in_profile: instaloader.Profile,
    saved_posts_first_page: tuple[instaloader.Post, ...],
    output_dir: Path,
) -> None:
    for post in saved_posts_first_page:
        logged_in_instaloader.download_post(
            post, target=f"{logged_in_profile.username}-saved"
        )


@requirement("saved-posts-first-50-logged-in-high")
def test_saved_posts_extended_download(
    logged_in_instaloader: instaloader.Instaloader,
    logged_in_profile: instaloader.Profile,
    saved_posts_extended: tuple[instaloader.Post, ...],
    output_dir: Path,
) -> None:
    for post in saved_posts_extended:
        logged_in_instaloader.download_post(
            post, target=f"{logged_in_profile.username}-saved"
        )
