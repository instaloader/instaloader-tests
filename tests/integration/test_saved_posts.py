import itertools
from pathlib import Path

import instaloader
import pytest

from tests.support.pagination import SAVED_POSTS_FURTHER_PAGES_START
from tests.support.requirements_map import requirement


@requirement("saved-posts-first-page-logged-in")
def test_saved_posts_first_page_download(
    logged_in_instaloader: instaloader.Instaloader,
    output_dir: Path,
) -> None:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    for post in itertools.islice(profile.get_saved_posts(), SAVED_POSTS_FURTHER_PAGES_START):
        logged_in_instaloader.download_post(post, target=f"{profile.username}-saved")


@requirement("saved-posts-further-pages-logged-in")
def test_saved_posts_extended_download(
    logged_in_instaloader: instaloader.Instaloader,
    max_items: int,
    output_dir: Path,
) -> None:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    further_posts = False
    for post in itertools.islice(
        profile.get_saved_posts(),
        SAVED_POSTS_FURTHER_PAGES_START,
        max_items,
    ):
        logged_in_instaloader.download_post(post, target=f"{profile.username}-saved")
        further_posts = True
    if not further_posts:
        pytest.skip(
            "configured target does not provide more than "
            f"{SAVED_POSTS_FURTHER_PAGES_START} items for saved posts of "
            f"{profile.username!r}"
        )
