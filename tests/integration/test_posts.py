from pathlib import Path

import instaloader

from tests.support.post_checkers import (
    PostChecker,
    PostCheckerName,
    assert_post_basic_information,
)
from tests.support.requirements_map import requirement


@requirement("post-basic-information-anonymous")
def test_public_shortcode_caption_and_date_accessible(
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
        assert_post_basic_information(post)


@requirement("single-post-shortcode-anonymous")
def test_public_shortcode_download(
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
        downloaded_files = list(output_dir.joinpath(shortcode).glob(f"{shortcode}*"))
        assert downloaded_files
