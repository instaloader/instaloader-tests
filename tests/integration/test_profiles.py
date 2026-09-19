from pathlib import Path

import instaloader
import pytest

from tests.support.targets import IntegrationTargets, require_target, take_first_items
from tests.support.requirements_map import requirement


@pytest.fixture(scope="session")
def public_profile_username(integration_targets: IntegrationTargets) -> str:
    return require_target(
        integration_targets.public_profile, option_name="--target-public-profile"
    )


@pytest.fixture(scope="session")
def public_profile_anonymous(
    anonymous_instaloader: instaloader.Instaloader, public_profile_username: str
) -> instaloader.Profile:
    return instaloader.Profile.from_username(
        anonymous_instaloader.context, public_profile_username
    )


@pytest.fixture(scope="session")
def public_profile_logged_in(
    logged_in_instaloader: instaloader.Instaloader, public_profile_username: str
) -> instaloader.Profile:
    return instaloader.Profile.from_username(
        logged_in_instaloader.context, public_profile_username
    )


@pytest.fixture()
def public_profile(
    active_authentication: str,
    public_profile_anonymous: instaloader.Profile,
    public_profile_logged_in: instaloader.Profile,
) -> instaloader.Profile:
    if active_authentication == "anonymous":
        return public_profile_anonymous
    if active_authentication == "logged_in":
        return public_profile_logged_in
    raise pytest.UsageError(f"Unknown authentication variant: {active_authentication}")


@pytest.fixture(scope="session")
def public_profile_first_page_posts_anonymous(
    public_profile_anonymous: instaloader.Profile,
) -> tuple[instaloader.Post, ...]:
    return tuple(
        take_first_items(
            public_profile_anonymous.get_posts(),
            count=12,
            description=f"public profile {public_profile_anonymous.username!r}",
        )
    )


@pytest.fixture(scope="session")
def public_profile_first_page_posts_logged_in(
    public_profile_logged_in: instaloader.Profile,
) -> tuple[instaloader.Post, ...]:
    return tuple(
        take_first_items(
            public_profile_logged_in.get_posts(),
            count=12,
            description=f"public profile {public_profile_logged_in.username!r}",
        )
    )


@pytest.fixture()
def public_profile_first_page_posts(
    active_authentication: str,
    public_profile_first_page_posts_anonymous: tuple[instaloader.Post, ...],
    public_profile_first_page_posts_logged_in: tuple[instaloader.Post, ...],
) -> tuple[instaloader.Post, ...]:
    if active_authentication == "anonymous":
        return public_profile_first_page_posts_anonymous
    if active_authentication == "logged_in":
        return public_profile_first_page_posts_logged_in
    raise pytest.UsageError(f"Unknown authentication variant: {active_authentication}")


@pytest.fixture(scope="session")
def private_profile(
    integration_targets: IntegrationTargets,
    logged_in_instaloader: instaloader.Instaloader,
) -> instaloader.Profile:
    username = require_target(
        integration_targets.private_profile, option_name="--target-private-profile"
    )
    return instaloader.Profile.from_username(logged_in_instaloader.context, username)


@pytest.fixture(scope="session")
def private_profile_first_page_posts(
    private_profile: instaloader.Profile,
) -> tuple[instaloader.Post, ...]:
    return tuple(
        take_first_items(
            private_profile.get_posts(),
            count=12,
            description=f"private profile {private_profile.username!r}",
        )
    )


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


@requirement("profile-picture-private-logged-in-critical")
def test_private_profile_picture_download(
    logged_in_instaloader: instaloader.Instaloader,
    private_profile: instaloader.Profile,
    _output_dir: Path,
) -> None:
    logged_in_instaloader.download_profilepic(private_profile)


@requirement("profile-posts-first-page-private-logged-in-critical")
def test_private_profile_first_page_posts_download(
    logged_in_instaloader: instaloader.Instaloader,
    private_profile: instaloader.Profile,
    private_profile_first_page_posts: tuple[instaloader.Post, ...],
    _output_dir: Path,
) -> None:
    for post in private_profile_first_page_posts:
        logged_in_instaloader.download_post(post, target=private_profile.username)
