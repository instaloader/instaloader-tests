import itertools
from pathlib import Path
from collections.abc import Iterator

import instaloader
import pytest

from tests.support.requirements_map import requirement


@requirement("saved-posts-first-page-logged-in")
def test_saved_posts_first_page_download(
    logged_in_instaloader: instaloader.Instaloader,
    output_dir: Path,
) -> None:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    for post in itertools.islice(profile.get_saved_posts(), 12):
        logged_in_instaloader.download_post(post, target=f"{profile.username}-saved")


@requirement("saved-posts-further-pages-logged-in")
def test_saved_posts_extended_download(
    logged_in_instaloader: instaloader.Instaloader,
    saved_posts_further_pages_end: int,
    output_dir: Path,
) -> None:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    further_posts = False
    for post in itertools.islice(
        profile.get_saved_posts(), 12, saved_posts_further_pages_end
    ):
        logged_in_instaloader.download_post(post, target=f"{profile.username}-saved")
        further_posts = True
    if not further_posts:
        pytest.skip(
            f"configured target does not provide more than 12 items for saved posts of {profile.username!r}"
        )
