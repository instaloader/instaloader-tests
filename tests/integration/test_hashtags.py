from __future__ import annotations

from pathlib import Path

import instaloader

from tests.support.requirements_map import requirement
from tests.support.targets import (
    FIRST_50_ITEM_COUNT,
    FIRST_PAGE_ITEM_COUNT,
    IntegrationTargets,
    require_target,
    take_first_items,
    take_up_to_items,
)


def _hashtag_from_name(
    loader: instaloader.Instaloader, hashtag_name: str
) -> instaloader.Hashtag:
    return instaloader.Hashtag.from_name(loader.context, hashtag_name)


@requirement("hashtag-posts-first-page-anonymous-high")
def test_hashtag_first_page_posts_download_anonymous(
    anonymous_instaloader: instaloader.Instaloader,
    integration_targets: IntegrationTargets,
    _output_dir: Path,
) -> None:
    hashtag_name = require_target(
        integration_targets.public_hashtag, option_name="--target-public-hashtag"
    )
    hashtag = _hashtag_from_name(anonymous_instaloader, hashtag_name)
    take_first_items(
        hashtag.get_all_posts(),
        count=FIRST_PAGE_ITEM_COUNT,
        description=f"hashtag {hashtag_name!r}",
    )
    anonymous_instaloader.download_hashtag(
        hashtag_name, max_count=FIRST_PAGE_ITEM_COUNT, profile_pic=False
    )


@requirement("hashtag-posts-first-50-anonymous-medium")
def test_hashtag_first_50_posts_download_anonymous(
    anonymous_instaloader: instaloader.Instaloader,
    integration_targets: IntegrationTargets,
    _output_dir: Path,
) -> None:
    hashtag_name = require_target(
        integration_targets.public_hashtag, option_name="--target-public-hashtag"
    )
    hashtag = _hashtag_from_name(anonymous_instaloader, hashtag_name)
    take_up_to_items(
        hashtag.get_all_posts(),
        minimum_count=FIRST_PAGE_ITEM_COUNT + 1,
        maximum_count=FIRST_50_ITEM_COUNT,
        description=f"hashtag {hashtag_name!r}",
    )
    anonymous_instaloader.download_hashtag(
        hashtag_name, max_count=FIRST_50_ITEM_COUNT, profile_pic=False
    )


@requirement("hashtag-posts-first-page-logged-in-critical")
def test_hashtag_first_page_posts_download_logged_in(
    logged_in_instaloader: instaloader.Instaloader,
    integration_targets: IntegrationTargets,
    _output_dir: Path,
) -> None:
    hashtag_name = require_target(
        integration_targets.public_hashtag, option_name="--target-public-hashtag"
    )
    hashtag = _hashtag_from_name(logged_in_instaloader, hashtag_name)
    take_first_items(
        hashtag.get_all_posts(),
        count=FIRST_PAGE_ITEM_COUNT,
        description=f"hashtag {hashtag_name!r}",
    )
    logged_in_instaloader.download_hashtag(
        hashtag_name, max_count=FIRST_PAGE_ITEM_COUNT, profile_pic=False
    )


@requirement("hashtag-posts-first-50-logged-in-critical")
def test_hashtag_first_50_posts_download_logged_in(
    logged_in_instaloader: instaloader.Instaloader,
    integration_targets: IntegrationTargets,
    _output_dir: Path,
) -> None:
    hashtag_name = require_target(
        integration_targets.public_hashtag, option_name="--target-public-hashtag"
    )
    hashtag = _hashtag_from_name(logged_in_instaloader, hashtag_name)
    take_up_to_items(
        hashtag.get_all_posts(),
        minimum_count=FIRST_PAGE_ITEM_COUNT + 1,
        maximum_count=FIRST_50_ITEM_COUNT,
        description=f"hashtag {hashtag_name!r}",
    )
    logged_in_instaloader.download_hashtag(
        hashtag_name, max_count=FIRST_50_ITEM_COUNT, profile_pic=False
    )
