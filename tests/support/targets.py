from dataclasses import dataclass
from typing import Literal

import pytest

TargetKey = Literal[
    "public_profile",
    "private_profile",
    "public_shortcode",
    "hashtag",
]


@dataclass(frozen=True)
class TargetOption:
    option_name: str
    help_text: str


TARGET_OPTIONS: dict[TargetKey, TargetOption] = {
    "public_profile": TargetOption(
        option_name="--target-public-profile",
        help_text="public profile username for profile tests",
    ),
    "private_profile": TargetOption(
        option_name="--target-private-profile",
        help_text="private profile username for logged-in profile tests",
    ),
    "public_shortcode": TargetOption(
        option_name="--target-public-shortcode",
        help_text="public shortcode for single-post tests",
    ),
    "hashtag": TargetOption(
        option_name="--target-hashtag",
        help_text="hashtag for hashtag tests",
    ),
}


def target_option(target_key: TargetKey) -> TargetOption:
    return TARGET_OPTIONS[target_key]


@dataclass(frozen=True)
class IntegrationTargets:
    public_profile: str | None = None
    private_profile: str | None = None
    public_shortcode: str | None = None
    hashtag: str | None = None

    def require(self, target_key: TargetKey) -> str:
        return require_target(getattr(self, target_key), target_key=target_key)


def load_targets(
    *,
    public_profile: str | None,
    private_profile: str | None,
    public_shortcode: str | None,
    hashtag: str | None,
) -> IntegrationTargets:
    return IntegrationTargets(
        public_profile=public_profile,
        private_profile=private_profile,
        public_shortcode=public_shortcode,
        hashtag=hashtag,
    )


def require_target(value: str | None, *, target_key: TargetKey) -> str:
    if value:
        return value
    pytest.skip(f"configure {target_option(target_key).option_name}")
