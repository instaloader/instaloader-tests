import itertools
from pathlib import Path

import instaloader
import pytest

from tests.support.targets import IntegrationTargets, require_target
from tests.support.requirements_map import requirement


@pytest.fixture(scope="session")
def profile_cache() -> dict[tuple[str, str], instaloader.Profile]:
    return {}


def _profile_from_username(
    context: instaloader.InstaloaderContext,
    authentication: str,
    username: str,
    profile_cache: dict[tuple[str, str], instaloader.Profile],
) -> instaloader.Profile:
    cache_key = (authentication, username)
    if cache_key not in profile_cache:
        profile_cache[cache_key] = instaloader.Profile.from_username(context, username)
    return profile_cache[cache_key]


@pytest.fixture()
def public_profile(
    active_authentication: str,
    active_instaloader: instaloader.Instaloader,
    integration_targets: IntegrationTargets,
    profile_cache: dict[tuple[str, str], instaloader.Profile],
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
def logged_in_private_profile(
    request: pytest.FixtureRequest,
    integration_targets: IntegrationTargets,
    profile_cache: dict[tuple[str, str], instaloader.Profile],
) -> tuple[instaloader.Instaloader, instaloader.Profile]:
    username = require_target(
        integration_targets.private_profile, option_name="--target-private-profile"
    )
    logged_in_instaloader = request.getfixturevalue("logged_in_instaloader")
    return logged_in_instaloader, _profile_from_username(
        logged_in_instaloader.context,
        "logged_in",
        username,
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


@pytest.mark.integration
@pytest.mark.logged_in
@pytest.mark.importance("critical")
def test_private_profile_picture_download(
    logged_in_private_profile: tuple[instaloader.Instaloader, instaloader.Profile],
    output_dir: Path,
) -> None:
    logged_in_instaloader, private_profile = logged_in_private_profile
    logged_in_instaloader.download_profilepic(private_profile)


@pytest.mark.integration
@pytest.mark.logged_in
@pytest.mark.importance("critical")
def test_private_profile_first_page_posts_download(
    logged_in_private_profile: tuple[instaloader.Instaloader, instaloader.Profile],
    output_dir: Path,
) -> None:
    logged_in_instaloader, private_profile = logged_in_private_profile
    for post in itertools.islice(private_profile.get_posts(), 12):
        logged_in_instaloader.download_post(post, target=private_profile.username)
