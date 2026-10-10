from pathlib import Path

import instaloader
import pytest

from tests.support.post_checkers import PostChecker
from tests.support.pagination import first_page, further_pages
from tests.support.requirements_map import requirement
from tests.support.targets import IntegrationTargets


@pytest.fixture()
def hashtag(
    active_instaloader: instaloader.Instaloader,
    integration_targets: IntegrationTargets,
) -> instaloader.Hashtag:
    return instaloader.Hashtag.from_name(
        active_instaloader.context, integration_targets.require("hashtag")
    )


@requirement("hashtag-posts-first-page")
def test_hashtag_first_page_posts_download(
    active_instaloader: instaloader.Instaloader,
    hashtag: instaloader.Hashtag,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in first_page(hashtag.get_posts_resumable(), f"hashtag {hashtag.name!r}"):
        post_checker(active_instaloader, post, f"#{hashtag.name}")


@requirement("hashtag-profile-picture")
def test_hashtag_profile_picture_download(
    active_instaloader: instaloader.Instaloader,
    hashtag: instaloader.Hashtag,
    output_dir: Path,
) -> None:
    active_instaloader.download_title_pic(
        hashtag.profile_pic_url,
        f"#{hashtag.name}",
        "profile_pic",
        None,
    )


@requirement("hashtag-posts-further-pages")
def test_hashtag_further_pages_posts_download(
    active_instaloader: instaloader.Instaloader,
    hashtag: instaloader.Hashtag,
    max_items: int,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in further_pages(
        hashtag.get_posts_resumable(), max_items, f"hashtag {hashtag.name!r}"
    ):
        post_checker(active_instaloader, post, f"#{hashtag.name}")
