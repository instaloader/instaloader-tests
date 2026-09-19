import itertools
from pathlib import Path

import instaloader
import pytest

from tests.support.requirements_map import Authentication, requirement
from tests.support.targets import IntegrationTargets, require_target


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
    username = require_target(
        integration_targets.public_profile, option_name="--target-public-profile"
    )
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
        require_target(
            integration_targets.private_profile, option_name="--target-private-profile"
        ),
        profile_cache,
    )


@requirement("profile-picture-anonymous-critical")
def test_public_profile_picture_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    output_dir: Path,
) -> None:
    active_instaloader.download_profilepic(public_profile)


@requirement("profile-posts-first-page-anonymous-critical")
def test_public_profile_first_page_posts_download(
    active_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    output_dir: Path,
) -> None:
    for post in itertools.islice(public_profile.get_posts(), 12):
        active_instaloader.download_post(post, target=public_profile.username)


@requirement("profile-picture-private-logged-in-critical")
def test_private_profile_picture_download(
    active_instaloader: instaloader.Instaloader,
    private_profile: instaloader.Profile,
    output_dir: Path,
) -> None:
    active_instaloader.download_profilepic(private_profile)


@requirement("profile-posts-first-page-private-logged-in-critical")
def test_private_profile_first_page_posts_download(
    active_instaloader: instaloader.Instaloader,
    private_profile: instaloader.Profile,
    output_dir: Path,
) -> None:
    for post in itertools.islice(private_profile.get_posts(), 12):
        active_instaloader.download_post(post, target=private_profile.username)
