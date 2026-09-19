import itertools
from pathlib import Path

import instaloader
import pytest

from tests.support.post_checkers import PostChecker
from tests.support.requirements_map import requirement
from tests.support.targets import IntegrationTargets


@pytest.fixture()
def hashtag(
    active_instaloader: instaloader.Instaloader,
    integration_targets: IntegrationTargets,
) -> instaloader.Hashtag:
    return instaloader.Hashtag.from_name(
        active_instaloader.context, integration_targets.require("public_hashtag")
    )


@requirement("hashtag-posts-first-page")
def test_hashtag_first_page_posts_download(
    active_instaloader: instaloader.Instaloader,
    hashtag: instaloader.Hashtag,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in itertools.islice(hashtag.get_posts(), 12):
        post_checker(active_instaloader, post, f"#{hashtag.name}")


@requirement("hashtag-posts-further-pages")
def test_hashtag_further_pages_posts_download(
    active_instaloader: instaloader.Instaloader,
    hashtag: instaloader.Hashtag,
    max_items: int,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    further_posts = False
    for post in itertools.islice(hashtag.get_posts(), 12, max_items):
        post_checker(active_instaloader, post, f"#{hashtag.name}")
        further_posts = True
    if not further_posts:
        pytest.skip(
            f"configured target does not provide more than 12 items for hashtag {hashtag.name!r}"
        )
