from pathlib import Path

import instaloader

from tests.support.pagination import Pager
from tests.support.post_checkers import PostChecker
from tests.support.requirements_map import paged_requirement
from tests.support.targets import IntegrationTargets


@paged_requirement(
    "location-posts-first-page-logged-in",
    "location-posts-further-pages-logged-in",
)
def test_location_paged_posts_download(
    paginate: Pager,
    active_instaloader: instaloader.Instaloader,
    integration_targets: IntegrationTargets,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    location_id = integration_targets.require("location_id")
    for post in paginate(
        active_instaloader.get_location_posts(location_id), f"location {location_id!r}"
    ):
        post_checker(active_instaloader, post, f"%{location_id}")
