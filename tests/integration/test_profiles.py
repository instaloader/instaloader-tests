from pathlib import Path

import instaloader
import pytest

from tests.support.targets import IntegrationTargets, require_target, take_first_items
from tests.support.requirements_map import requirement


@pytest.fixture(scope="session")
def public_profile_cache() -> dict[tuple[str, str], instaloader.Profile]:
    return {}


@pytest.fixture()
def public_profile(
    active_authentication: str,
    active_instaloader: instaloader.Instaloader,
    integration_targets: IntegrationTargets,
    public_profile_cache: dict[tuple[str, str], instaloader.Profile],
) -> instaloader.Profile:
    username = require_target(
        integration_targets.public_profile, option_name="--target-public-profile"
    )
    cache_key = (active_authentication, username)
    if cache_key not in public_profile_cache:
        public_profile_cache[cache_key] = instaloader.Profile.from_username(
            active_instaloader.context, username
        )
    return public_profile_cache[cache_key]


@pytest.fixture(scope="session")
def public_profile_first_page_posts_cache() -> (
    dict[tuple[str, str], tuple[instaloader.Post, ...]]
):
    return {}


@pytest.fixture()
def public_profile_first_page_posts(
    public_profile: instaloader.Profile,
    active_authentication: str,
    public_profile_first_page_posts_cache: dict[
        tuple[str, str], tuple[instaloader.Post, ...]
    ],
) -> tuple[instaloader.Post, ...]:
    cache_key = (active_authentication, public_profile.username)
    if cache_key not in public_profile_first_page_posts_cache:
        public_profile_first_page_posts_cache[cache_key] = tuple(
            take_first_items(
                public_profile.get_posts(),
                count=12,
                description=f"public profile {public_profile.username!r}",
            )
        )
    return public_profile_first_page_posts_cache[cache_key]


@requirement("profile-picture-anonymous-critical")
def test_public_profile_picture_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    _output_dir: Path,
) -> None:
    active_instaloader.download_profilepic(public_profile)


@requirement("profile-posts-first-page-anonymous-critical")
def test_public_profile_first_page_posts_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    public_profile_first_page_posts: tuple[instaloader.Post, ...],
    _output_dir: Path,
) -> None:
    for post in public_profile_first_page_posts:
        active_instaloader.download_post(post, target=public_profile.username)
