from pathlib import Path

import instaloader
import pytest

from tests.support.post_checkers import PostChecker
from tests.support.pagination import Pager
from tests.support.requirements_map import paged_requirement, requirement
from tests.support.targets import IntegrationTargets


@pytest.fixture()
def hashtag(
    active_instaloader: instaloader.Instaloader,
    integration_targets: IntegrationTargets,
) -> instaloader.Hashtag:
    return instaloader.Hashtag.from_name(
        active_instaloader.context, integration_targets.require("hashtag")
    )


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


@paged_requirement(
    "hashtag-posts-first-page",
    "hashtag-posts-further-pages",
)
def test_hashtag_paged_posts_download(
    paginate: Pager,
    active_instaloader: instaloader.Instaloader,
    hashtag: instaloader.Hashtag,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in paginate(hashtag.get_posts(), f"hashtag {hashtag.name!r}"):
        post_checker(active_instaloader, post, f"#{hashtag.name}")
