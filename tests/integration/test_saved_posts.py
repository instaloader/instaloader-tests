import itertools
from pathlib import Path
from collections.abc import Iterator

import instaloader
import pytest

from tests.support.post_checkers import PostChecker
from tests.support.requirements_map import requirement


@requirement("saved-posts-first-page-logged-in-critical")
def test_saved_posts_first_page_download(
    logged_in_instaloader: instaloader.Instaloader,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    for post in itertools.islice(profile.get_saved_posts(), 12):
        post_checker(
            logged_in_instaloader, post, target=f"{profile.username}-saved"
        )


@requirement("saved-posts-first-50-logged-in-critical")
def test_saved_posts_extended_download(
    logged_in_instaloader: instaloader.Instaloader,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    further_posts = False
    for post in itertools.islice(profile.get_saved_posts(), 12, 50):
        post_checker(
            logged_in_instaloader, post, target=f"{profile.username}-saved"
        )
        further_posts = True
    if not further_posts:
        pytest.skip(
            f"configured target does not provide more than 12 items for saved posts of {profile.username!r}"
        )
