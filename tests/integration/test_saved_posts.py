from pathlib import Path

import instaloader
from tests.support.post_checkers import PostChecker
from tests.support.pagination import Pager
from tests.support.requirements_map import paged_requirement


@paged_requirement(
    "saved-posts-first-page-logged-in",
    "saved-posts-further-pages-logged-in",
)
def test_saved_posts_paged_download(
    paginate: Pager,
    logged_in_instaloader: instaloader.Instaloader,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    for post in paginate(
        profile.get_saved_posts(), f"saved posts of {profile.username!r}"
    ):
        post_checker(logged_in_instaloader, post, f"{profile.username}-saved")
