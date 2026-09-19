from __future__ import annotations

from pathlib import Path

import instaloader

from tests.support.requirements_map import requirement
from tests.support.targets import require_target, take_first_items


@requirement("profile-picture-anonymous-critical")
def test_public_profile_picture_download(
    anonymous_instaloader: instaloader.Instaloader,
    integration_targets,
    output_dir: Path,
) -> None:
    username = require_target(integration_targets.public_profile, option_name="--target-public-profile")

    profile = instaloader.Profile.from_username(anonymous_instaloader.context, username)
    anonymous_instaloader.download_profilepic(profile)

    downloaded_files = [path for path in output_dir.rglob("*.jpg") if path.is_file()]
    assert downloaded_files


@requirement("profile-posts-first-page-anonymous-critical")
def test_public_profile_first_page_posts_download(
    anonymous_instaloader: instaloader.Instaloader,
    integration_targets,
    output_dir: Path,
) -> None:
    username = require_target(integration_targets.public_profile, option_name="--target-public-profile")

    profile = instaloader.Profile.from_username(anonymous_instaloader.context, username)
    posts = take_first_items(profile.get_posts(), count=12, description=f"public profile {username!r}")

    for post in posts:
        anonymous_instaloader.download_post(post, target=username)
        assert list(output_dir.joinpath(username).glob(f"{post.shortcode}*"))
