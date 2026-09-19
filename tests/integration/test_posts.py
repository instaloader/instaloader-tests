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
) -> tuple[str, instaloader.Post]:
    shortcode = integration_targets.require("public_shortcode")
    post = instaloader.Post.from_shortcode(active_instaloader.context, shortcode)
    return shortcode, post


@requirement("post-basic-information-anonymous")
def test_public_shortcode_caption_and_date_accessible(
    active_instaloader: instaloader.Instaloader,
    shortcode_post: tuple[str, instaloader.Post],
    output_dir: Path,
    post_checker_name: PostCheckerName,
    post_checker: PostChecker,
) -> None:
    shortcode, post = shortcode_post
    post_checker(active_instaloader, post, shortcode)
    if post_checker_name == "download":
        assert_post_basic_information(post)


@requirement("single-post-shortcode-anonymous")
def test_public_shortcode_download(
    active_instaloader: instaloader.Instaloader,
    shortcode_post: tuple[str, instaloader.Post],
    output_dir: Path,
    post_checker_name: PostCheckerName,
    post_checker: PostChecker,
) -> None:
    shortcode, post = shortcode_post
    post_checker(active_instaloader, post, shortcode)
    if post_checker_name == "download":
        downloaded_files = list(output_dir.joinpath(shortcode).glob(f"{shortcode}*"))
        assert downloaded_files


@requirement("post-likes-first-page-logged-in")
def test_shortcode_post_likes_first_page_listable(
    active_instaloader: instaloader.Instaloader,
    shortcode_post: tuple[str, instaloader.Post],
) -> None:
    del active_instaloader
    _, post = shortcode_post
    likes_found = False
    for profile in itertools.islice(post.get_likes(), 12):
        assert profile.username
        likes_found = True
    if not likes_found:
        pytest.skip(f"post {post.shortcode!r} has no likes")


@requirement("post-likes-further-pages-logged-in")
def test_shortcode_post_likes_further_pages_listable(
    active_instaloader: instaloader.Instaloader,
    shortcode_post: tuple[str, instaloader.Post],
    max_items: int,
) -> None:
    del active_instaloader
    _, post = shortcode_post
    likes_found = False
    stop_index = max(13, max_items)
    for profile in itertools.islice(post.get_likes(), 12, stop_index):
        assert profile.username
        likes_found = True
    if not likes_found:
        pytest.skip(f"post {post.shortcode!r} has no likes beyond the first page")


@requirement("post-comments-first-page-logged-in")
def test_shortcode_post_comments_first_page_listable(
    active_instaloader: instaloader.Instaloader,
    shortcode_post: tuple[str, instaloader.Post],
) -> None:
    del active_instaloader
    _, post = shortcode_post
    comments_found = False
    for comment in itertools.islice(post.get_comments(), 12):
        assert comment.owner.username
        comments_found = True
    if not comments_found:
        pytest.skip(f"post {post.shortcode!r} has no comments")
