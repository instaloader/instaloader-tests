from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterable
import os

import pytest


ENV_PUBLIC_PROFILE = "INSTALOADER_PUBLIC_PROFILE"
ENV_PUBLIC_SHORTCODE = "INSTALOADER_PUBLIC_SHORTCODE"
ENV_PUBLIC_HASHTAG = "INSTALOADER_PUBLIC_HASHTAG"


@dataclass(frozen=True)
class IntegrationTargets:
    public_profile: str | None = None
    public_shortcode: str | None = None
    public_hashtag: str | None = None



def load_targets(*, public_profile: str | None, public_shortcode: str | None, public_hashtag: str | None) -> IntegrationTargets:
    return IntegrationTargets(
        public_profile=public_profile or os.getenv(ENV_PUBLIC_PROFILE),
        public_shortcode=public_shortcode or os.getenv(ENV_PUBLIC_SHORTCODE),
        public_hashtag=public_hashtag or os.getenv(ENV_PUBLIC_HASHTAG),
    )


def require_target(value: str | None, *, option_name: str) -> str:
    if value:
        return value
    pytest.skip(f"configure {option_name} or the matching INSTALOADER_* environment variable")


def take_first_items(items: Iterable[object], *, count: int, description: str) -> list[object]:
    selected: list[object] = []
    for item in items:
        selected.append(item)
        if len(selected) == count:
            return selected
    pytest.skip(f"configured target does not provide {count} items for {description}")
