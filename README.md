# instaloader-tests

Integration tests for Instaloader features that require Instagram access.

This repository aims to provide mostly automated regression tests for Instaloader's
integration behavior. The integration requirements are documented in
`instaloader-requirements.md` and focus only on Instagram-access-related behavior.

The test suite is intended to be user-friendly, modern Python style compliant
(typing, Black formatting), and practical without unnecessary over-engineering.
It is expected to support:

- execution up to a configurable importance level;
- parametrized test targets (e.g., public/private profiles, posts with comments);
- coverage of features regardless of how `Post` and `Profile` instances are created.
