from pathlib import Path

import instaloader

from tests.support.post_checkers import PostChecker
from tests.support.pagination import Pager
from tests.support.requirements_map import paged_requirement


@paged_requirement(
    "feed-first-page-logged-in",
    "feed-further-pages-logged-in",
)
def test_feed_paged_posts_download(
    paginate: Pager,
    active_instaloader: instaloader.Instaloader,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in paginate(active_instaloader.get_feed_posts(), "feed"):
        post_checker(active_instaloader, post, "feed")


@paged_requirement(
    "stories-first-page-logged-in",
    "stories-further-pages-logged-in",
)
def test_visible_stories_paged_download(
    paginate: Pager,
    active_instaloader: instaloader.Instaloader,
    output_dir: Path,
) -> None:
    for story in paginate(active_instaloader.get_stories(), "visible stories"):
        first_item = next(iter(story.get_items()), None)
        if first_item is not None:
            active_instaloader.download_storyitem(first_item, "stories")
