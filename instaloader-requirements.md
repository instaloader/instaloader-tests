# Instaloader Integration Requirements

## Conventions

This file shall only describe requirements that need Instagram access and can be verified by integration tests.

Requirements describe Instaloaders behavior with the modal verb *shall*.

## Session Creation

Instaloader shall be able to create a session by logging in or by importing cookies.

Instaloader shall be able to save a created session (`Instaloader.save_session_to_file()`) and reload the saved session 
(`Instaloader.load_session_from_file()`).

### Import session from Firefox

| Importance |
|------------|
| critical   |

Instaloader shall provide a single-command way to import cookies from Firefox.

### Import session from other browsers

| Importance |
|------------|
| high       |

Instaloader shall provide a single-command way to import cookies from browsers other than Firefox.

### Login

| Importance |
|------------|
| high       |

Instaloader shall be able to create a Session file with `Instaloader.interactive_login()` if no 2FA is configured.

### 2FA

| Importance |
|------------|
| medium     |

Instaloader shall be able to create a Session file with `Instaloader.interactive_login()` if 2FA is configured.

## Download Targets

### Profile

#### Profile Picture

| Importance | logged-in | anonymous |
|------------|-----------|-----------|
|            | critical  | critical  |

Instaloader shall be able to download the profile picture of a Profile.

#### Profile Posts

| Importance            | logged-in | anonymous |
|-----------------------|-----------|-----------|
| First page (12 Posts) | critical  | high      |
| First 50 Posts        | critical  | medium    |

Instaloader shall be able to download the Posts of a Profile.

#### Stories

| Importance                 | logged-in |
|----------------------------|-----------|
| First page (12 StoryItems) | high      |
| First 50 posts             | medium    |

Instaloader shall be able to download the Stories of a Profile (if logged-in).

#### Highlights

##### Cover Picture

| Importance |
|------------|
| high       |

Instaloader shall be able to download the cover picture of a Highlight (if logged-in).

##### Highlights

| Importance                 | logged-in |
|----------------------------|-----------|
| First page (12 Highlights) | high      |
| First 50 Highlights        | medium    |

Instaloader shall be able to download the Highlights of a Profile (if logged-in).

#### Tagged

| Importance            | logged-in | anonymous |
|-----------------------|-----------|-----------|
| First page (12 Posts) | medium    | low       |
| First 50 Posts        | low       | very low  |

Instaloader shall be able to download the Posts where the Profile is tagged.

#### Reels

| Importance            | logged-in | anonymous |
|-----------------------|-----------|-----------|
| First page (12 Posts) | medium    | low       |
| First 50 Posts        | low       | very low  |

Instaloader shall be able to download the Reels videos of a Profile.

#### IGTV

| Importance            | logged-in | anonymous |
|-----------------------|-----------|-----------|
| First page (12 Posts) | medium    | low       |
| First 50 Posts        | low       | very low  |

Instaloader shall be able to download the IGTV videos of a Profile.

### Hashtags

#### Hashtag Profile Picture

| Importance | logged-in | anonymous |
|------------|-----------|-----------|
|            | high      | medium    |

Instaloader shall be able to download the profile picture of a Hashtag.

#### Hashtag Posts

| Importance            | logged-in | anonymous |
|-----------------------|-----------|-----------|
| First page (12 Posts) | critical  | high      |
| First 50 Posts        | critical  | medium    |

Instaloader shall be able to download the Posts of a Hashtag.

### Locations

| Importance            | logged-in |
|-----------------------|-----------|
| First page (12 Posts) | medium    |
| First 50 Posts        | low       |

Instaloader shall be able to download the Posts of a Location (if logged-in).

### Saved Posts

| Importance            | logged-in |
|-----------------------|-----------|
| First page (12 Posts) | critical  |
| First 50 Posts        | critical  |

Instaloader shall be able to download the saved Posts of the logged-in user.

### Feed

| Importance            | logged-in |
|-----------------------|-----------|
| First page (12 Posts) | high      |
| First 50 Posts        | medium    |

Instaloader shall be able to download the Feed of the logged-in user.

### Stories

| Importance              | logged-in |
|-------------------------|-----------|
| First page (12 Stories) | high      |
| First 50 Stories        | medium    |

Instaloader shall be able to download the currently-visible Stories of the logged-in user.

### Single Post (shortcode)

| Importance | logged-in | anonymous |
|------------|-----------|-----------|
|            | critical  | critical  |

Instaloader shall be able to download a single Post specified by its shortcode.

## Post Metadata

### Basic Information

| Importance | logged-in | anonymous |
|------------|-----------|-----------|
|            | critical  | critical  |

Instaloader shall be able to access the Caption and Date of a Post.

### Likes

| Importance               | logged-in |
|--------------------------|-----------|
| First page (12 Profiles) | high      |
| First 50 Profiles        | high      |

Instaloader shall be able to list the Profiles that have liked a Post (if logged-in).

### Comments

| Importance               | logged-in | anonymous |
|--------------------------|-----------|-----------|
| First page (12 Profiles) | high      | medium    |
| First 50 Profiles        | medium    | low       |

Instaloader shall be able to list the comments of a Post.

### Geotags

| Importance | logged-in |
|------------|-----------|
|            | low       |

Instaloader shall be able to access the geotag of a Post (if logged-in).

## Profile Metadata

### Followers

| Importance               | logged-in |
|--------------------------|-----------|
| First page (12 Profiles) | high      |
| First 50 Profiles        | medium    |

Instaloader shall be able to list the followers of a Profile (if logged-in). 

### Followees

| Importance               | logged-in |
|--------------------------|-----------|
| First page (12 Profiles) | high      |
| First 50 Profiles        | medium    |

Instaloader shall be able to list the followees of a Profile (if logged-in). 
