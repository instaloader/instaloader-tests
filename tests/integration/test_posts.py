from datetime import datetime

import instaloader
import pytest

from tests.support.requirements_map import requirement


@requirement("post-basic-information-anonymous")
def test_public_shortcode_caption_and_date_accessible(
    active_instaloader: instaloader.Instaloader,
    integration_targets,
) -> None:
    shortcode = integration_targets.require("public_shortcode")

    post = instaloader.Post.from_shortcode(active_instaloader.context, shortcode)
    if not post.caption:
        pytest.skip("configured shortcode has no caption")

    assert isinstance(post.caption, str)
    assert post.caption.strip()
    assert isinstance(post.date_utc, datetime)
