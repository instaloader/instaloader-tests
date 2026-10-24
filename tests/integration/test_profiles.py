import itertools
from pathlib import Path

import instaloader
import pytest
from instaloader.exceptions import PrivateProfileNotFollowedException

from tests.support.post_checkers import PostChecker
from tests.support.pagination import first_page, further_pages
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


@pytest.fixture()
def public_profile_from_id(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
) -> instaloader.Profile:
    active_instaloader.context.profile_id_cache.pop(public_profile.userid, None)
    return instaloader.Profile.from_id(
        active_instaloader.context, public_profile.userid
    )


@requirement("profile-from-id-public")
def test_public_profile_from_id(
    public_profile: instaloader.Profile,
    public_profile_from_id: instaloader.Profile,
) -> None:
    assert public_profile_from_id.userid == public_profile.userid
    assert public_profile_from_id.username == public_profile.username


@requirement("profile-from-id-private-logged-in")
def test_private_profile_from_id(
    active_instaloader: instaloader.Instaloader,
    private_profile: instaloader.Profile,
) -> None:
    active_instaloader.context.profile_id_cache.pop(private_profile.userid, None)
    resolved_profile = instaloader.Profile.from_id(
        active_instaloader.context, private_profile.userid
    )
    assert resolved_profile.userid == private_profile.userid
    assert resolved_profile.username == private_profile.username


@requirement("profile-picture-public")
def test_public_profile_from_id_picture_download(
    active_instaloader: instaloader.Instaloader,
    public_profile_from_id: instaloader.Profile,
    output_dir: Path,
) -> None:
    active_instaloader.download_profilepic(public_profile_from_id)


@requirement("profile-posts-first-page-public")
def test_public_profile_from_id_first_page_posts_download(
    active_instaloader: instaloader.Instaloader,
    public_profile_from_id: instaloader.Profile,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in first_page(
        public_profile_from_id.get_posts(),
        f"profile {public_profile_from_id.username!r}",
        expected_count=public_profile_from_id.mediacount,
    ):
        post_checker(active_instaloader, post, public_profile_from_id.username)


@requirement("profile-picture-public")
def test_public_profile_picture_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    output_dir: Path,
) -> None:
    active_instaloader.download_profilepic(public_profile)


@requirement("profile-posts-first-page-public")
def test_public_profile_first_page_posts_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in first_page(
        public_profile.get_posts(),
        f"profile {public_profile.username!r}",
        expected_count=public_profile.mediacount,
    ):
        post_checker(active_instaloader, post, public_profile.username)


@requirement("profile-posts-further-pages")
def test_public_profile_further_pages_posts_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    max_items: int,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in further_pages(
        public_profile.get_posts(),
        max_items,
        f"profile {public_profile.username!r}",
        expected_count=public_profile.mediacount,
    ):
        post_checker(active_instaloader, post, public_profile.username)


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
    try:
        for post in first_page(
            private_profile.get_posts(),
            f"profile {private_profile.username!r}",
            expected_count=private_profile.mediacount,
        ):
            post_checker(active_instaloader, post, private_profile.username)
    except PrivateProfileNotFollowedException as error:
        pytest.skip(str(error))


@requirement("profile-posts-further-pages-private-logged-in")
def test_private_profile_further_pages_posts_download(
    active_instaloader: instaloader.Instaloader,
    private_profile: instaloader.Profile,
    max_items: int,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    try:
        for post in further_pages(
            private_profile.get_posts(),
            max_items,
            f"private profile {private_profile.username!r}",
            expected_count=private_profile.mediacount,
        ):
            post_checker(active_instaloader, post, private_profile.username)
    except PrivateProfileNotFollowedException as error:
        pytest.skip(str(error))


@requirement("profile-tagged-posts-first-page")
def test_profile_tagged_posts_first_page_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in first_page(
        public_profile.get_tagged_posts(), f"profile {public_profile.username!r}"
    ):
        post_checker(active_instaloader, post, f"{public_profile.username}-tagged")


@requirement("profile-tagged-posts-further-pages")
def test_profile_tagged_posts_further_pages_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    max_items: int,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in further_pages(
        public_profile.get_tagged_posts(),
        max_items,
        f"tagged posts of profile {public_profile.username!r}",
    ):
        post_checker(active_instaloader, post, f"{public_profile.username}-tagged")


@requirement("profile-reels-first-page")
def test_profile_reels_first_page_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in first_page(
        public_profile.get_reels(), f"profile {public_profile.username!r}"
    ):
        post_checker(active_instaloader, post, f"{public_profile.username}-reels")


@requirement("profile-reels-further-pages")
def test_profile_reels_further_pages_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    max_items: int,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in further_pages(
        public_profile.get_reels(),
        max_items,
        f"reels of profile {public_profile.username!r}",
    ):
        post_checker(active_instaloader, post, f"{public_profile.username}-reels")


@requirement("profile-igtv-first-page")
def test_profile_igtv_first_page_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in first_page(
        public_profile.get_igtv_posts(),
        f"profile {public_profile.username!r}",
        expected_count=public_profile.igtvcount,
    ):
        post_checker(active_instaloader, post, f"{public_profile.username}-igtv")


@requirement("profile-igtv-further-pages")
def test_profile_igtv_further_pages_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    max_items: int,
    output_dir: Path,
    post_checker: PostChecker,
) -> None:
    for post in further_pages(
        public_profile.get_igtv_posts(),
        max_items,
        f"IGTV posts of profile {public_profile.username!r}",
        expected_count=public_profile.igtvcount,
    ):
        post_checker(active_instaloader, post, f"{public_profile.username}-igtv")


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
    for story_item in first_page(
        stories[0].get_items(),
        f"stories of profile {public_profile.username!r}",
        expected_count=stories[0].itemcount,
    ):
        active_instaloader.download_storyitem(
            story_item, f"{public_profile.username}-stories"
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
    for story_item in further_pages(
        stories[0].get_items(),
        max_items,
        f"stories of profile {public_profile.username!r}",
        expected_count=stories[0].itemcount,
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


@requirement("profile-highlights-first-page-logged-in")
def test_profile_highlights_first_page_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    output_dir: Path,
) -> None:
    for highlight in first_page(
        active_instaloader.get_highlights(public_profile),
        f"highlights of profile {public_profile.username!r}",
    ):
        first_item = next(iter(highlight.get_items()), None)
        if first_item is not None:
            active_instaloader.download_storyitem(
                first_item, f"{public_profile.username}-{highlight.title}"
            )


@requirement("profile-highlights-further-pages-logged-in")
def test_profile_highlights_further_pages_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    max_items: int,
    output_dir: Path,
) -> None:
    for highlight in further_pages(
        active_instaloader.get_highlights(public_profile),
        max_items,
        f"highlights of profile {public_profile.username!r}",
    ):
        first_item = next(iter(highlight.get_items()), None)
        if first_item is not None:
            active_instaloader.download_storyitem(
                first_item, f"{public_profile.username}-{highlight.title}"
            )


@requirement("profile-followers-first-page-logged-in")
def test_profile_followers_first_page_listable(
    public_profile: instaloader.Profile,
) -> None:
    for follower in first_page(
        public_profile.get_followers(),
        f"followers of profile {public_profile.username!r}",
        expected_count=public_profile.followers,
    ):
        assert follower.username


@requirement("profile-followers-further-pages-logged-in")
def test_profile_followers_further_pages_listable(
    public_profile: instaloader.Profile,
    max_items: int,
) -> None:
    for follower in further_pages(
        public_profile.get_followers(),
        max_items,
        f"followers of profile {public_profile.username!r}",
        expected_count=public_profile.followers,
    ):
        assert follower.username


@requirement("profile-followees-first-page-logged-in")
def test_profile_followees_first_page_listable(
    public_profile: instaloader.Profile,
) -> None:
    for followee in first_page(
        public_profile.get_followees(),
        f"followees of profile {public_profile.username!r}",
        expected_count=public_profile.followees,
    ):
        assert followee.username


@requirement("profile-followees-further-pages-logged-in")
def test_profile_followees_further_pages_listable(
    public_profile: instaloader.Profile,
    max_items: int,
) -> None:
    for followee in further_pages(
        public_profile.get_followees(),
        max_items,
        f"followees of profile {public_profile.username!r}",
        expected_count=public_profile.followees,
    ):
        assert followee.username
