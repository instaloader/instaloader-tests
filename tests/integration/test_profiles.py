import itertools
from pathlib import Path

import instaloader
import pytest

from tests.support.post_checkers import PostChecker
from tests.support.pagination import Pager
from tests.support.requirements_map import (
    Authentication,
    paged_requirement,
    requirement,
)
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


@requirement("profile-picture-public")
def test_public_profile_picture_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    output_dir: Path,
) -> None:
    active_instaloader.download_profilepic(public_profile)


@paged_requirement(
    "profile-posts-first-page-public",
    "profile-posts-further-pages",
)
def test_public_profile_paged_posts_download(
    paginate: Pager,
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in paginate(
        public_profile.get_posts(), f"profile {public_profile.username!r}"
    ):
        post_checker(active_instaloader, post, public_profile.username)


@requirement("profile-picture-private-logged-in")
def test_private_profile_picture_download(
    active_instaloader: instaloader.Instaloader,
    private_profile: instaloader.Profile,
    output_dir: Path,
) -> None:
    active_instaloader.download_profilepic(private_profile)


@paged_requirement(
    "profile-posts-first-page-private-logged-in",
    "profile-posts-further-pages-private-logged-in",
)
def test_private_profile_paged_posts_download(
    paginate: Pager,
    active_instaloader: instaloader.Instaloader,
    private_profile: instaloader.Profile,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in paginate(
        private_profile.get_posts(), f"profile {private_profile.username!r}"
    ):
        post_checker(active_instaloader, post, private_profile.username)


@paged_requirement(
    "profile-tagged-posts-first-page",
    "profile-tagged-posts-further-pages",
)
def test_profile_tagged_posts_paged_download(
    paginate: Pager,
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in paginate(
        public_profile.get_tagged_posts(), f"profile {public_profile.username!r}"
    ):
        post_checker(active_instaloader, post, f"{public_profile.username}-tagged")


@paged_requirement(
    "profile-reels-first-page",
    "profile-reels-further-pages",
)
def test_profile_reels_paged_download(
    paginate: Pager,
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in paginate(
        public_profile.get_reels(), f"profile {public_profile.username!r}"
    ):
        post_checker(active_instaloader, post, f"{public_profile.username}-reels")


@paged_requirement(
    "profile-igtv-first-page",
    "profile-igtv-further-pages",
)
def test_profile_igtv_paged_download(
    paginate: Pager,
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in paginate(
        public_profile.get_igtv_posts(), f"profile {public_profile.username!r}"
    ):
        post_checker(active_instaloader, post, f"{public_profile.username}-igtv")


@paged_requirement(
    "profile-stories-first-page-logged-in",
    "profile-stories-further-pages-logged-in",
)
def test_profile_stories_paged_download(
    paginate: Pager,
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    output_dir: Path,
) -> None:
    stories = list(
        itertools.islice(active_instaloader.get_stories([public_profile.userid]), 1)
    )
    if not stories:
        pytest.skip(f"profile {public_profile.username!r} has no visible stories")
    for story_item in paginate(
        stories[0].get_items(), f"stories of profile {public_profile.username!r}"
    ):
        active_instaloader.download_storyitem(
            story_item, f"{public_profile.username}-stories"
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


@paged_requirement(
    "profile-highlights-first-page-logged-in",
    "profile-highlights-further-pages-logged-in",
)
def test_profile_highlights_paged_download(
    paginate: Pager,
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    output_dir: Path,
) -> None:
    for highlight in paginate(
        active_instaloader.get_highlights(public_profile),
        f"highlights of profile {public_profile.username!r}",
    ):
        first_item = next(iter(highlight.get_items()), None)
        if first_item is not None:
            active_instaloader.download_storyitem(
                first_item, f"{public_profile.username}-{highlight.title}"
            )


@paged_requirement(
    "profile-followers-first-page-logged-in",
    "profile-followers-further-pages-logged-in",
)
def test_profile_followers_paged_listable(
    paginate: Pager,
    public_profile: instaloader.Profile,
) -> None:
    for follower in paginate(
        public_profile.get_followers(),
        f"followers of profile {public_profile.username!r}",
    ):
        assert follower.username


@paged_requirement(
    "profile-followees-first-page-logged-in",
    "profile-followees-further-pages-logged-in",
)
def test_profile_followees_paged_listable(
    paginate: Pager,
    public_profile: instaloader.Profile,
) -> None:
    for followee in paginate(
        public_profile.get_followees(),
        f"followees of profile {public_profile.username!r}",
    ):
        assert followee.username
