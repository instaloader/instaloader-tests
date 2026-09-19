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
    return tuple(
        take_item_range(
            logged_in_profile.get_saved_posts(),
            start=13,
            end=50,
            description=f"saved posts of {logged_in_profile.username!r}",
            skip_prefix_errors=True,
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
