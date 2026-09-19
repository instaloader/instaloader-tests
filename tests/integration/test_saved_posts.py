import itertools
from pathlib import Path

import instaloader
import pytest

from tests.support.post_checkers import PostChecker
from tests.support.requirements_map import requirement


@requirement("saved-posts-first-page-logged-in")
def test_saved_posts_first_page_download(
    logged_in_instaloader: instaloader.Instaloader,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    for post in itertools.islice(profile.get_saved_posts(), 12):
        post_checker(logged_in_instaloader, post, f"{profile.username}-saved")


@requirement("saved-posts-further-pages-logged-in")
def test_saved_posts_further_pages_download(
    logged_in_instaloader: instaloader.Instaloader,
    max_items: int,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    further_posts = False
    for post in itertools.islice(profile.get_saved_posts(), 12, max_items):
        post_checker(logged_in_instaloader, post, f"{profile.username}-saved")
        further_posts = True
    if not further_posts:
        pytest.skip(
            f"configured target does not provide more than 12 items for saved posts of {profile.username!r}"
        )
