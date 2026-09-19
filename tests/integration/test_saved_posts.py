import itertools
from pathlib import Path

import instaloader
import pytest

from tests.support.pagination import (
    FIRST_PAGE_ITEMS,
    first_page_limit,
    further_pages_slice,
)
from tests.support.requirements_map import requirement


@requirement("saved-posts-first-page-logged-in")
def test_saved_posts_first_page_download(
    logged_in_instaloader: instaloader.Instaloader,
    max_items: int,
    output_dir: Path,
) -> None:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    for post in itertools.islice(profile.get_saved_posts(), first_page_limit(max_items)):
        logged_in_instaloader.download_post(post, target=f"{profile.username}-saved")


@requirement("saved-posts-further-pages-logged-in")
def test_saved_posts_extended_download(
    logged_in_instaloader: instaloader.Instaloader,
    max_items: int,
    output_dir: Path,
) -> None:
    further_pages_range = further_pages_slice(max_items)
    if further_pages_range is None:
        pytest.skip(
            f"requires --max-items > {FIRST_PAGE_ITEMS} for further-pages coverage"
        )

    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    further_posts = False
    start, stop = further_pages_range
    for post in itertools.islice(profile.get_saved_posts(), start, stop):
        logged_in_instaloader.download_post(post, target=f"{profile.username}-saved")
        further_posts = True
    if not further_posts:
        pytest.skip(
            "configured target does not provide more than "
            f"{FIRST_PAGE_ITEMS} items for saved posts of "
            f"{profile.username!r}"
        )
