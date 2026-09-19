from dataclasses import dataclass

import pytest


@dataclass(frozen=True)
class IntegrationTargets:
    public_profile: str | None = None
    private_profile: str | None = None
    public_shortcode: str | None = None
    public_hashtag: str | None = None


def load_targets(
    *,
    public_profile: str | None,
    private_profile: str | None,
    public_shortcode: str | None,
    public_hashtag: str | None,
) -> IntegrationTargets:
    return IntegrationTargets(
        public_profile=public_profile,
        private_profile=private_profile,
        public_shortcode=public_shortcode,
        public_hashtag=public_hashtag,
    )


def require_target(value: str | None, *, option_name: str) -> str:
    if value:
        return value
    pytest.skip(f"configure {option_name}")
