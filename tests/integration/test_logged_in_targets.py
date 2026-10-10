from pathlib import Path

import instaloader

from tests.support.post_checkers import PostChecker
from tests.support.pagination import first_page, further_pages
from tests.support.requirements_map import requirement


@requirement("feed-first-page-logged-in")
def test_feed_first_page_posts_download(
    active_instaloader: instaloader.Instaloader,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in first_page(active_instaloader.get_feed_posts(), "feed"):
        post_checker(active_instaloader, post, "feed")


@requirement("feed-further-pages-logged-in")
def test_feed_further_pages_posts_download(
    active_instaloader: instaloader.Instaloader,
    max_items: int,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in further_pages(active_instaloader.get_feed_posts(), max_items, "feed"):
        post_checker(active_instaloader, post, "feed")


@requirement("stories-first-page-logged-in")
def test_visible_stories_first_page_download(
    active_instaloader: instaloader.Instaloader,
    output_dir: Path,
) -> None:
    for story in first_page(active_instaloader.get_stories(), "visible stories"):
        first_item = next(iter(story.get_items()), None)
        if first_item is not None:
            active_instaloader.download_storyitem(first_item, "stories")


@requirement("stories-further-pages-logged-in")
def test_visible_stories_further_pages_download(
    active_instaloader: instaloader.Instaloader,
    max_items: int,
    output_dir: Path,
) -> None:
    for story in further_pages(
        active_instaloader.get_stories(), max_items, "visible stories"
    ):
        first_item = next(iter(story.get_items()), None)
        if first_item is not None:
            active_instaloader.download_storyitem(first_item, "stories")
