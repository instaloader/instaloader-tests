# Instaloader Integration Requirements

## Scope

This document specifies the Instagram-access-related behaviors that the integration
suite shall cover. It excludes purely local concerns such as formatting, CLI text,
and filesystem details unless they are directly required to authenticate against
Instagram or to fetch Instagram data.

## Conventions

- Each requirement describes one externally observable behavior and uses *shall* wording.
- Importance expresses how valuable a regression test is for routine execution.
- Allowed importance values are **critical**, **high**, **medium**, **low**, and **very low**.
- Access modes:
  - **anonymous**: no authenticated Instagram session is available;
  - **bootstrap**: credentials or browser cookies are available to establish an Instagram session;
  - **authenticated**: a valid Instagram session is available;
  - **owner**: the authenticated session belongs to the account whose own data is accessed.
- Quantitative scopes:
  - **first 12 items** applies when the target provides at least 12 items of the relevant surface type;
  - **first 50 items** applies only when the target provides at least 50 items.
- Additional coverage values:
  - **single item** means one directly addressed object is fetched successfully;
  - **media set** means all media items belonging to one addressed post are fetched successfully;
  - **update run** means a repeated download run is executed against an already-downloaded target and validates the expected incremental behavior.
- Logged-in profile download requirements shall be exercised against both a public profile
  and, where Instagram permissions allow it, a followed private profile.

## Shared Fixture Expectations

The integration suite shall maintain reusable targets for at least the following cases:

- a public profile with at least 50 posts;
- a followed private profile with at least 50 posts;
- a Firefox browser profile with valid Instagram cookies;
- another supported browser profile with valid Instagram cookies;
- a login target account without two-factor authentication;
- a login target account with two-factor authentication enabled;
- a profile with at least 50 story items and at least 50 highlights;
- a profile with at least 50 tagged posts, 50 reels, and 50 IGTV items;
- a profile with at least 50 followers and at least 50 followees, and with those relationships visible to the authenticated session;
- a profile fixture whose username can be changed between two download runs while preserving the same Instagram identity;
- a hashtag with at least 50 posts;
- a location with at least 50 posts;
- a reusable public post fixture that is accessible in both anonymous and authenticated runs and exposes caption and date;
- a reusable public post fixture that is accessible in both anonymous and authenticated runs, exposes a comment list with at least 50 entries, and preserves stable comment ordering and pagination across repeated runs;
- a reusable authenticated post fixture that exposes a geotag;
- a reusable authenticated post fixture that exposes a liker list with at least 50 entries;
- a shortcode for a downloadable post with one or more media items;
- an owner account with at least 50 saved posts, 50 feed items, and 50 visible story items.

## Session Management Requirements

| ID | Importance | Access | Requirement |
|----|------------|--------|-------------|
| SM-1 | critical | bootstrap | Instaloader shall be able to create a reusable session by importing cookies from Firefox with `instaloader --load-cookies firefox`. |
| SM-2 | high | bootstrap | Instaloader shall be able to create a reusable session by importing cookies from another supported browser with `instaloader --load-cookies BROWSER`. |
| SM-3 | high | bootstrap | Instaloader shall be able to create a reusable session with `Instaloader.interactive_login()` when two-factor authentication is not required. |
| SM-4 | medium | bootstrap | Instaloader shall be able to create a reusable session with `Instaloader.interactive_login()` when two-factor authentication is required. |
| SM-5 | high | authenticated | Instaloader shall be able to save a created session with `Instaloader.save_session_to_file()` and reload it with `Instaloader.load_session_from_file()`. |
| SM-6 | critical | authenticated | Instaloader shall be able to reuse an existing valid session for a non-interactive authenticated download run. |

## Download Requirements

### Profiles

Authenticated tagged-post, reel, and IGTV requirements shall be exercised
against both public profiles and, where Instagram permissions allow it,
followed private profiles.

| ID | Importance | Access | Coverage | Requirement |
|----|------------|--------|----------|-------------|
| DL-PROFILE-1 | critical | anonymous | single item | Instaloader shall be able to download the profile picture of a profile. |
| DL-PROFILE-1A | critical | authenticated | single item | Instaloader shall be able to download the profile picture of a profile. |
| DL-PROFILE-2 | critical | authenticated | first 12 items | Instaloader shall be able to download the first 12 posts of a profile. |
| DL-PROFILE-3 | high | anonymous | first 12 items | Instaloader shall be able to download the first 12 posts of a public profile. |
| DL-PROFILE-4 | critical | authenticated | first 50 items | Instaloader shall be able to download the first 50 posts of a profile. |
| DL-PROFILE-5 | medium | anonymous | first 50 items | Instaloader shall be able to download the first 50 posts of a public profile. |
| DL-PROFILE-6 | high | authenticated | first 12 items | Instaloader shall be able to download the first 12 story items of a profile. |
| DL-PROFILE-7 | medium | authenticated | first 50 items | Instaloader shall be able to download the first 50 story items of a profile. |
| DL-PROFILE-8 | high | authenticated | single item | Instaloader shall be able to download the cover picture of a profile highlight. |
| DL-PROFILE-9 | high | authenticated | first 12 items | Instaloader shall be able to download the first 12 highlights of a profile. |
| DL-PROFILE-10 | medium | authenticated | first 50 items | Instaloader shall be able to download the first 50 highlights of a profile. |
| DL-PROFILE-11 | medium | authenticated | first 12 items | Instaloader shall be able to download the first 12 posts in which a profile is tagged. |
| DL-PROFILE-12 | low | anonymous | first 12 items | Instaloader shall be able to download the first 12 posts in which a public profile is tagged. |
| DL-PROFILE-13 | low | authenticated | first 50 items | Instaloader shall be able to download the first 50 posts in which a profile is tagged. |
| DL-PROFILE-14 | very low | anonymous | first 50 items | Instaloader shall be able to download the first 50 posts in which a public profile is tagged. |
| DL-PROFILE-15 | medium | authenticated | first 12 items | Instaloader shall be able to download the first 12 reels of a profile. |
| DL-PROFILE-16 | low | anonymous | first 12 items | Instaloader shall be able to download the first 12 reels of a public profile. |
| DL-PROFILE-17 | low | authenticated | first 50 items | Instaloader shall be able to download the first 50 reels of a profile. |
| DL-PROFILE-18 | very low | anonymous | first 50 items | Instaloader shall be able to download the first 50 reels of a public profile. |
| DL-PROFILE-19 | medium | authenticated | first 12 items | Instaloader shall be able to download the first 12 IGTV videos of a profile. |
| DL-PROFILE-20 | low | anonymous | first 12 items | Instaloader shall be able to download the first 12 IGTV videos of a public profile. |
| DL-PROFILE-21 | low | authenticated | first 50 items | Instaloader shall be able to download the first 50 IGTV videos of a profile. |
| DL-PROFILE-22 | very low | anonymous | first 50 items | Instaloader shall be able to download the first 50 IGTV videos of a public profile. |
| DL-PROFILE-23 | medium | authenticated | update run | Instaloader shall detect a profile username change during a subsequent download run, continue the download into the target named after the new username, and avoid writing newly downloaded data into the target named after the old username. |

### Hashtags

| ID | Importance | Access | Coverage | Requirement |
|----|------------|--------|----------|-------------|
| DL-HASHTAG-1 | high | authenticated | single item | Instaloader shall be able to download the profile picture of a hashtag in an authenticated run. |
| DL-HASHTAG-2 | medium | anonymous | single item | Instaloader shall be able to download the profile picture of a hashtag in an anonymous run. |
| DL-HASHTAG-3 | critical | authenticated | first 12 items | Instaloader shall be able to download the first 12 posts of a hashtag. |
| DL-HASHTAG-4 | high | anonymous | first 12 items | Instaloader shall be able to download the first 12 posts of a hashtag. |
| DL-HASHTAG-5 | critical | authenticated | first 50 items | Instaloader shall be able to download the first 50 posts of a hashtag. |
| DL-HASHTAG-6 | medium | anonymous | first 50 items | Instaloader shall be able to download the first 50 posts of a hashtag. |

### Locations

| ID | Importance | Access | Coverage | Requirement |
|----|------------|--------|----------|-------------|
| DL-LOCATION-1 | medium | authenticated | first 12 items | Instaloader shall be able to download the first 12 posts of a location. |
| DL-LOCATION-2 | low | authenticated | first 50 items | Instaloader shall be able to download the first 50 posts of a location. |

### Owner-only surfaces

| ID | Importance | Access | Coverage | Requirement |
|----|------------|--------|----------|-------------|
| DL-OWNER-1 | critical | owner | first 12 items | Instaloader shall be able to download the first 12 saved posts of the owner. |
| DL-OWNER-2 | critical | owner | first 50 items | Instaloader shall be able to download the first 50 saved posts of the owner. |
| DL-OWNER-3 | high | owner | first 12 items | Instaloader shall be able to download the first 12 feed posts of the owner. |
| DL-OWNER-4 | medium | owner | first 50 items | Instaloader shall be able to download the first 50 feed posts of the owner. |
| DL-OWNER-5 | high | owner | first 12 items | Instaloader shall be able to download the first 12 currently visible story items of the owner. |
| DL-OWNER-6 | medium | owner | first 50 items | Instaloader shall be able to download the first 50 currently visible story items of the owner. |

### Single-post targets

| ID | Importance | Access | Coverage | Requirement |
|----|------------|--------|----------|-------------|
| DL-POST-1 | critical | anonymous | single item | Instaloader shall be able to download a post specified by its shortcode. |
| DL-POST-2 | critical | authenticated | single item | Instaloader shall be able to download a post specified by its shortcode. |
| DL-POST-3 | high | authenticated | media set | Instaloader shall download all media items that belong to the addressed post, including sidecar items when present. |

## Metadata and Relationship Requirements

### Post metadata

| ID | Importance | Access | Coverage | Requirement |
|----|------------|--------|----------|-------------|
| MD-POST-1 | critical | anonymous | single item | Instaloader shall be able to access the caption and date of a post. |
| MD-POST-2 | critical | authenticated | single item | Instaloader shall be able to access the caption and date of a post. |
| MD-POST-3 | high | authenticated | first 12 items | Instaloader shall be able to list the first 12 profiles that liked a post. |
| MD-POST-4 | high | authenticated | first 50 items | Instaloader shall be able to list the first 50 profiles that liked a post. |
| MD-POST-5 | high | authenticated | first 12 items | Instaloader shall be able to retrieve the first 12 comments of a post in Instagram-provided order. |
| MD-POST-6 | medium | anonymous | first 12 items | Instaloader shall be able to retrieve the first 12 comments of a public post in Instagram-provided order. |
| MD-POST-7 | medium | authenticated | first 50 items | Instaloader shall be able to retrieve the first 50 comments of a post without gaps or duplicates across pagination. |
| MD-POST-8 | low | anonymous | first 50 items | Instaloader shall be able to retrieve the first 50 comments of a public post without gaps or duplicates across pagination. |
| MD-POST-9 | low | authenticated | single item | Instaloader shall be able to access the geotag of a post. |

### Profile relationships

| ID | Importance | Access | Coverage | Requirement |
|----|------------|--------|----------|-------------|
| MD-PROFILE-1 | high | authenticated | first 12 items | Instaloader shall be able to list the first 12 followers of a profile that the authenticated session is permitted to inspect. |
| MD-PROFILE-2 | medium | authenticated | first 50 items | Instaloader shall be able to list the first 50 followers of a profile that the authenticated session is permitted to inspect. |
| MD-PROFILE-3 | high | authenticated | first 12 items | Instaloader shall be able to list the first 12 followees of a profile that the authenticated session is permitted to inspect. |
| MD-PROFILE-4 | medium | authenticated | first 50 items | Instaloader shall be able to list the first 50 followees of a profile that the authenticated session is permitted to inspect. |
