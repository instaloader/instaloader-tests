from collections.abc import Callable
from datetime import datetime
from typing import Literal

import instaloader
import pytest

PostCheckerName = Literal["download", "fast"]
PostChecker = Callable[[instaloader.Instaloader, instaloader.Post, str], None]


def check_post_by_download(
    loader: instaloader.Instaloader, post: instaloader.Post, target: str
) -> None:
    loader.download_post(post, target=target)


def check_post_basic_information(
    loader: instaloader.Instaloader, post: instaloader.Post, target: str
) -> None:
    del loader, target
    if not post.caption:
        pytest.skip("checked post has no caption")

    assert_post_basic_information(post)


def assert_post_basic_information(post: instaloader.Post) -> None:
    assert isinstance(post.caption, str)
    assert post.caption.strip()
    assert isinstance(post.date_utc, datetime)


POST_CHECKERS: dict[PostCheckerName, PostChecker] = {
    "download": check_post_by_download,
    "fast": check_post_basic_information,
}


def load_post_checker(name: PostCheckerName) -> PostChecker:
    return POST_CHECKERS[name]
