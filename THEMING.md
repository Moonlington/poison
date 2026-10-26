# Theming Poison — parameter contract

One theme, several sites. Everything that distinguishes a site lives in its
`hugo.toml`; nothing site-specific belongs in the theme. If a site needs a visual
change the theme cannot express, add a parameter here rather than forking the CSS.

## Colour

`layouts/partials/head/css.html` turns these parameters into CSS custom
properties, one block for the default scheme and one for `body.dark-theme`.
Omit any of them to keep the theme default shown after the arrow.

### Sidebar (dark in both schemes, so one set of values)
| Parameter | Default | Used for |
|---|---|---|
| `sidebar_bg_color` | `#202020` | sidebar background |
| `sidebar_img_border_color` | `#515151` | border around the brand image |
| `sidebar_p_color` | `#909090` | sidebar description text |
| `sidebar_h1_color` | `#FFF` | brand heading and `.brand-title` |
| `sidebar_a_color` | `#FFF` | sidebar links |
| `sidebar_socials_color` | `#FFF` | social icons |
| `moon_sun_color` | `#FFF` | dark-mode toggle glyph |
| `moon_sun_background_color` | `#515151` | dark-mode toggle background |

### Light scheme
| Parameter | Default |
|---|---|
| `text_color` | `#222` |
| `content_bg_color` | `#FAF9F6` |
| `post_title_color` | `#303030` |
| `list_color` | `#5a5a5a` |
| `link_color` | `#268bd2` |
| `date_color` | `#515151` |
| `table_border_color` | `#E5E5E5` |
| `table_stripe_color` | `#F9F9F9` |
| `code_color` / `code_background_color` | `#000` / `#E5E5E5` |
| `code_block_color` / `code_block_background_color` | `#fff` / `#272822` |

### Dark scheme
Same names with a `_dark` suffix: `text_color_dark`, `content_bg_color_dark`,
`post_title_color_dark`, `list_color_dark`, `link_color_dark`, `date_color_dark`,
`table_border_color_dark`, `table_stripe_color_dark`, `code_color_dark`,
`code_background_color_dark`, `code_block_color_dark`,
`code_block_background_color_dark`.

### Contrast is not optional
`link_color` is the classic failure: a red that reads well on `#121212` is too
dark-blind on `#FAF9F6`. A single value usually cannot serve both schemes, which
is why both exist. Check any new palette with:

```
python3 scripts/contrast.py
```

Body text needs 4.5:1. For reference, `#f42020` measures 3.93:1 on `#FAF9F6`
(fails) and 4.53:1 on `#121212` (passes); `#d81a1a` measures 4.89:1 in light.

### Browser chrome
- `theme_color` — `<meta name="theme-color">` for the light scheme
- `theme_color_dark` — same for dark

## Identity and icons

| Parameter | Notes |
|---|---|
| `brand` | name shown in the sidebar; falls back to `site.Title` |
| `description` | sidebar text and default meta description |
| `brand_image` | path under `/static`, e.g. `/img/logo.png` |
| `remote_brand_image` | absolute URL, wins over `brand_image` |
| `favicon` | defaults to `/favicon.png` |
| `og_image` | default social card, path relative to `assets/` **or** `static/` |

Per-article social cards: set `image:` in the post front matter. It overrides
`og_image` and is also used for `BlogPosting.image`.

## Author

Author metadata reads `site.Params.author.name`, so put it under `[params]`:

```toml
[params.author]
  name = "Your Name"
  email = "you@example.com"
```

A root-level `[author]` table is **not** visible to templates in current Hugo —
it silently produces empty `author`, `article:author` and RSS `managingEditor`
tags. This was one of the bugs fixed in this fork.

## Navigation

```toml
[params]
  menu = [
    {Name = "About", URL = "/about/", HasChildren = false},
    {Name = "Posts", URL = "/posts/", Pre = "Recent posts", HasChildren = true, Limit = 5},
  ]
  github_url = "https://github.com/you"
  rss_icon = true
  rss_section = "posts"
```

Socials are `*_url` parameters (`github_url`, `mastodon_url`, `bluesky_url`,
`email_url`, …). `External = true` on a menu entry marks an off-site link.

## Content contract

- Articles live in any section; the home page lists `front_page_content`
  (default `["posts"]`). The section name is not hardcoded anywhere in the theme.
- `series` may be a string or a list. A list generates one term page per series.
- `tags` render in the byline and as a taxonomy.
- `_index.md` in a section named `about` renders with the about layout.
- Set `robots: "noindex,follow"` in front matter (or via `cascade`) to override
  the default `index,follow`.
- `noindex_paths` in params adds `Disallow:` lines to the generated `robots.txt`.

## Typography

Base CSS lives in `assets/css/hyde.css`. A site overrides it with its own
`assets/css/custom.css`, which the bundle loads last — that is the supported way
to change fonts without touching the theme.

## Breaking changes vs. upstream poison

- `.brand-title` — on non-home pages the brand text is a `<span class="brand-title">`
  instead of a nested `<h1>`. Sites that styled `.sidebar-about h1` must add
  `.brand-title` to those selectors.
- `partial "post/info.html"` accepts a Page or `dict "page" . "heading" 2`.
  Custom callers passing a Page keep working.
- `pagination.html` uses `.Paginator` (the caller's paginator) instead of
  re-paginating with a hardcoded `posts` filter.
- `meta.html` no longer emits `rel=first/last/prev/next`; see the article meta
  section for what replaced it.
