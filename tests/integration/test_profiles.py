from __future__ import annotations

from pathlib import Path

import instaloader
import pytest

from tests.support.targets import IntegrationTargets, require_target, take_first_items
from tests.support.requirements_map import requirement


@pytest.fixture(scope="module")
def public_profile(
    anonymous_instaloader: instaloader.Instaloader,
    integration_targets: IntegrationTargets,
) -> instaloader.Profile:
    username = require_target(
        integration_targets.public_profile, option_name="--target-public-profile"
    )
    return instaloader.Profile.from_username(anonymous_instaloader.context, username)


@pytest.fixture(scope="module")
def public_profile_first_page_posts(
    public_profile: instaloader.Profile,
) -> tuple[instaloader.Post, ...]:
    return tuple(
        take_first_items(
            public_profile.get_posts(),
            count=12,
            description=f"public profile {public_profile.username!r}",
        )
    )


@requirement("profile-picture-anonymous-critical")
def test_public_profile_picture_download(
    anonymous_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    _output_dir: Path,
) -> None:
    anonymous_instaloader.download_profilepic(public_profile)


@requirement("profile-posts-first-page-anonymous-critical")
def test_public_profile_first_page_posts_download(
    anonymous_instaloader: instaloader.Instaloader,
    public_profile: instaloader.Profile,
    public_profile_first_page_posts: tuple[instaloader.Post, ...],
    _output_dir: Path,
) -> None:
    for post in public_profile_first_page_posts:
        anonymous_instaloader.download_post(post, target=public_profile.username)
