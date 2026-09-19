from __future__ import annotations

from collections.abc import Iterable, Iterator
from pathlib import Path

import instaloader
import pytest

from tests.support.requirements_map import requirement
from tests.support.targets import (
    FIRST_50_ITEM_COUNT,
    FIRST_PAGE_ITEM_COUNT,
    IntegrationTargets,
    require_target,
    require_target_or_fallback,
    take_first_items,
    take_up_to_items,
)


def _profile_from_username(
    loader: instaloader.Instaloader, username: str
) -> instaloader.Profile:
    return instaloader.Profile.from_username(loader.context, username)


def _download_profile_posts(
    loader: instaloader.Instaloader,
    profile: instaloader.Profile,
    *,
    max_count: int,
) -> None:
    loader.download_profiles(
        {profile}, profile_pic=False, raise_errors=True, max_count=max_count
    )


def _download_profile_collection(
    loader: instaloader.Instaloader,
    profile: instaloader.Profile,
    *,
    max_count: int,
    tagged: bool = False,
    reels: bool = False,
    igtv: bool = False,
) -> None:
    loader.download_profiles(
        {profile},
        profile_pic=False,
        posts=False,
        tagged=tagged,
        reels=reels,
        igtv=igtv,
        raise_errors=True,
        max_count=max_count,
    )


def _story_for_profile(
    loader: instaloader.Instaloader, profile: instaloader.Profile
) -> instaloader.Story:
    story = next(loader.get_stories(userids=[profile.userid]), None)
    if story is None:
        pytest.skip(
            f"configured target profile {profile.username!r} has no visible stories"
        )
    return story


def _download_story_items(
    loader: instaloader.Instaloader,
    items: list[instaloader.StoryItem] | tuple[instaloader.StoryItem, ...],
    *,
    target: str,
) -> None:
    for item in items:
        loader.download_storyitem(item, target=target)


def _highlight_items(
    highlights: Iterable[instaloader.Highlight],
) -> Iterator[instaloader.StoryItem]:
    for highlight in highlights:
        for item in highlight.get_items():
            yield item


@pytest.fixture(scope="module")
def public_profile_username(integration_targets: IntegrationTargets) -> str:
    return require_target(
        integration_targets.public_profile, option_name="--target-public-profile"
    )


@pytest.fixture(scope="module")
def tagged_profile_username(integration_targets: IntegrationTargets) -> str:
    return require_target_or_fallback(
        integration_targets.public_tagged_profile,
        option_name="--target-public-tagged-profile",
        fallback_value=integration_targets.public_profile,
        fallback_option_name="--target-public-profile",
    )


@pytest.fixture(scope="module")
def reels_profile_username(integration_targets: IntegrationTargets) -> str:
    return require_target_or_fallback(
        integration_targets.public_reels_profile,
        option_name="--target-public-reels-profile",
        fallback_value=integration_targets.public_profile,
        fallback_option_name="--target-public-profile",
    )


@pytest.fixture(scope="module")
def igtv_profile_username(integration_targets: IntegrationTargets) -> str:
    return require_target_or_fallback(
        integration_targets.public_igtv_profile,
        option_name="--target-public-igtv-profile",
        fallback_value=integration_targets.public_profile,
        fallback_option_name="--target-public-profile",
    )


@pytest.fixture(scope="module")
def story_profile_username(integration_targets: IntegrationTargets) -> str:
    return require_target(
        integration_targets.story_profile, option_name="--target-story-profile"
    )


@pytest.fixture(scope="module")
def highlight_profile_username(integration_targets: IntegrationTargets) -> str:
    return require_target(
        integration_targets.highlight_profile, option_name="--target-highlight-profile"
    )


@pytest.fixture(scope="module")
def anonymous_public_profile(
    anonymous_instaloader: instaloader.Instaloader,
    public_profile_username: str,
) -> instaloader.Profile:
    return _profile_from_username(anonymous_instaloader, public_profile_username)


@pytest.fixture(scope="module")
def logged_in_public_profile(
    logged_in_instaloader: instaloader.Instaloader,
    public_profile_username: str,
) -> instaloader.Profile:
    return _profile_from_username(logged_in_instaloader, public_profile_username)


@requirement("profile-picture-anonymous-critical")
def test_public_profile_picture_download(
    anonymous_instaloader: instaloader.Instaloader,
    anonymous_public_profile: instaloader.Profile,
    output_dir: Path,
) -> None:
    anonymous_instaloader.download_profilepic(anonymous_public_profile)


@requirement("profile-posts-first-page-anonymous-high")
def test_public_profile_first_page_posts_download_anonymous(
    anonymous_instaloader: instaloader.Instaloader,
    anonymous_public_profile: instaloader.Profile,
    output_dir: Path,
) -> None:
    take_first_items(
        anonymous_public_profile.get_posts(),
        count=FIRST_PAGE_ITEM_COUNT,
        description=f"public profile {anonymous_public_profile.username!r}",
    )
    _download_profile_posts(
        anonymous_instaloader,
        anonymous_public_profile,
        max_count=FIRST_PAGE_ITEM_COUNT,
    )


@requirement("profile-posts-first-50-anonymous-medium")
def test_public_profile_first_50_posts_download_anonymous(
    anonymous_instaloader: instaloader.Instaloader,
    anonymous_public_profile: instaloader.Profile,
    output_dir: Path,
) -> None:
    take_up_to_items(
        anonymous_public_profile.get_posts(),
        minimum_count=FIRST_PAGE_ITEM_COUNT + 1,
        maximum_count=FIRST_50_ITEM_COUNT,
        description=f"public profile {anonymous_public_profile.username!r}",
    )
    _download_profile_posts(
        anonymous_instaloader,
        anonymous_public_profile,
        max_count=FIRST_50_ITEM_COUNT,
    )


@requirement("profile-posts-first-page-logged-in-critical")
def test_public_profile_first_page_posts_download_logged_in(
    logged_in_instaloader: instaloader.Instaloader,
    logged_in_public_profile: instaloader.Profile,
    output_dir: Path,
) -> None:
    take_first_items(
        logged_in_public_profile.get_posts(),
        count=FIRST_PAGE_ITEM_COUNT,
        description=f"public profile {logged_in_public_profile.username!r}",
    )
    _download_profile_posts(
        logged_in_instaloader,
        logged_in_public_profile,
        max_count=FIRST_PAGE_ITEM_COUNT,
    )


@requirement("profile-posts-first-50-logged-in-critical")
def test_public_profile_first_50_posts_download_logged_in(
    logged_in_instaloader: instaloader.Instaloader,
    logged_in_public_profile: instaloader.Profile,
    output_dir: Path,
) -> None:
    take_up_to_items(
        logged_in_public_profile.get_posts(),
        minimum_count=FIRST_PAGE_ITEM_COUNT + 1,
        maximum_count=FIRST_50_ITEM_COUNT,
        description=f"public profile {logged_in_public_profile.username!r}",
    )
    _download_profile_posts(
        logged_in_instaloader,
        logged_in_public_profile,
        max_count=FIRST_50_ITEM_COUNT,
    )


@requirement("profile-tagged-first-page-anonymous-low")
def test_public_profile_tagged_first_page_download_anonymous(
    anonymous_instaloader: instaloader.Instaloader,
    tagged_profile_username: str,
    output_dir: Path,
) -> None:
    profile = _profile_from_username(anonymous_instaloader, tagged_profile_username)
    take_first_items(
        profile.get_tagged_posts(),
        count=FIRST_PAGE_ITEM_COUNT,
        description=f"tagged posts of profile {profile.username!r}",
    )
    _download_profile_collection(
        anonymous_instaloader,
        profile,
        max_count=FIRST_PAGE_ITEM_COUNT,
        tagged=True,
    )


@requirement("profile-tagged-first-50-anonymous-verylow")
def test_public_profile_tagged_first_50_download_anonymous(
    anonymous_instaloader: instaloader.Instaloader,
    tagged_profile_username: str,
    output_dir: Path,
) -> None:
    profile = _profile_from_username(anonymous_instaloader, tagged_profile_username)
    take_up_to_items(
        profile.get_tagged_posts(),
        minimum_count=FIRST_PAGE_ITEM_COUNT + 1,
        maximum_count=FIRST_50_ITEM_COUNT,
        description=f"tagged posts of profile {profile.username!r}",
    )
    _download_profile_collection(
        anonymous_instaloader,
        profile,
        max_count=FIRST_50_ITEM_COUNT,
        tagged=True,
    )


@requirement("profile-tagged-first-page-logged-in-medium")
def test_public_profile_tagged_first_page_download_logged_in(
    logged_in_instaloader: instaloader.Instaloader,
    tagged_profile_username: str,
    output_dir: Path,
) -> None:
    profile = _profile_from_username(logged_in_instaloader, tagged_profile_username)
    take_first_items(
        profile.get_tagged_posts(),
        count=FIRST_PAGE_ITEM_COUNT,
        description=f"tagged posts of profile {profile.username!r}",
    )
    _download_profile_collection(
        logged_in_instaloader,
        profile,
        max_count=FIRST_PAGE_ITEM_COUNT,
        tagged=True,
    )


@requirement("profile-tagged-first-50-logged-in-low")
def test_public_profile_tagged_first_50_download_logged_in(
    logged_in_instaloader: instaloader.Instaloader,
    tagged_profile_username: str,
    output_dir: Path,
) -> None:
    profile = _profile_from_username(logged_in_instaloader, tagged_profile_username)
    take_up_to_items(
        profile.get_tagged_posts(),
        minimum_count=FIRST_PAGE_ITEM_COUNT + 1,
        maximum_count=FIRST_50_ITEM_COUNT,
        description=f"tagged posts of profile {profile.username!r}",
    )
    _download_profile_collection(
        logged_in_instaloader,
        profile,
        max_count=FIRST_50_ITEM_COUNT,
        tagged=True,
    )


@requirement("profile-reels-first-page-anonymous-low")
def test_public_profile_reels_first_page_download_anonymous(
    anonymous_instaloader: instaloader.Instaloader,
    reels_profile_username: str,
    output_dir: Path,
) -> None:
    profile = _profile_from_username(anonymous_instaloader, reels_profile_username)
    take_first_items(
        profile.get_reels(),
        count=FIRST_PAGE_ITEM_COUNT,
        description=f"reels of profile {profile.username!r}",
    )
    _download_profile_collection(
        anonymous_instaloader,
        profile,
        max_count=FIRST_PAGE_ITEM_COUNT,
        reels=True,
    )


@requirement("profile-reels-first-50-anonymous-verylow")
def test_public_profile_reels_first_50_download_anonymous(
    anonymous_instaloader: instaloader.Instaloader,
    reels_profile_username: str,
    output_dir: Path,
) -> None:
    profile = _profile_from_username(anonymous_instaloader, reels_profile_username)
    take_up_to_items(
        profile.get_reels(),
        minimum_count=FIRST_PAGE_ITEM_COUNT + 1,
        maximum_count=FIRST_50_ITEM_COUNT,
        description=f"reels of profile {profile.username!r}",
    )
    _download_profile_collection(
        anonymous_instaloader,
        profile,
        max_count=FIRST_50_ITEM_COUNT,
        reels=True,
    )


@requirement("profile-reels-first-page-logged-in-medium")
def test_public_profile_reels_first_page_download_logged_in(
    logged_in_instaloader: instaloader.Instaloader,
    reels_profile_username: str,
    output_dir: Path,
) -> None:
    profile = _profile_from_username(logged_in_instaloader, reels_profile_username)
    take_first_items(
        profile.get_reels(),
        count=FIRST_PAGE_ITEM_COUNT,
        description=f"reels of profile {profile.username!r}",
    )
    _download_profile_collection(
        logged_in_instaloader,
        profile,
        max_count=FIRST_PAGE_ITEM_COUNT,
        reels=True,
    )


@requirement("profile-reels-first-50-logged-in-low")
def test_public_profile_reels_first_50_download_logged_in(
    logged_in_instaloader: instaloader.Instaloader,
    reels_profile_username: str,
    output_dir: Path,
) -> None:
    profile = _profile_from_username(logged_in_instaloader, reels_profile_username)
    take_up_to_items(
        profile.get_reels(),
        minimum_count=FIRST_PAGE_ITEM_COUNT + 1,
        maximum_count=FIRST_50_ITEM_COUNT,
        description=f"reels of profile {profile.username!r}",
    )
    _download_profile_collection(
        logged_in_instaloader,
        profile,
        max_count=FIRST_50_ITEM_COUNT,
        reels=True,
    )


@requirement("profile-igtv-first-page-anonymous-low")
def test_public_profile_igtv_first_page_download_anonymous(
    anonymous_instaloader: instaloader.Instaloader,
    igtv_profile_username: str,
    output_dir: Path,
) -> None:
    profile = _profile_from_username(anonymous_instaloader, igtv_profile_username)
    take_first_items(
        profile.get_igtv_posts(),
        count=FIRST_PAGE_ITEM_COUNT,
        description=f"IGTV posts of profile {profile.username!r}",
    )
    _download_profile_collection(
        anonymous_instaloader,
        profile,
        max_count=FIRST_PAGE_ITEM_COUNT,
        igtv=True,
    )


@requirement("profile-igtv-first-50-anonymous-verylow")
def test_public_profile_igtv_first_50_download_anonymous(
    anonymous_instaloader: instaloader.Instaloader,
    igtv_profile_username: str,
    output_dir: Path,
) -> None:
    profile = _profile_from_username(anonymous_instaloader, igtv_profile_username)
    take_up_to_items(
        profile.get_igtv_posts(),
        minimum_count=FIRST_PAGE_ITEM_COUNT + 1,
        maximum_count=FIRST_50_ITEM_COUNT,
        description=f"IGTV posts of profile {profile.username!r}",
    )
    _download_profile_collection(
        anonymous_instaloader,
        profile,
        max_count=FIRST_50_ITEM_COUNT,
        igtv=True,
    )


@requirement("profile-igtv-first-page-logged-in-medium")
def test_public_profile_igtv_first_page_download_logged_in(
    logged_in_instaloader: instaloader.Instaloader,
    igtv_profile_username: str,
    output_dir: Path,
) -> None:
    profile = _profile_from_username(logged_in_instaloader, igtv_profile_username)
    take_first_items(
        profile.get_igtv_posts(),
        count=FIRST_PAGE_ITEM_COUNT,
        description=f"IGTV posts of profile {profile.username!r}",
    )
    _download_profile_collection(
        logged_in_instaloader,
        profile,
        max_count=FIRST_PAGE_ITEM_COUNT,
        igtv=True,
    )


@requirement("profile-igtv-first-50-logged-in-low")
def test_public_profile_igtv_first_50_download_logged_in(
    logged_in_instaloader: instaloader.Instaloader,
    igtv_profile_username: str,
    output_dir: Path,
) -> None:
    profile = _profile_from_username(logged_in_instaloader, igtv_profile_username)
    take_up_to_items(
        profile.get_igtv_posts(),
        minimum_count=FIRST_PAGE_ITEM_COUNT + 1,
        maximum_count=FIRST_50_ITEM_COUNT,
        description=f"IGTV posts of profile {profile.username!r}",
    )
    _download_profile_collection(
        logged_in_instaloader,
        profile,
        max_count=FIRST_50_ITEM_COUNT,
        igtv=True,
    )


@requirement("profile-stories-first-page-logged-in-high")
def test_profile_story_items_first_page_download(
    logged_in_instaloader: instaloader.Instaloader,
    story_profile_username: str,
    output_dir: Path,
) -> None:
    profile = _profile_from_username(logged_in_instaloader, story_profile_username)
    story = _story_for_profile(logged_in_instaloader, profile)
    story_items = take_first_items(
        story.get_items(),
        count=FIRST_PAGE_ITEM_COUNT,
        description=f"story items of profile {profile.username!r}",
    )
    _download_story_items(
        logged_in_instaloader, story_items, target=f"{profile.username}:stories"
    )


@requirement("profile-stories-first-50-logged-in-medium")
def test_profile_story_items_first_50_download(
    logged_in_instaloader: instaloader.Instaloader,
    story_profile_username: str,
    output_dir: Path,
) -> None:
    profile = _profile_from_username(logged_in_instaloader, story_profile_username)
    story = _story_for_profile(logged_in_instaloader, profile)
    story_items = take_up_to_items(
        story.get_items(),
        minimum_count=FIRST_PAGE_ITEM_COUNT + 1,
        maximum_count=FIRST_50_ITEM_COUNT,
        description=f"story items of profile {profile.username!r}",
    )
    _download_story_items(
        logged_in_instaloader, story_items, target=f"{profile.username}:stories"
    )


@requirement("profile-highlights-first-page-logged-in-high")
def test_profile_highlights_first_page_download(
    logged_in_instaloader: instaloader.Instaloader,
    highlight_profile_username: str,
    output_dir: Path,
) -> None:
    profile = _profile_from_username(logged_in_instaloader, highlight_profile_username)
    highlight_items = take_first_items(
        _highlight_items(logged_in_instaloader.get_highlights(profile)),
        count=FIRST_PAGE_ITEM_COUNT,
        description=f"highlight items of profile {profile.username!r}",
    )
    _download_story_items(
        logged_in_instaloader,
        highlight_items,
        target=f"{profile.username}:highlights",
    )


@requirement("profile-highlights-first-50-logged-in-medium")
def test_profile_highlights_first_50_download(
    logged_in_instaloader: instaloader.Instaloader,
    highlight_profile_username: str,
    output_dir: Path,
) -> None:
    profile = _profile_from_username(logged_in_instaloader, highlight_profile_username)
    highlight_items = take_up_to_items(
        _highlight_items(logged_in_instaloader.get_highlights(profile)),
        minimum_count=FIRST_PAGE_ITEM_COUNT + 1,
        maximum_count=FIRST_50_ITEM_COUNT,
        description=f"highlight items of profile {profile.username!r}",
    )
    _download_story_items(
        logged_in_instaloader,
        highlight_items,
        target=f"{profile.username}:highlights",
    )
