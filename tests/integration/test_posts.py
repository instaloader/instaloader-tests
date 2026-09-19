from itertools import islice
from pathlib import Path
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
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(logged_in_instaloader, "dirname_pattern", "{target}")
    monkeypatch.setattr(logged_in_instaloader, "filename_pattern", "{shortcode}")
    saved_posts_target = "saved-posts"
    assert Path.cwd() == output_dir

    saved_posts = instaloader.Profile.own_profile(
        logged_in_instaloader.context
    ).get_saved_posts()
    first_post = next(iter(saved_posts), None)
    if first_post is None:
        pytest.skip("configured account has no saved posts")
    first_page_size = len(saved_posts._data["edges"])
    expected_posts = (first_post, *tuple(islice(saved_posts, first_page_size - 1)))
    if saved_posts.count is not None:
        assert len(expected_posts) == min(saved_posts.count, first_page_size)

    for post in expected_posts:
        logged_in_instaloader.download_post(post, target=saved_posts_target)

    saved_dir = Path.cwd() / saved_posts_target
    assert saved_dir.is_dir()
    downloaded_filenames = tuple(
        sorted(path.name for path in saved_dir.iterdir() if path.is_file())
    )

    assert downloaded_filenames
    for post in expected_posts:
        assert any(
            filename.startswith(post.shortcode) for filename in downloaded_filenames
        )
