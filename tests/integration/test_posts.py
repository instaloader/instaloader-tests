from datetime import datetime

import instaloader
import pytest

from tests.support.requirements_map import requirement
from tests.support.targets import require_target


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
    logged_in_instaloader.download_saved_posts(max_count=12)
