from __future__ import annotations

from pathlib import Path

import instaloader
import pytest

from tests.support.requirements_map import requirement
from tests.support.targets import (
    ItemWindows,
    require_extended_window,
    require_first_page_window,
    split_item_windows,
)


@pytest.fixture(scope="module")
def logged_in_profile(
    logged_in_instaloader: instaloader.Instaloader,
) -> instaloader.Profile:
    username = logged_in_instaloader.test_login()
    return instaloader.Profile.from_username(logged_in_instaloader.context, username)


@pytest.fixture(scope="module")
def saved_posts_windows(
    logged_in_profile: instaloader.Profile,
) -> ItemWindows[instaloader.Post]:
    return split_item_windows(
        logged_in_profile.get_saved_posts(),
        first_page_count=12,
        total_count=50,
        description=f"saved posts of {logged_in_profile.username!r}",
    )


@pytest.fixture(scope="module")
def saved_posts_first_page(
    saved_posts_windows: ItemWindows[instaloader.Post],
) -> tuple[instaloader.Post, ...]:
    return require_first_page_window(saved_posts_windows)


@pytest.fixture(scope="module")
def saved_posts_extended(
    saved_posts_windows: ItemWindows[instaloader.Post],
) -> tuple[instaloader.Post, ...]:
    return require_extended_window(saved_posts_windows)


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
