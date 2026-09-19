from pathlib import Path
from datetime import datetime

import instaloader
import pytest

from tests.support.requirements_map import requirement
from tests.support.targets import require_target, take_first_items


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
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(logged_in_instaloader, "dirname_pattern", "{target}")
    monkeypatch.setattr(logged_in_instaloader, "filename_pattern", "{shortcode}")
    saved_posts_target = "saved-posts"
    assert Path.cwd() == output_dir

    expected_posts = tuple(
        take_first_items(
            instaloader.Profile.own_profile(
                logged_in_instaloader.context
            ).get_saved_posts(),
            count=12,
            description="logged-in user's saved posts",
        )
    )
    assert expected_posts

    for post in expected_posts:
        logged_in_instaloader.download_post(post, target=saved_posts_target)

    saved_dir = Path.cwd() / saved_posts_target
    downloaded_filenames = tuple(
        path.name for path in saved_dir.iterdir() if path.is_file()
    )

    assert downloaded_filenames
    for post in expected_posts:
        assert any(
            filename.startswith(post.shortcode) for filename in downloaded_filenames
        )
