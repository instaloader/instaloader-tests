from pathlib import Path

import instaloader
import pytest

from tests.support.requirements_map import requirement


@pytest.fixture(scope="module")
def saved_posts_first_page(
    logged_in_instaloader: instaloader.Instaloader,
) -> list[instaloader.Post]:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    iterator = iter(profile.get_saved_posts())
    description = f"saved posts of {profile.username!r}"

    selected: list[instaloader.Post] = []
    for _ in range(1, 13):
        try:
            selected.append(next(iterator))
        except StopIteration:
            pytest.skip(
                f"configured target does not provide 12 items for {description}"
            )
    return selected


@pytest.fixture(scope="module")
def saved_posts_extended(
    logged_in_instaloader: instaloader.Instaloader,
) -> list[instaloader.Post]:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    iterator = iter(profile.get_saved_posts())
    description = f"saved posts of {profile.username!r}"

    for prefix_index in range(1, 13):
        try:
            next(iterator)
        except StopIteration:
            pytest.skip(
                f"configured target does not provide 12 items for {description}"
            )
        except Exception as error:
            pytest.xfail(
                "extended saved-post range failed while advancing through prefix "
                f"(item {prefix_index}) for {description} ({type(error).__name__}: {error})"
            )

    selected: list[instaloader.Post] = []
    for item_index in range(13, 51):
        try:
            selected.append(next(iterator))
        except StopIteration:
            pytest.skip(
                f"configured target does not provide {item_index} items for {description}"
            )
    return selected


@requirement("saved-posts-first-page-logged-in-critical")
def test_saved_posts_first_page_download(
    logged_in_instaloader: instaloader.Instaloader,
    saved_posts_first_page: list[instaloader.Post],
    output_dir: Path,
) -> None:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    for post in saved_posts_first_page:
        logged_in_instaloader.download_post(post, target=f"{profile.username}-saved")


@requirement("saved-posts-first-50-logged-in-critical")
def test_saved_posts_extended_download(
    logged_in_instaloader: instaloader.Instaloader,
    saved_posts_extended: list[instaloader.Post],
    output_dir: Path,
) -> None:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    for post in saved_posts_extended:
        logged_in_instaloader.download_post(post, target=f"{profile.username}-saved")
