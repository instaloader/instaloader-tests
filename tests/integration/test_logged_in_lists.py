from __future__ import annotations

from collections.abc import Iterable, Iterator
from pathlib import Path

import instaloader

from tests.support.requirements_map import requirement
from tests.support.targets import (
    FIRST_50_ITEM_COUNT,
    FIRST_PAGE_ITEM_COUNT,
    take_first_items,
    take_up_to_items,
)


def _story_items(
    stories: Iterable[instaloader.Story],
) -> Iterator[tuple[str, instaloader.StoryItem]]:
    for story in stories:
        for item in story.get_items():
            yield story.owner_username, item


def _download_story_items(
    logged_in_instaloader: instaloader.Instaloader,
    story_items: (
        list[tuple[str, instaloader.StoryItem]]
        | tuple[tuple[str, instaloader.StoryItem], ...]
    ),
) -> None:
    for target, item in story_items:
        logged_in_instaloader.download_storyitem(item, target=target)


def _saved_posts(
    logged_in_instaloader: instaloader.Instaloader,
) -> instaloader.NodeIterator[instaloader.Post]:
    return instaloader.Profile.own_profile(
        logged_in_instaloader.context
    ).get_saved_posts()


@requirement("saved-posts-first-page-logged-in-critical")
def test_saved_posts_first_page_download(
    logged_in_instaloader: instaloader.Instaloader,
    output_dir: Path,
) -> None:
    take_first_items(
        _saved_posts(logged_in_instaloader),
        count=FIRST_PAGE_ITEM_COUNT,
        description="logged-in user's saved posts",
    )
    logged_in_instaloader.download_saved_posts(max_count=FIRST_PAGE_ITEM_COUNT)


@requirement("saved-posts-first-50-logged-in-critical")
def test_saved_posts_first_50_download(
    logged_in_instaloader: instaloader.Instaloader,
    output_dir: Path,
) -> None:
    take_up_to_items(
        _saved_posts(logged_in_instaloader),
        minimum_count=FIRST_PAGE_ITEM_COUNT + 1,
        maximum_count=FIRST_50_ITEM_COUNT,
        description="logged-in user's saved posts",
    )
    logged_in_instaloader.download_saved_posts(max_count=FIRST_50_ITEM_COUNT)


@requirement("feed-first-page-logged-in-high")
def test_feed_first_page_download(
    logged_in_instaloader: instaloader.Instaloader,
    output_dir: Path,
) -> None:
    take_first_items(
        logged_in_instaloader.get_feed_posts(),
        count=FIRST_PAGE_ITEM_COUNT,
        description="logged-in user's feed",
    )
    logged_in_instaloader.download_feed_posts(max_count=FIRST_PAGE_ITEM_COUNT)


@requirement("feed-first-50-logged-in-medium")
def test_feed_first_50_download(
    logged_in_instaloader: instaloader.Instaloader,
    output_dir: Path,
) -> None:
    take_up_to_items(
        logged_in_instaloader.get_feed_posts(),
        minimum_count=FIRST_PAGE_ITEM_COUNT + 1,
        maximum_count=FIRST_50_ITEM_COUNT,
        description="logged-in user's feed",
    )
    logged_in_instaloader.download_feed_posts(max_count=FIRST_50_ITEM_COUNT)


@requirement("stories-first-page-logged-in-high")
def test_visible_stories_first_page_download(
    logged_in_instaloader: instaloader.Instaloader,
    output_dir: Path,
) -> None:
    story_items = take_first_items(
        _story_items(logged_in_instaloader.get_stories()),
        count=FIRST_PAGE_ITEM_COUNT,
        description="currently-visible story items",
    )
    _download_story_items(logged_in_instaloader, story_items)


@requirement("stories-first-50-logged-in-medium")
def test_visible_stories_first_50_download(
    logged_in_instaloader: instaloader.Instaloader,
    output_dir: Path,
) -> None:
    story_items = take_up_to_items(
        _story_items(logged_in_instaloader.get_stories()),
        minimum_count=FIRST_PAGE_ITEM_COUNT + 1,
        maximum_count=FIRST_50_ITEM_COUNT,
        description="currently-visible story items",
    )
    _download_story_items(logged_in_instaloader, story_items)
