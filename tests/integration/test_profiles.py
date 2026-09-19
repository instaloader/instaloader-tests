import itertools
from pathlib import Path

import instaloader
import pytest

from tests.support.post_checkers import PostChecker
from tests.support.requirements_map import Authentication, requirement
from tests.support.targets import IntegrationTargets


@pytest.fixture(scope="session")
def profile_cache() -> dict[tuple[Authentication, str], instaloader.Profile]:
    return {}


def _profile_from_username(
    context: instaloader.InstaloaderContext,
    authentication: Authentication,
    username: str,
    profile_cache: dict[tuple[Authentication, str], instaloader.Profile],
) -> instaloader.Profile:
    cache_key = (authentication, username)
    if cache_key not in profile_cache:
        profile_cache[cache_key] = instaloader.Profile.from_username(context, username)
    return profile_cache[cache_key]


@pytest.fixture()
def public_profile(
    active_authentication: Authentication,
    active_instaloader: instaloader.Instaloader,
    integration_targets: IntegrationTargets,
    profile_cache: dict[tuple[Authentication, str], instaloader.Profile],
) -> instaloader.Profile:
    username = integration_targets.require("public_profile")
    return _profile_from_username(
        active_instaloader.context,
        active_authentication,
        username,
        profile_cache,
    )


@pytest.fixture()
def private_profile(
    integration_targets: IntegrationTargets,
    logged_in_instaloader: instaloader.Instaloader,
    profile_cache: dict[tuple[Authentication, str], instaloader.Profile],
) -> instaloader.Profile:
    return _profile_from_username(
        logged_in_instaloader.context,
        Authentication.LOGGED_IN,
        integration_targets.require("private_profile"),
        profile_cache,
    )


@requirement("profile-picture-anonymous")
def test_public_profile_picture_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    output_dir: Path,
) -> None:
    active_instaloader.download_profilepic(public_profile)


@requirement("profile-posts-first-page-anonymous")
def test_public_profile_first_page_posts_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in itertools.islice(public_profile.get_posts(), 12):
        post_checker(active_instaloader, post, public_profile.username)


@requirement("profile-posts-further-pages")
def test_public_profile_further_pages_posts_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    max_items: int,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    further_posts = False
    stop_index = max(13, max_items)
    for post in itertools.islice(public_profile.get_posts(), 12, stop_index):
        post_checker(active_instaloader, post, public_profile.username)
        further_posts = True
    if not further_posts:
        pytest.skip(
            f"configured target does not provide more than 12 items for profile {public_profile.username!r}"
        )


@requirement("profile-picture-private-logged-in")
def test_private_profile_picture_download(
    active_instaloader: instaloader.Instaloader,
    private_profile: instaloader.Profile,
    output_dir: Path,
) -> None:
    active_instaloader.download_profilepic(private_profile)


@requirement("profile-posts-first-page-private-logged-in")
def test_private_profile_first_page_posts_download(
    active_instaloader: instaloader.Instaloader,
    private_profile: instaloader.Profile,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in itertools.islice(private_profile.get_posts(), 12):
        post_checker(active_instaloader, post, private_profile.username)


@requirement("profile-stories-first-page-logged-in")
def test_profile_stories_first_page_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    output_dir: Path,
) -> None:
    stories = list(
        itertools.islice(active_instaloader.get_stories([public_profile.userid]), 1)
    )
    if not stories:
        pytest.skip(f"profile {public_profile.username!r} has no visible stories")
    story_items_found = False
    for story_item in itertools.islice(stories[0].get_items(), 12):
        active_instaloader.download_storyitem(
            story_item, f"{public_profile.username}-stories"
        )
        story_items_found = True
    if not story_items_found:
        pytest.skip(
            f"profile {public_profile.username!r} stories contain no downloadable items"
        )


@requirement("profile-stories-further-pages-logged-in")
def test_profile_stories_further_pages_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    max_items: int,
    output_dir: Path,
) -> None:
    stories = list(
        itertools.islice(active_instaloader.get_stories([public_profile.userid]), 1)
    )
    if not stories:
        pytest.skip(f"profile {public_profile.username!r} has no visible stories")
    story_items_found = False
    for story_item in itertools.islice(stories[0].get_items(), 12, max_items):
        active_instaloader.download_storyitem(
            story_item, f"{public_profile.username}-stories"
        )
        story_items_found = True
    if not story_items_found:
        pytest.skip(
            f"profile {public_profile.username!r} stories contain no downloadable items beyond the first page"
        )


@requirement("profile-highlights-cover-picture-logged-in")
def test_profile_highlight_cover_picture_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    output_dir: Path,
) -> None:
    highlight = next(iter(active_instaloader.get_highlights(public_profile)), None)
    if highlight is None:
        pytest.skip(f"profile {public_profile.username!r} has no highlights")
    active_instaloader.download_title_pic(
        highlight.cover_url,
        f"{public_profile.username}-{highlight.title}",
        "cover",
        None,
    )


@requirement("profile-highlights-first-page-logged-in")
def test_profile_highlights_first_page_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    output_dir: Path,
) -> None:
    highlights_found = False
    for highlight in itertools.islice(
        active_instaloader.get_highlights(public_profile), 12
    ):
        first_item = next(iter(highlight.get_items()), None)
        if first_item is None:
            continue
        active_instaloader.download_storyitem(
            first_item, f"{public_profile.username}-{highlight.title}"
        )
        highlights_found = True
    if not highlights_found:
        pytest.skip(
            f"profile {public_profile.username!r} has no downloadable highlight items"
        )


@requirement("profile-highlights-further-pages-logged-in")
def test_profile_highlights_further_pages_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    max_items: int,
    output_dir: Path,
) -> None:
    highlights_found = False
    for highlight in itertools.islice(
        active_instaloader.get_highlights(public_profile), 12, max_items
    ):
        first_item = next(iter(highlight.get_items()), None)
        if first_item is None:
            continue
        active_instaloader.download_storyitem(
            first_item, f"{public_profile.username}-{highlight.title}"
        )
        highlights_found = True
    if not highlights_found:
        pytest.skip(
            f"profile {public_profile.username!r} has no downloadable highlight items beyond the first page"
        )


@requirement("profile-followers-first-page-logged-in")
def test_profile_followers_first_page_listable(
    public_profile: instaloader.Profile,
) -> None:
    followers_found = False
    for follower in itertools.islice(public_profile.get_followers(), 12):
        assert follower.username
        followers_found = True
    if not followers_found:
        pytest.skip(f"profile {public_profile.username!r} has no followers to list")


@requirement("profile-followers-further-pages-logged-in")
def test_profile_followers_further_pages_listable(
    public_profile: instaloader.Profile,
    max_items: int,
) -> None:
    followers_found = False
    for follower in itertools.islice(public_profile.get_followers(), 12, max_items):
        assert follower.username
        followers_found = True
    if not followers_found:
        pytest.skip(
            f"profile {public_profile.username!r} has no followers beyond the first page"
        )


@requirement("profile-followees-first-page-logged-in")
def test_profile_followees_first_page_listable(
    public_profile: instaloader.Profile,
) -> None:
    followees_found = False
    for followee in itertools.islice(public_profile.get_followees(), 12):
        assert followee.username
        followees_found = True
    if not followees_found:
        pytest.skip(f"profile {public_profile.username!r} has no followees to list")


@requirement("profile-followees-further-pages-logged-in")
def test_profile_followees_further_pages_listable(
    public_profile: instaloader.Profile,
    max_items: int,
) -> None:
    followees_found = False
    for followee in itertools.islice(public_profile.get_followees(), 12, max_items):
        assert followee.username
        followees_found = True
    if not followees_found:
        pytest.skip(
            f"profile {public_profile.username!r} has no followees beyond the first page"
        )
