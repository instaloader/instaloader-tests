import itertools
from pathlib import Path

import instaloader
import pytest

from tests.support.post_checkers import PostChecker
from tests.support.requirements_map import requirement


@requirement("feed-first-page-logged-in")
def test_feed_first_page_posts_download(
    active_instaloader: instaloader.Instaloader,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    feed_posts_found = False
    for post in itertools.islice(active_instaloader.get_feed_posts(), 12):
        post_checker(active_instaloader, post, "feed")
        feed_posts_found = True
    if not feed_posts_found:
        pytest.skip("feed returned no posts")


@requirement("feed-further-pages-logged-in")
def test_feed_further_pages_posts_download(
    active_instaloader: instaloader.Instaloader,
    max_items: int,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    feed_posts_found = False
    for post in itertools.islice(active_instaloader.get_feed_posts(), 12, max_items):
        post_checker(active_instaloader, post, "feed")
        feed_posts_found = True
    if not feed_posts_found:
        pytest.skip("feed returned no posts beyond the first page")


@requirement("stories-first-page-logged-in")
def test_visible_stories_first_page_download(
    active_instaloader: instaloader.Instaloader,
    output_dir: Path,
) -> None:
    stories_found = False
    for story in itertools.islice(active_instaloader.get_stories(), 12):
        first_item = next(iter(story.get_items()), None)
        if first_item is None:
            continue
        active_instaloader.download_storyitem(first_item, "stories")
        stories_found = True
    if not stories_found:
        pytest.skip("no visible stories with downloadable items")


@requirement("stories-further-pages-logged-in")
def test_visible_stories_further_pages_download(
    active_instaloader: instaloader.Instaloader,
    max_items: int,
    output_dir: Path,
) -> None:
    stories_found = False
    for story in itertools.islice(active_instaloader.get_stories(), 12, max_items):
        first_item = next(iter(story.get_items()), None)
        if first_item is None:
            continue
        active_instaloader.download_storyitem(first_item, "stories")
        stories_found = True
    if not stories_found:
        pytest.skip("no visible stories with downloadable items beyond the first page")
