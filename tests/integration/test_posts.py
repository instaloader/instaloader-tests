from pathlib import Path

import instaloader
import pytest

from tests.support.post_checkers import (
    PostChecker,
    PostCheckerName,
    assert_post_basic_information,
)
from tests.support.pagination import first_page, further_pages
from tests.support.requirements_map import requirement


@pytest.fixture()
def shortcode_post(
    active_instaloader: instaloader.Instaloader,
    integration_targets,
) -> instaloader.Post:
    shortcode = integration_targets.require("public_shortcode")
    return instaloader.Post.from_shortcode(active_instaloader.context, shortcode)


@requirement("post-basic-information")
def test_public_shortcode_caption_and_date_accessible(
    active_instaloader: instaloader.Instaloader,
    shortcode_post: instaloader.Post,
    output_dir: Path,
    post_checker_name: PostCheckerName,
    post_checker: PostChecker,
) -> None:
    post_checker(active_instaloader, shortcode_post, shortcode_post.shortcode)
    if post_checker_name == "download":
        assert_post_basic_information(shortcode_post)


@requirement("single-post-shortcode")
def test_public_shortcode_download(
    active_instaloader: instaloader.Instaloader,
    shortcode_post: instaloader.Post,
    output_dir: Path,
    post_checker_name: PostCheckerName,
    post_checker: PostChecker,
) -> None:
    post_checker(active_instaloader, shortcode_post, shortcode_post.shortcode)
    if post_checker_name == "download":
        shortcode = shortcode_post.shortcode
        downloaded_files = list(output_dir.joinpath(shortcode).glob(f"{shortcode}*"))
        assert downloaded_files


@requirement("post-likes-first-page-logged-in")
def test_shortcode_post_likes_first_page_listable(
    shortcode_post: instaloader.Post,
) -> None:
    for profile in first_page(
        shortcode_post.get_likes(), f"likes of post {shortcode_post.shortcode!r}"
    ):
        assert profile.username


@requirement("post-likes-further-pages-logged-in")
def test_shortcode_post_likes_further_pages_listable(
    shortcode_post: instaloader.Post,
    max_items: int,
) -> None:
    for profile in further_pages(
        shortcode_post.get_likes(),
        max_items,
        f"likes of post {shortcode_post.shortcode!r}",
    ):
        assert profile.username


@requirement("post-comments-first-page")
def test_shortcode_post_comments_first_page_listable(
    shortcode_post: instaloader.Post,
) -> None:
    for comment in first_page(
        shortcode_post.get_comments(),
        f"comments of post {shortcode_post.shortcode!r}",
    ):
        assert comment.owner.username


@requirement("post-comments-further-pages")
def test_shortcode_post_comments_further_pages_listable(
    shortcode_post: instaloader.Post,
    max_items: int,
) -> None:
    for comment in further_pages(
        shortcode_post.get_comments(),
        max_items,
        f"comments of post {shortcode_post.shortcode!r}",
    ):
        assert comment.owner.username


@requirement("post-geotag-logged-in")
def test_shortcode_post_geotag_accessible(shortcode_post: instaloader.Post) -> None:
    location = shortcode_post.location
    if location is None:
        pytest.skip(f"post {shortcode_post.shortcode!r} has no geotag")
    assert location.id
    assert location.name
