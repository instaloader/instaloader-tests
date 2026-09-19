from pathlib import Path
import itertools

import instaloader
import pytest

from tests.support.post_checkers import (
    PostChecker,
    PostCheckerName,
    assert_post_basic_information,
)
from tests.support.requirements_map import requirement


@pytest.fixture()
def shortcode_post(
    active_instaloader: instaloader.Instaloader,
    integration_targets,
) -> instaloader.Post:
    shortcode = integration_targets.require("public_shortcode")
    return instaloader.Post.from_shortcode(active_instaloader.context, shortcode)


@requirement("post-basic-information-anonymous")
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


@requirement("single-post-shortcode-anonymous")
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
    likes_found = False
    for profile in itertools.islice(shortcode_post.get_likes(), 12):
        assert profile.username
        likes_found = True
    if not likes_found:
        pytest.skip(f"post {shortcode_post.shortcode!r} has no likes")


@requirement("post-likes-further-pages-logged-in")
def test_shortcode_post_likes_further_pages_listable(
    shortcode_post: instaloader.Post,
    max_items: int,
) -> None:
    likes_found = False
    for profile in itertools.islice(shortcode_post.get_likes(), 12, max_items):
        assert profile.username
        likes_found = True
    if not likes_found:
        pytest.skip(
            f"post {shortcode_post.shortcode!r} has no likes beyond the first page"
        )


@requirement("post-comments-first-page-logged-in")
def test_shortcode_post_comments_first_page_listable(
    shortcode_post: instaloader.Post,
) -> None:
    comments_found = False
    for comment in itertools.islice(shortcode_post.get_comments(), 12):
        assert comment.owner.username
        comments_found = True
    if not comments_found:
        pytest.skip(f"post {shortcode_post.shortcode!r} has no comments")


@requirement("post-comments-further-pages-logged-in")
def test_shortcode_post_comments_further_pages_listable(
    shortcode_post: instaloader.Post,
    max_items: int,
) -> None:
    comments_found = False
    for comment in itertools.islice(shortcode_post.get_comments(), 12, max_items):
        assert comment.owner.username
        comments_found = True
    if not comments_found:
        pytest.skip(
            f"post {shortcode_post.shortcode!r} has no comments beyond the first page"
        )
