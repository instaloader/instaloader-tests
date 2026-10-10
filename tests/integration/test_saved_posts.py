from pathlib import Path

import instaloader
from tests.support.post_checkers import PostChecker
from tests.support.pagination import first_page, further_pages
from tests.support.requirements_map import requirement


@requirement("saved-posts-first-page-logged-in")
def test_saved_posts_first_page_download(
    logged_in_instaloader: instaloader.Instaloader,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    for post in first_page(
        profile.get_saved_posts(), f"saved posts of {profile.username!r}"
    ):
        post_checker(logged_in_instaloader, post, f"{profile.username}-saved")


@requirement("saved-posts-further-pages-logged-in")
def test_saved_posts_further_pages_download(
    logged_in_instaloader: instaloader.Instaloader,
    max_items: int,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    for post in further_pages(
        profile.get_saved_posts(), max_items, f"saved posts of {profile.username!r}"
    ):
        post_checker(logged_in_instaloader, post, f"{profile.username}-saved")
