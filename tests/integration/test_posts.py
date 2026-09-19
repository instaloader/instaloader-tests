from datetime import datetime

import instaloader
import pytest

from tests.support.requirements_map import requirement
from tests.support.targets import require_target

FIRST_PAGE_POST_COUNT = 12
FIRST_50_POST_COUNT = 50


def _saved_posts_count(
    logged_in_instaloader: instaloader.Instaloader,
) -> int | None:
    return (
        instaloader.Profile.own_profile(logged_in_instaloader.context)
        .get_saved_posts()
        .count
    )


@requirement("post-basic-information-anonymous-critical")
def test_public_shortcode_caption_and_date_accessible(
    anonymous_instaloader: instaloader.Instaloader,
    integration_targets,
) -> None:
    shortcode = require_target(
        integration_targets.public_shortcode, option_name="--target-public-shortcode"
    )

    post = instaloader.Post.from_shortcode(anonymous_instaloader.context, shortcode)
    if not post.caption:
        pytest.skip("configured shortcode has no caption")

    assert isinstance(post.caption, str)
    assert post.caption.strip()
    assert isinstance(post.date_utc, datetime)


@requirement("saved-posts-first-page-logged-in-critical")
def test_saved_posts_first_page_download(
    logged_in_instaloader: instaloader.Instaloader,
    output_dir,
) -> None:
    if _saved_posts_count(logged_in_instaloader) == 0:
        pytest.skip("configured account has no saved posts")
    logged_in_instaloader.download_saved_posts(max_count=FIRST_PAGE_POST_COUNT)


@requirement("saved-posts-first-50-logged-in-critical")
def test_saved_posts_first_50_download(
    logged_in_instaloader: instaloader.Instaloader,
    output_dir,
) -> None:
    saved_posts_count = _saved_posts_count(logged_in_instaloader)
    if saved_posts_count == 0:
        pytest.skip("configured account has no saved posts")
    if saved_posts_count is not None and saved_posts_count <= FIRST_PAGE_POST_COUNT:
        pytest.skip("configured account has fewer than 13 saved posts")
    logged_in_instaloader.download_saved_posts(max_count=FIRST_50_POST_COUNT)
