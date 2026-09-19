import itertools
from pathlib import Path
from collections.abc import Iterator

import instaloader
import pytest

from tests.support.requirements_map import requirement

SAVED_POSTS_FIRST_PAGE_COUNT = 12
SAVED_POSTS_EXTENDED_UPPER_BOUND = 50


def _saved_posts_slice(
    profile: instaloader.Profile,
    *,
    start: int,
    stop: int,
    skip_if_empty: bool,
) -> Iterator[instaloader.Post]:
    sliced_iterator = itertools.islice(profile.get_saved_posts(), start, stop)
    if not skip_if_empty:
        return sliced_iterator

    first_post = next(sliced_iterator, None)
    if first_post is None:
        pytest.skip(
            f"configured target does not provide items in range [{start}, {stop}) "
            f"for saved posts of {profile.username!r}"
        )
    return itertools.chain((first_post,), sliced_iterator)


@pytest.fixture(scope="module")
def saved_posts_first_page(
    logged_in_instaloader: instaloader.Instaloader,
    request: pytest.FixtureRequest,
) -> Iterator[instaloader.Post]:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    start, stop = getattr(request, "param", (0, SAVED_POSTS_FIRST_PAGE_COUNT))
    return _saved_posts_slice(profile, start=start, stop=stop, skip_if_empty=False)


@pytest.fixture(scope="module")
def saved_posts_extended(
    logged_in_instaloader: instaloader.Instaloader,
    request: pytest.FixtureRequest,
) -> Iterator[instaloader.Post]:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    start, stop = getattr(
        request,
        "param",
        (SAVED_POSTS_FIRST_PAGE_COUNT, SAVED_POSTS_EXTENDED_UPPER_BOUND),
    )
    return _saved_posts_slice(profile, start=start, stop=stop, skip_if_empty=True)


@requirement("saved-posts-first-page-logged-in-critical")
@pytest.mark.parametrize(
    "saved_posts_first_page",
    [(0, SAVED_POSTS_FIRST_PAGE_COUNT)],
    ids=["first-page-default"],
    indirect=True,
)
def test_saved_posts_first_page_download(
    logged_in_instaloader: instaloader.Instaloader,
    saved_posts_first_page: Iterator[instaloader.Post],
    output_dir: Path,
) -> None:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    for post in saved_posts_first_page:
        logged_in_instaloader.download_post(post, target=f"{profile.username}-saved")


@requirement("saved-posts-first-50-logged-in-critical")
@pytest.mark.parametrize(
    "saved_posts_extended",
    [(SAVED_POSTS_FIRST_PAGE_COUNT, SAVED_POSTS_EXTENDED_UPPER_BOUND)],
    ids=["extended-default"],
    indirect=True,
)
def test_saved_posts_extended_download(
    logged_in_instaloader: instaloader.Instaloader,
    saved_posts_extended: Iterator[instaloader.Post],
    output_dir: Path,
) -> None:
    profile = instaloader.Profile.own_profile(logged_in_instaloader.context)
    for post in saved_posts_extended:
        logged_in_instaloader.download_post(post, target=f"{profile.username}-saved")
