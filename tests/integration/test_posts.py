from datetime import datetime
from pathlib import Path

import instaloader
import pytest

from tests.support.post_checkers import (
    PostChecker,
    PostCheckerName,
    assert_post_basic_information,
)
from tests.support.requirements_map import requirement


@requirement("post-basic-information-anonymous-critical")
def test_public_shortcode_post_check(
    active_instaloader: instaloader.Instaloader,
    integration_targets,
    output_dir: Path,
    post_checker_name: PostCheckerName,
    post_checker: PostChecker,
) -> None:
    shortcode = integration_targets.require("public_shortcode")

    post = instaloader.Post.from_shortcode(active_instaloader.context, shortcode)
    post_checker(active_instaloader, post, shortcode)
    if post_checker_name == "download":
        if not post.caption:
            pytest.skip("configured shortcode has no caption")
        assert_post_basic_information(post)
