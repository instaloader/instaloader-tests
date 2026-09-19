from __future__ import annotations

from pathlib import Path

import instaloader
import pytest

from tests.support.requirements_map import requirement
from tests.support.targets import (
    FIRST_50_ITEM_COUNT,
    FIRST_PAGE_ITEM_COUNT,
    IntegrationTargets,
    require_target,
    take_first_items,
    take_up_to_items,
)


def _require_location_id(integration_targets: IntegrationTargets) -> int:
    location = require_target(
        integration_targets.location, option_name="--target-location"
    )
    try:
        return int(location)
    except ValueError as error:
        raise pytest.UsageError(
            "--target-location must be an Instagram location ID"
        ) from error


@requirement("location-posts-first-page-logged-in-medium")
def test_location_first_page_posts_download(
    logged_in_instaloader: instaloader.Instaloader,
    integration_targets: IntegrationTargets,
    output_dir: Path,
) -> None:
    location = _require_location_id(integration_targets)
    take_first_items(
        logged_in_instaloader.get_location_posts(location),
        count=FIRST_PAGE_ITEM_COUNT,
        description=f"location {location!r}",
    )
    logged_in_instaloader.download_location(location, max_count=FIRST_PAGE_ITEM_COUNT)


@requirement("location-posts-first-50-logged-in-low")
def test_location_first_50_posts_download(
    logged_in_instaloader: instaloader.Instaloader,
    integration_targets: IntegrationTargets,
    output_dir: Path,
) -> None:
    location = _require_location_id(integration_targets)
    take_up_to_items(
        logged_in_instaloader.get_location_posts(location),
        minimum_count=FIRST_PAGE_ITEM_COUNT + 1,
        maximum_count=FIRST_50_ITEM_COUNT,
        description=f"location {location!r}",
    )
    logged_in_instaloader.download_location(location, max_count=FIRST_50_ITEM_COUNT)
