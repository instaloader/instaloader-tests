import itertools
from pathlib import Path
from collections.abc import Iterator

import instaloader
import pytest

from tests.support.requirements_map import requirement


@pytest.fixture(scope="module")
def saved_posts_first_page(
    logged_in_instaloader: instaloader.Instaloader,
) -> Iterator[instaloader.Post]:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    return itertools.islice(profile.get_saved_posts(), 12)


@pytest.fixture(scope="module")
def saved_posts_extended(
    logged_in_instaloader: instaloader.Instaloader,
) -> Iterator[instaloader.Post]:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    extended_posts = list(itertools.islice(profile.get_saved_posts(), 12, 50))
    description = f"saved posts of {profile.username!r}"
    if not extended_posts:
        pytest.skip(
            f"configured target does not provide more than 12 items for {description}"
        )
    return iter(extended_posts)


@requirement("saved-posts-first-page-logged-in-critical")
def test_saved_posts_first_page_download(
    logged_in_instaloader: instaloader.Instaloader,
    saved_posts_first_page: Iterator[instaloader.Post],
    output_dir: Path,
) -> None:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    for post in saved_posts_first_page:
        logged_in_instaloader.download_post(post, target=f"{profile.username}-saved")


@requirement("saved-posts-first-50-logged-in-critical")
def test_saved_posts_extended_download(
    logged_in_instaloader: instaloader.Instaloader,
    saved_posts_extended: Iterator[instaloader.Post],
    output_dir: Path,
) -> None:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    for post in saved_posts_extended:
        logged_in_instaloader.download_post(post, target=f"{profile.username}-saved")
