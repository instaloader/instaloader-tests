from pathlib import Path

import instaloader

from tests.support.pagination import first_page, further_pages
from tests.support.post_checkers import PostChecker
from tests.support.requirements_map import requirement
from tests.support.targets import IntegrationTargets


@requirement("location-posts-first-page-logged-in")
def test_location_first_page_posts_download(
    active_instaloader: instaloader.Instaloader,
    integration_targets: IntegrationTargets,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    location_id = integration_targets.require("location_id")
    for post in first_page(
        active_instaloader.get_location_posts(location_id), f"location {location_id!r}"
    ):
        post_checker(active_instaloader, post, f"%{location_id}")


@requirement("location-posts-further-pages-logged-in")
def test_location_further_pages_posts_download(
    active_instaloader: instaloader.Instaloader,
    integration_targets: IntegrationTargets,
    max_items: int,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    location_id = integration_targets.require("location_id")
    for post in further_pages(
        active_instaloader.get_location_posts(location_id),
        max_items,
        f"location {location_id!r}",
    ):
        post_checker(active_instaloader, post, f"%{location_id}")
